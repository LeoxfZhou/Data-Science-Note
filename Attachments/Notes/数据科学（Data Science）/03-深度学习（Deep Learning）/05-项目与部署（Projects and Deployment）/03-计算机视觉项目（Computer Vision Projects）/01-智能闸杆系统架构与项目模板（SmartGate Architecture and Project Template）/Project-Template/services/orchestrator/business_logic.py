from dataclasses import dataclass


@dataclass(frozen=True)
class GateDecision:
    allow: bool
    reason: str


def decide_gate(plate_text: str, confidence: float, allowlist: set[str], minimum_confidence: float) -> GateDecision:
    """采用默认拒绝策略：任何不完整或低置信度输入都不能触发物理开闸。"""
    normalized = plate_text.strip().upper()
    if not normalized:
        return GateDecision(False, "empty_plate")
    if confidence < minimum_confidence:
        return GateDecision(False, "low_confidence")
    if normalized not in allowlist:
        return GateDecision(False, "not_in_allowlist")
    return GateDecision(True, "authorized")
