import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "scaffold", Path(__file__).parents[1] / "tools" / "scaffold.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
BUNDLE = Path(__file__).resolve().parents[2]


class ScaffoldTests(unittest.TestCase):
    def test_generate(self):
        with tempfile.TemporaryDirectory() as directory:
            target = module.scaffold("orders-api", "xWalker3139", directory, BUNDLE)
            self.assertTrue((target / "src/forge_service/main.py").exists())
            self.assertTrue((target / "deploy/chart/Chart.yaml").exists())
            self.assertIn("orders-api", (target / "deploy/values.yaml").read_text())
            with self.assertRaises(FileExistsError):
                module.scaffold("orders-api", "xWalker3139", directory, BUNDLE)

    def test_path_traversal_rejected(self):
        with self.assertRaises(ValueError):
            module.scaffold("../bad", "owner", "generated", BUNDLE)
