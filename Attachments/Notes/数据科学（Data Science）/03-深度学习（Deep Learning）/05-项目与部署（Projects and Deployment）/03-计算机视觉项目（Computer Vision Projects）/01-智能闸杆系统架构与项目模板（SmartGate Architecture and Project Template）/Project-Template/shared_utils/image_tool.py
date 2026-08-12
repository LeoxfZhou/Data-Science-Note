from __future__ import annotations

import base64

import cv2
import numpy as np


def decode_base64_image(encoded: str) -> np.ndarray:
    """把 Base64 字符串解码为 BGR 图像，并对空数据和坏图显式失败。"""
    try:
        raw = base64.b64decode(encoded, validate=True)
    except (ValueError, TypeError) as exc:
        raise ValueError("image_base64 is not valid Base64") from exc
    array = np.frombuffer(raw, dtype=np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("decoded bytes are not a supported image")
    return image


def encode_jpeg(image: np.ndarray, quality: int = 90) -> str:
    """编码 JPEG；质量必须在 1 到 100 之间，防止配置错误被静默接受。"""
    if not 1 <= quality <= 100:
        raise ValueError("quality must be in [1, 100]")
    ok, buffer = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, quality])
    if not ok:
        raise RuntimeError("OpenCV failed to encode JPEG")
    return base64.b64encode(buffer).decode("ascii")
