import sys
import re

def patch(current_all_in_one, current_fleet_shard, current_ingress, current_executor):
    with open("sandbox/kustomize/overlays/prod/kustomization.yaml", "r") as stream:
        try:
            prod_kustomization = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

    data = re.sub("newTag:.*", "newTag: " + current_version, data)

    # Shard
    shard = filter(lambda x: x['name'] == 'event-bridge-shard-operator', prod_kustomization['images'])
    shard[0]['newTag'] = current_fleet_shard

    with open('sandbox/kustomize/overlays/prod/kustomization.yaml', 'w') as outfile:
        yaml.dump(prod_kustomization, outfile, default_flow_style=True)

    with open("sandbox/kustomize/overlays/prod/shard/patches/deploy-config.yaml", "r") as stream:
        try:
            shard_patch = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)
    # ingress
    shard_patch['data']['EVENT_BRIDGE_INGRESS_IMAGE'] = current_ingress

    # executor 
    shard_patch['data']['EVENT_BRIDGE_EXECUTOR_IMAGE'] = current_executor

    with open('sandbox/kustomize/overlays/prod/shard/patches/deploy-config.yaml', 'w') as outfile:
        yaml.dump(shard_patch, outfile, default_flow_style=True)

if __name__ == "__main__":
    current_all_in_one = sys.argv[1]
    current_fleet_shard = sys.argv[2]
    current_ingress = sys.argv[3]
    current_executor = sys.argv[4]
    patch(current_all_in_one, current_fleet_shard, current_ingress, current_executor)
