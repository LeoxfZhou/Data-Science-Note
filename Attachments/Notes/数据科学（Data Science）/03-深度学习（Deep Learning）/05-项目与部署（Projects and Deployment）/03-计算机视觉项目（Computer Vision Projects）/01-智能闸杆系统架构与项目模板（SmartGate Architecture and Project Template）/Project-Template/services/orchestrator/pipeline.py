from __future__ import annotations

from dataclasses import asdict

from services.detector_service.predictor import PlateDetector
from services.orchestrator.business_logic import decide_gate
from services.recognizer_service.ocr_engine import PlateRecognizer
from shared_utils.image_tool import decode_base64_image


class SmartGatePipeline:
    """本地组合管道；生产版可把两个适配器替换成 HTTP 客户端。"""

    def __init__(self, allowlist: set[str], minimum_confidence: float = 0.75) -> None:
        self.detector = PlateDetector(mock=True)
        self.recognizer = PlateRecognizer(mock=True)
        self.allowlist = allowlist
        self.minimum_confidence = minimum_confidence

    def run(self, image_base64: str) -> dict[str, object]:
        image = decode_base64_image(image_base64)
        detections = self.detector.predict(image)
        if not detections:
            return {"allow": False, "reason": "no_plate_detected", "plate_text": None}
        best = max(detections, key=lambda item: item.confidence)
        x1, y1, x2, y2 = best.xyxy
        crop = image[y1:y2, x1:x2]
        plate_text, ocr_confidence = self.recognizer.recognize(crop)
        decision = decide_gate(plate_text, ocr_confidence, self.allowlist, self.minimum_confidence)
        return {**asdict(decision), "plate_text": plate_text, "ocr_confidence": ocr_confidence}
