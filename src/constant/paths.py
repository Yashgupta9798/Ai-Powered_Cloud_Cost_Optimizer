from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

ARTIFACTS_DIR = ROOT_DIR / "artifacts"
CONFIG_DIR = ROOT_DIR / "config"
LOGS_DIR = ROOT_DIR / "logs"

PROJECT_DESC_FILE = ARTIFACTS_DIR / "project_description.txt"
PROJECT_PROFILE_FILE = ARTIFACTS_DIR / "project_profile.json"
BILLING_FILE = ARTIFACTS_DIR / "mock_billing.json"
REPORT_FILE = ARTIFACTS_DIR / "cost_optimization_report.json"

for path in [ARTIFACTS_DIR, CONFIG_DIR, LOGS_DIR]:
    path.mkdir(exist_ok=True)
