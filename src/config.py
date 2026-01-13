from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Paths:
    project_root: Path = Path(__file__).resolve().parents[1]
    data_raw: Path = project_root / "data" / "raw"
    data_processed: Path = project_root / "data" / "processed"
    models: Path = project_root / "models"
    reports: Path = project_root / "reports"

DEFAULT_TRAIN_END = "2017-01-01"  # time split cut
RANDOM_STATE = 42
