import os
from kubernetes import client, config, watch

RHOC_NAMESPACE = os.getenv("RHOSE_PROD_RHOC_NAMESPACE")

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

v1 = client.CoreV1Api()
pod_list = v1.list_namespaced_pod(RHOC_NAMESPACE)

for pod in pod_list.items:
    logs = v1.read_namespaced_pod_log(name=pod.metadata.name, namespace=RHOC_NAMESPACE)
    if "Terminating KafkaConsumer thread" in logs:
        print("Terminating pod " + pod.metadata.name)
        delete_namespaced_pod(pod.metadata.name, RHOC_NAMESPACE, body=client.V1DeleteOptions())
        print("Terminating pod " + pod.metadata.name " + done)
