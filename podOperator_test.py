from datetime import datetime, timedelta

from kubernetes.client import models as k8s
from airflow.models import DAG, Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.kubernetes.secret import Secret
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)

dag_id = 'kubernetes-dag-crawler-success'

task_default_args = {
    'execution_timeout': timedelta(hours=1)
}

dag = DAG(
    dag_id=dag_id,
    description='kubernetes pod operator',
    default_args=task_default_args,
    start_date=datetime(2023,6,1),
    schedule_interval='0 * * * *'
)

# env = Secret(
#     'env',
#     'TEST',
#     'test_env',
#     'TEST',
# )

# pod_resources = Resources()
# pod_resources.request_cpu = '1000m'
# pod_resources.request_memory = '512Mi'
# pod_resources.limit_cpu = '1000m'
# pod_resources.limit_memory = '1024Mi'


# configmaps = [
#     k8s.V1EnvFromSource(config_map_ref=k8s.V1ConfigMapEnvSource(name='secret')),
# ]

# start = DummyOperator(task_id="start", dag=dag)

echo = BashOperator(
        task_id="print_echo",
        bash_command="echo print test",
    )

run = KubernetesPodOperator(
    task_id="kubernetespodoperator",
    namespace='airflow',
    in_cluster=True,
    image='crawler-success:1.0.0',
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
