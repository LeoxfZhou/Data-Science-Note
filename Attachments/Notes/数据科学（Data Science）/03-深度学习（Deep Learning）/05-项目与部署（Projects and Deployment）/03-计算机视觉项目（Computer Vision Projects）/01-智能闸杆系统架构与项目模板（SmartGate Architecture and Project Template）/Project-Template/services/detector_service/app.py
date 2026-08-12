from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from services.detector_service.predictor import PlateDetector
from shared_utils.image_tool import decode_base64_image


class DetectRequest(BaseModel):
    image_base64: str = Field(min_length=4)


class DetectResponse(BaseModel):
    boxes: list[tuple[int, int, int, int]]
    confidences: list[float]


state: dict[str, PlateDetector] = {}


@asynccontextmanager
async def lifespan(_: FastAPI):
    state["detector"] = PlateDetector(mock=True)
    yield
    state.clear()


app = FastAPI(title="SmartGate Detector", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/detect", response_model=DetectResponse)
def detect(payload: DetectRequest) -> DetectResponse:
    try:
        image = decode_base64_image(payload.image_base64)
        detections = state["detector"].predict(image)
        return DetectResponse(
            boxes=[item.xyxy for item in detections],
            confidences=[item.confidence for item in detections],
        )
    except (ValueError, KeyError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
