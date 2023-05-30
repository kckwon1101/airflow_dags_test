from datetime import datetime, timedelta

from kubernetes.client import models as k8s
from airflow.models import DAG, Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.kubernetes.secret import Secret
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)

dag_id = 'kubernetes-dag-crawler-fail'

with DAG(
    dag_id,
    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        'execution_timeout': timedelta(hours=1)
    },
    description="A simple tutorial DAG",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:

    echo = BashOperator(
        task_id="print_echo",
        bash_command="echo print test",
    )

    run = KubernetesPodOperator(
        task_id="kubernetespodoperator",
        namespace='airflow',
        in_cluster=True,
        image='crawler-fail:1.0.0',
    #     secrets=[
    #         env
    #     ],
    #     image_pull_secrets=[k8s.V1LocalObjectReference('image_credential')],
        name="job",
        is_delete_operator_pod=False,
        get_logs=True,
    #     resources=pod_resources,
    #     env_from=configmaps,
        dag=dag,
        do_xcom_push=True,
    )

    pod_task_xcom_result = BashOperator(
            bash_command="echo \"{{ task_instance.xcom_pull('write-xcom')[0] }}\"",
            task_id="pod_task_xcom_result",
        )

    # start >> 
    echo >> run >> pod_task_xcom_result
