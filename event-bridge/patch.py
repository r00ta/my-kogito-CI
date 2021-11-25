import sys
import re
import yaml

def patch(current_all_in_one, current_fleet_shard, current_ingress, current_executor):
    with open("sandbox/kustomize/overlays/prod/kustomization.yaml", "r") as stream:
        try:
            prod_kustomization = yaml.full_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

    # All in one
    all_in_one = next(filter(lambda x: x['name'] == 'event-bridge-all-in-one', prod_kustomization['images']))
    all_in_one['newTag'] = current_all_in_one

    # Shard
    shard = next(filter(lambda x: x['name'] == 'event-bridge-shard-operator', prod_kustomization['images']))
    shard['newTag'] = current_fleet_shard

    with open('sandbox/kustomize/overlays/prod/kustomization.yaml', 'w') as outfile:
        yaml.dump(prod_kustomization, outfile)

    with open("sandbox/kustomize/overlays/prod/shard/patches/deploy-config.yaml", "r") as stream:
        try:
            shard_patch = yaml.full_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

    shard_patch['data']['EVENT_BRIDGE_INGRESS_IMAGE'] = "quay.io/5733d9e2be6485d52ffa08870cabdee0/ingress:" + current_ingress
    shard_patch['data']['EVENT_BRIDGE_EXECUTOR_IMAGE'] = "quay.io/5733d9e2be6485d52ffa08870cabdee0/executor:" + current_executor

    with open('sandbox/kustomize/overlays/prod/shard/patches/deploy-config.yaml', 'w') as outfile:
        yaml.dump(shard_patch, outfile)

if __name__ == "__main__":
    current_all_in_one = sys.argv[1]
    current_fleet_shard = sys.argv[2]
    current_ingress = sys.argv[3]
    current_executor = sys.argv[4]
    patch(current_all_in_one, current_fleet_shard, current_ingress, current_executor)
