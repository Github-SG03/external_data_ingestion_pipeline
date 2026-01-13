from github_pipeline.github_ingestion import load_config

def test_config_load():
    config = load_config()
    assert "sources" in config
