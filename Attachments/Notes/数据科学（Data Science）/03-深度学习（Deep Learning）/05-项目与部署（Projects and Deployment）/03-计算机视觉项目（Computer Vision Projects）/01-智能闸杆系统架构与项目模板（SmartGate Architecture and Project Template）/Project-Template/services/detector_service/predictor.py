from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class Detection:
    xyxy: tuple[int, int, int, int]
    confidence: float
    class_name: str = "license_plate"


class PlateDetector:
    """检测器适配层；默认模拟结果，真实引擎只需保持 predict 契约。"""

    def __init__(self, weights: str | None = None, mock: bool = True) -> None:
        self.mock = mock
        self.weights = Path(weights) if weights else None
        if not mock and (self.weights is None or not self.weights.exists()):
            # 真实模式不能悄悄退回模拟结果，否则集成测试会掩盖权重缺失。
            raise FileNotFoundError(f"detector weights not found: {self.weights}")

    def predict(self, image: np.ndarray) -> list[Detection]:
        if image.ndim != 3 or image.shape[2] != 3:
            raise ValueError("detector expects a BGR image with shape [H, W, 3]")
        height, width = image.shape[:2]
        if height == 0 or width == 0:
            raise ValueError("image cannot be empty")
        if self.mock:
            # 中央框让裁剪、OCR 和业务状态机能在无权重环境中完整联调。
            return [Detection((width // 4, height // 3, width * 3 // 4, height * 2 // 3), 0.95)]
        raise NotImplementedError("connect Ultralytics/ONNX detector here")
