from pathlib import Path


def validate_dataset(dataset_dir: Path) -> list[Path]:
    """OCR 训练实现前先验证数据目录，避免空数据集仍启动长时间训练。"""
    images = sorted(dataset_dir.glob("*.jpg")) + sorted(dataset_dir.glob("*.png"))
    if not images:
        raise ValueError(f"no OCR images found in {dataset_dir}")
    return images


if __name__ == "__main__":
    files = validate_dataset(Path("data/processed/ocr"))
    raise NotImplementedError(f"connect OCR trainer here; validated {len(files)} images")
