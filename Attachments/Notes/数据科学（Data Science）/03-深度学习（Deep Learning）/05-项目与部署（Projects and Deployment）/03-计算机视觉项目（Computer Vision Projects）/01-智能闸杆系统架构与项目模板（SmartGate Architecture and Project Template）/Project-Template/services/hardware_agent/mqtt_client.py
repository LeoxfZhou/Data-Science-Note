from __future__ import annotations

import json

import paho.mqtt.client as mqtt


def publish_gate_command(host: str, port: int, topic: str, command: str) -> None:
    """发布一次硬件命令；网络失败会向上抛出，不能伪装成执行成功。"""
    if command not in {"OPEN", "CLOSE"}:
        raise ValueError("command must be OPEN or CLOSE")
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(host, port, keepalive=30)
    client.loop_start()
    try:
        info = client.publish(topic, json.dumps({"command": command}), qos=1)
        info.wait_for_publish(timeout=5)
        if info.rc != mqtt.MQTT_ERR_SUCCESS:
            raise RuntimeError(f"MQTT publish failed with rc={info.rc}")
    finally:
        client.loop_stop()
        client.disconnect()
