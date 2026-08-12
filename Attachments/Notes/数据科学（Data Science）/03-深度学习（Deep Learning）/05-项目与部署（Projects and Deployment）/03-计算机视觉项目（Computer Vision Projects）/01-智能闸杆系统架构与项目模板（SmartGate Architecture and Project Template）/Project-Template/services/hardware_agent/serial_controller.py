from __future__ import annotations

import serial


def send_gate_command(port: str, baudrate: int, command: str) -> bytes:
    """通过串口发送带换行的 ASCII 命令，并返回设备回执。"""
    if command not in {"OPEN", "CLOSE"}:
        raise ValueError("command must be OPEN or CLOSE")
    with serial.Serial(port=port, baudrate=baudrate, timeout=2) as connection:
        connection.write((command + "\n").encode("ascii"))
        connection.flush()
        acknowledgement = connection.readline().strip()
    if not acknowledgement:
        raise TimeoutError("gate controller did not acknowledge the command")
    return acknowledgement
