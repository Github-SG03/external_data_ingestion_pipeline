def test_dag_import():
    from dags.external_ingestion_dag import dag

    assert dag.dag_id == "external_data_ingestion"
