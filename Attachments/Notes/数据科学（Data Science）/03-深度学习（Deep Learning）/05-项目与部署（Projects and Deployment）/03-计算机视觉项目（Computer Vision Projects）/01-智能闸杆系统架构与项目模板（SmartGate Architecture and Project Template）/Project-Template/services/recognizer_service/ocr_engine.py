from __future__ import annotations

from pathlib import Path

import numpy as np


class PlateRecognizer:
    """OCR 适配层；真实 CRNN/ONNX 引擎应返回文本和置信度。"""

    def __init__(self, weights: str | None = None, mock: bool = True) -> None:
        self.mock = mock
        self.weights = Path(weights) if weights else None
        if not mock and (self.weights is None or not self.weights.exists()):
            raise FileNotFoundError(f"OCR weights not found: {self.weights}")

    def recognize(self, plate_image: np.ndarray) -> tuple[str, float]:
        if plate_image.size == 0:
            raise ValueError("plate crop cannot be empty")
        if self.mock:
            return "TEST001", 0.98
        raise NotImplementedError("connect CRNN/ONNX OCR engine here")
