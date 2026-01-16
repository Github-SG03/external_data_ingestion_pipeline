from src.ingestion.config import load_sources

def test_sources_load():
    sources = load_sources()
    assert isinstance(sources, list)
