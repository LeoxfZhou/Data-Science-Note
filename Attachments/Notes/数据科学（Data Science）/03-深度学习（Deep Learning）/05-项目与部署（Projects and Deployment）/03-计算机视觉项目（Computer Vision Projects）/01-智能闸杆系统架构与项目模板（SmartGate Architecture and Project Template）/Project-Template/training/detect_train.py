from pathlib import Path


def train_detector(data_yaml: Path, weights: str = "yolov8n.pt", epochs: int = 100) -> None:
    """训练入口延迟导入 Ultralytics，未安装时不会影响模拟服务与单元测试。"""
    if not data_yaml.exists():
        raise FileNotFoundError(data_yaml)
    from ultralytics import YOLO

    model = YOLO(weights)
    model.train(data=str(data_yaml), epochs=epochs, imgsz=640, seed=42)


if __name__ == "__main__":
    train_detector(Path("data/annotations/data.yaml"))
