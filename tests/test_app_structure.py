"""Integration tests for app structure and imports."""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestAppStructure(unittest.TestCase):
    """Test that the app structure is correct."""

    def test_app_file_exists(self):
        """Test that app.py exists."""
        app_path = Path(__file__).parent.parent / "app.py"
        self.assertTrue(app_path.exists(), "app.py should exist")

    def test_core_package_exists(self):
        """Test that core package exists."""
        core_path = Path(__file__).parent.parent / "core"
        self.assertTrue(core_path.exists(), "core/ should exist")
        self.assertTrue((core_path / "__init__.py").exists())

    def test_utils_package_exists(self):
        """Test that utils package exists."""
        utils_path = Path(__file__).parent.parent / "utils"
        self.assertTrue(utils_path.exists(), "utils/ should exist")
        self.assertTrue((utils_path / "__init__.py").exists())

    def test_data_directory_exists(self):
        """Test that data directory exists."""
        data_path = Path(__file__).parent.parent / "data"
        self.assertTrue(data_path.exists(), "data/ should exist")

    def test_database_file_exists(self):
        """Test that database file exists."""
        db_path = Path(__file__).parent.parent / "data" / "greatglobe.db"
        self.assertTrue(db_path.exists(), "data/greatglobe.db should exist")

    def test_requirements_exists(self):
        """Test that requirements.txt exists."""
        req_path = Path(__file__).parent.parent / "requirements.txt"
        self.assertTrue(req_path.exists(), "requirements.txt should exist")

    def test_readme_exists(self):
        """Test that README.md exists."""
        readme_path = Path(__file__).parent.parent / "README.md"
        self.assertTrue(readme_path.exists(), "README.md should exist")

    def test_security_guide_exists(self):
        """Test that SECURITY.md exists."""
        security_path = Path(__file__).parent.parent / "SECURITY.md"
        self.assertTrue(security_path.exists(), "SECURITY.md should exist")

    def test_deployment_guide_exists(self):
        """Test that DEPLOYMENT_GUIDE.md exists."""
        deploy_path = Path(__file__).parent.parent / "DEPLOYMENT_GUIDE.md"
        self.assertTrue(deploy_path.exists(), "DEPLOYMENT_GUIDE.md should exist")

    def test_github_workflow_exists(self):
        """Test that GitHub Actions workflow exists."""
        workflow_path = Path(__file__).parent.parent / ".github" / "workflows" / "deploy.yml"
        self.assertTrue(workflow_path.exists(), ".github/workflows/deploy.yml should exist")

    def test_gitignore_exists(self):
        """Test that .gitignore exists."""
        gitignore_path = Path(__file__).parent.parent / ".gitignore"
        self.assertTrue(gitignore_path.exists(), ".gitignore should exist")

    def test_streamlit_config_exists(self):
        """Test that Streamlit config exists."""
        config_path = Path(__file__).parent.parent / ".streamlit" / "config.toml"
        self.assertTrue(config_path.exists(), ".streamlit/config.toml should exist")


class TestImports(unittest.TestCase):
    """Test that all modules can be imported."""

    def test_import_core_groq_client(self):
        """Test importing groq_client."""
        from core.groq_client import (
            TokenBudget,
            estimate_tokens,
            create_llm,
            BUDGET,
        )
        self.assertIsNotNone(TokenBudget)
        self.assertIsNotNone(estimate_tokens)
        self.assertIsNotNone(create_llm)
        self.assertIsNotNone(BUDGET)

    def test_import_core_database(self):
        """Test importing database module."""
        from core.database import (
            get_product_by_id,
            search_products,
            get_all_products,
            check_database_exists,
        )
        self.assertIsNotNone(get_product_by_id)
        self.assertIsNotNone(search_products)
        self.assertIsNotNone(get_all_products)
        self.assertTrue(check_database_exists())

    def test_import_core_tools(self):
        """Test importing tools module."""
        from core.tools import (
            create_tools_dict,
            product_lookup_tool,
            web_search_tool,
        )
        self.assertIsNotNone(create_tools_dict)
        self.assertIsNotNone(product_lookup_tool)
        self.assertIsNotNone(web_search_tool)

    def test_import_core_agent(self):
        """Test importing agent module."""
        from core.agent import (
            create_compliance_agent,
            invoke_agent,
            simple_compliance_lookup,
        )
        self.assertIsNotNone(create_compliance_agent)
        self.assertIsNotNone(invoke_agent)
        self.assertIsNotNone(simple_compliance_lookup)

    def test_import_utils_helpers(self):
        """Test importing helpers module."""
        from utils.helpers import (
            clip,
            validate_product_id,
            validate_country,
            format_product_display,
        )
        self.assertIsNotNone(clip)
        self.assertIsNotNone(validate_product_id)
        self.assertIsNotNone(validate_country)
        self.assertIsNotNone(format_product_display)


class TestConfiguration(unittest.TestCase):
    """Test configuration constants."""

    def test_token_budget_configuration(self):
        """Test token budget configuration."""
        from core import TPM_LIMIT, TPM_SAFETY, RATE_RETRIES
        self.assertEqual(TPM_LIMIT, 8000)
        self.assertEqual(TPM_SAFETY, 0.80)
        self.assertEqual(RATE_RETRIES, 6)

    def test_model_configuration(self):
        """Test model configuration."""
        from core import MODEL_NAME, LLM_MAX_TOKENS
        self.assertEqual(MODEL_NAME, "openai/gpt-oss-120b")
        self.assertEqual(LLM_MAX_TOKENS, 2000)

    def test_database_configuration(self):
        """Test database configuration."""
        from core.database import check_database_exists
        self.assertTrue(check_database_exists())


if __name__ == '__main__':
    unittest.main()
