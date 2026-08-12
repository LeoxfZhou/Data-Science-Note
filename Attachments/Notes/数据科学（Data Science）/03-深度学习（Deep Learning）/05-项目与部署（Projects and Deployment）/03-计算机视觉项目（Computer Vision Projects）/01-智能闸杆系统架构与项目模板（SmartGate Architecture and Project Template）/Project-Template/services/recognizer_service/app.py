from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from services.recognizer_service.ocr_engine import PlateRecognizer
from shared_utils.image_tool import decode_base64_image


class RecognizeRequest(BaseModel):
    plate_base64: str = Field(min_length=4)


class RecognizeResponse(BaseModel):
    plate_text: str
    confidence: float


state: dict[str, PlateRecognizer] = {}


@asynccontextmanager
async def lifespan(_: FastAPI):
    state["recognizer"] = PlateRecognizer(mock=True)
    yield
    state.clear()


app = FastAPI(title="SmartGate Recognizer", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/recognize", response_model=RecognizeResponse)
def recognize(payload: RecognizeRequest) -> RecognizeResponse:
    try:
        image = decode_base64_image(payload.plate_base64)
        text, confidence = state["recognizer"].recognize(image)
        return RecognizeResponse(plate_text=text, confidence=confidence)
    except (ValueError, KeyError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
