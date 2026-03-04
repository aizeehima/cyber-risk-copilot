from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import yaml


DEFAULT_WEIGHTS_PATH = Path("config/weights.yaml")


@dataclass
class WeightsConfig:
    raw: Dict[str, Any]

    @property
    def max_scores(self) -> Dict[str, int]:
        return self.raw.get("max_scores", {})

    @property
    def weights(self) -> Dict[str, Any]:
        return self.raw.get("weights", {})

    @property
    def normalized_max(self) -> int:
        return int(self.raw.get("scale", {}).get("normalized_max", 10))


def load_weights(path: Path = DEFAULT_WEIGHTS_PATH) -> WeightsConfig:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("weights.yaml must parse to a dictionary.")
    return WeightsConfig(raw=data)
