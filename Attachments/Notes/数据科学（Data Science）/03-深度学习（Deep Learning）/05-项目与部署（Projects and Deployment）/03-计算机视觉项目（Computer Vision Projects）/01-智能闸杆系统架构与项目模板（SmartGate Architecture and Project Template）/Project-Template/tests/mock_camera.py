import base64

import cv2
import numpy as np


def make_mock_frame(width: int = 320, height: int = 180) -> str:
    """生成含白色车牌区域的 JPEG，供无摄像头环境测试。"""
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.rectangle(frame, (width // 4, height // 3), (width * 3 // 4, height * 2 // 3), (255, 255, 255), -1)
    ok, buffer = cv2.imencode(".jpg", frame)
    if not ok:
        raise RuntimeError("failed to build mock frame")
    return base64.b64encode(buffer).decode("ascii")
