from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

k = KubernetesPodOperator(
    name="pod-operator-=test",
    image="crawler_test",
    cmds=["bash", "-cx"],
    arguments=["--app.name=dag_test"],
    task_id="dry_run_demo",
    do_xcom_push=True,
)

k.dry_run()
