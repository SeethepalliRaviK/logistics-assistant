"""Rate-limited Groq LLM client with token budget management."""

import os
import re
import time
import random
from typing import Any, List

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from core import TPM_LIMIT, TPM_SAFETY, RATE_RETRIES, LLM_MAX_TOKENS, MODEL_NAME


class TokenBudget:
    """Rolling 60-second token budget manager for Groq rate limiting.

    Groq measures tokens per minute over a sliding window. This class reserves
    the estimated cost up front and sleeps until the window has room, rather than
    firing a request and reacting to a 429 error.
    """

    def __init__(self, tpm_limit: int, safety: float = 0.8):
        self.limit = int(tpm_limit * safety)
        self.events: List[List[float]] = []  # [timestamp, tokens] per call

    def _prune(self) -> None:
        """Drop events older than 60s (outside the rolling window)."""
        cutoff = time.time() - 60
        self.events = [e for e in self.events if e[0] > cutoff]

    def used(self) -> int:
        """Return tokens spent inside the current 60-second window."""
        self._prune()
        return int(sum(e[1] for e in self.events))

    def reserve(self, tokens: int) -> None:
        """Block until tokens fit inside the current window, then record them."""
        tokens = min(tokens, self.limit)
        while True:
            self._prune()
            if self.used() + tokens <= self.limit or not self.events:
                break
            # Not enough room - sleep until oldest event ages out
            wait = max(61 - (time.time() - self.events[0][0]), 1.0)
            print(
                f"  [budget] {self.used()}/{self.limit} tokens used this minute - "
                f"waiting {wait:.0f}s for the window to refill"
            )
            time.sleep(wait)
        self.events.append([time.time(), tokens])

    def settle(self, estimated: int, actual: int) -> None:
        """Replace estimate with actual usage once API reports it."""
        if self.events and actual > 0:
            self.events[-1][1] = min(actual, self.limit)

    def penalise(self) -> None:
        """After a 429 error, assume the window is full."""
        self.events.append([time.time(), self.limit])


# Global token budget instance
BUDGET = TokenBudget(TPM_LIMIT, TPM_SAFETY)


def estimate_tokens(text: Any) -> int:
    """Rough character-based estimate (3 chars/token). Deliberately pessimistic."""
    return max(1, len(str(text or "")) // 3)


def estimate_messages_tokens(messages) -> int:
    """Sum estimated cost of all messages and tool calls in a request."""
    total = 0
    for m in messages:
        content = getattr(m, "content", m)
        total += estimate_tokens(content) + 4
        for tc in getattr(m, "tool_calls", None) or []:
            total += estimate_tokens(tc)
    return total


def parse_retry_after(error_text: str, default: float = 20.0) -> float:
    """Parse wait time from Groq error message (e.g., 'Please try again in 3.53s')."""
    m = re.search(r"try again in ([\d.]+)\s*m?s", error_text, re.I)
    if m:
        secs = float(m.group(1))
        if "ms" in error_text[m.start() : m.end() + 3].lower():
            secs /= 1000.0
        return secs + 2.0
    m = re.search(r"try again in (\d+)m([\d.]+)s", error_text, re.I)
    if m:
        return float(m.group(1)) * 60 + float(m.group(2)) + 2.0
    return default


def is_rate_limit(err: Exception) -> bool:
    """Detect a 429 rate limit error across different client implementations."""
    msg = str(err).lower()
    return any(
        k in msg for k in ["rate limit", "rate_limit", "429", "too many requests"]
    )


def cooldown(seconds: int = 60) -> None:
    """Pause between runs to reset the per-minute allowance."""
    print(f"Cooling down for {seconds}s to reset the per-minute allowance...")
    time.sleep(seconds)
    BUDGET.events.clear()
    print("Ready.")


class RateLimitedChatGroq(ChatGroq):
    """ChatGroq subclass with built-in rate limiting and retry logic."""

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        # Estimate request cost up front
        estimated = estimate_messages_tokens(messages) + (self.max_tokens or 512)

        for attempt in range(RATE_RETRIES):
            BUDGET.reserve(estimated)
            try:
                # Call parent implementation
                result = super()._generate(
                    messages, stop=stop, run_manager=run_manager, **kwargs
                )

                # Reconcile with actual usage from API
                try:
                    usage = (result.llm_output or {}).get("token_usage", {})
                    actual = usage.get("total_tokens", 0)
                    if actual:
                        BUDGET.settle(estimated, int(actual))
                except Exception:
                    pass
                return result

            except Exception as e:
                if not is_rate_limit(e) or attempt == RATE_RETRIES - 1:
                    raise

                BUDGET.penalise()
                wait = parse_retry_after(str(e))
                print(
                    f"  [429] rate limited - waiting {wait:.1f}s "
                    f"(attempt {attempt + 1}/{RATE_RETRIES})"
                )
                time.sleep(wait)

        raise RuntimeError("Exhausted rate-limit retries")


def create_llm(groq_api_key: str) -> RateLimitedChatGroq:
    """Factory function to create a rate-limited LLM instance."""
    return RateLimitedChatGroq(
        model=MODEL_NAME,
        temperature=0,
        max_tokens=LLM_MAX_TOKENS,
        max_retries=0,
        groq_api_key=groq_api_key,
    )


def safe_llm_call(messages, model=None, retries: int = 3) -> str:
    """Call LLM and retry on transient failures (timeouts, 502/503, etc).

    Rate-limit (429) handling is already inside RateLimitedChatGroq, so this
    only covers other transient failures.
    """
    model = model or None  # Will use the provided model

    for attempt in range(retries):
        try:
            result = model.invoke(messages)
            return result.content

        except Exception as e:
            msg = str(e).lower()
            transient = any(
                k in msg
                for k in ["timeout", "overloaded", "503", "502", "connection", "rate limit"]
            )
            if not transient or attempt == retries - 1:
                print(f"  [LLM error] {e}")
                return ""

            # Exponential backoff with jitter
            wait = 5.0 * (2 ** attempt) + random.uniform(0, 2)
            print(f"  [retry {attempt + 1}/{retries}] {type(e).__name__} - waiting {wait:.1f}s")
            time.sleep(wait)

    return ""
