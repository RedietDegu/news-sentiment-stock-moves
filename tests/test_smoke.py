from src import config


def test_data_dirs_can_be_created(tmp_path, monkeypatch):
    """
    Simple smoke test to ensure data directories can be created without error.
    """
    monkeypatch.setattr(config, "DATA_DIR", tmp_path / "data")
    monkeypatch.setattr(config, "RAW_DATA_DIR", config.DATA_DIR / "raw")
    monkeypatch.setattr(config, "INTERIM_DATA_DIR", config.DATA_DIR / "interim")
    monkeypatch.setattr(config, "PROCESSED_DATA_DIR", config.DATA_DIR / "processed")

    # Should not raise
    config.ensure_data_dirs()


