from datetime import datetime, timedelta

from kubernetes.client import models as k8s
from airflow.models import DAG, Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.kubernetes.secret import Secret
from airflow.kubernetes.pod import Resources
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)

dag_id = 'kubernetes-dag'

task_default_args = {
    'execution_timeout': timedelta(hours=1)
}

dag = DAG(
    dag_id=dag_id,
    description='kubernetes pod operator',
    default_args=task_default_args,
    schedule_interval='0 * * * *',
    max_active_runs=1
)

# env = Secret(
#     'env',
#     'TEST',
#     'test_env',
#     'TEST',
# )

pod_resources = Resources()
pod_resources.request_cpu = '1000m'
pod_resources.request_memory = '512Mi'
pod_resources.limit_cpu = '1000m'
pod_resources.limit_memory = '1024Mi'


# configmaps = [
#     k8s.V1EnvFromSource(config_map_ref=k8s.V1ConfigMapEnvSource(name='secret')),
# ]

start = DummyOperator(task_id="start", dag=dag)

run = KubernetesPodOperator(
    task_id="kubernetespodoperator",
    namespace='airflow',
    image='crawler_test',
#     secrets=[
#         env
#     ],
#     image_pull_secrets=[k8s.V1LocalObjectReference('image_credential')],
    name="job",
    is_delete_operator_pod=True,
    get_logs=True,
    resources=pod_resources,
    env_from=configmaps,
    dag=dag,
)

start >> run
