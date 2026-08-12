from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from services.orchestrator.pipeline import SmartGatePipeline


class GateRequest(BaseModel):
    image_base64: str = Field(min_length=4)


class GateResponse(BaseModel):
    allow: bool
    reason: str
    plate_text: str | None
    ocr_confidence: float | None = None


app = FastAPI(title="SmartGate Orchestrator")
pipeline = SmartGatePipeline(allowlist={"TEST001", "沪ARZ007"})


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/gate/decision", response_model=GateResponse)
def gate_decision(payload: GateRequest) -> GateResponse:
    try:
        return GateResponse(**pipeline.run(payload.image_base64))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
