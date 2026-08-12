from services.orchestrator.business_logic import decide_gate
from services.orchestrator.pipeline import SmartGatePipeline
from tests.mock_camera import make_mock_frame


def test_authorized_plate_opens_gate() -> None:
    pipeline = SmartGatePipeline(allowlist={"TEST001"})
    result = pipeline.run(make_mock_frame())
    assert result["allow"] is True
    assert result["reason"] == "authorized"


def test_unknown_plate_fails_closed() -> None:
    decision = decide_gate("UNKNOWN", 0.99, {"TEST001"}, 0.75)
    assert decision.allow is False
    assert decision.reason == "not_in_allowlist"


def test_low_confidence_fails_closed() -> None:
    decision = decide_gate("TEST001", 0.50, {"TEST001"}, 0.75)
    assert decision.allow is False
    assert decision.reason == "low_confidence"
