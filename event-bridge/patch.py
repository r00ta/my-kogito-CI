import sys
import re
import yaml

def patch(current_fleet_manager, current_fleet_shard, current_executor):
    current_fleet_shard = current_fleet_shard.split("-")[1]
    
    # prod overlay
    with open("sandbox/kustomize/base-openshift/kustomization.yaml", "r") as stream:
        try:
            prod_kustomization = yaml.full_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

    # Manager
    manager = next(filter(lambda x: x['name'] == 'event-bridge-manager', prod_kustomization['images']))
    manager['newTag'] = current_fleet_manager

    # Shard
    shard = next(filter(lambda x: x['name'] == 'event-bridge-shard-operator', prod_kustomization['images']))
    shard['newTag'] = "ocp-" + current_fleet_shard + "-jvm"

    with open('sandbox/kustomize/base-openshift/kustomization.yaml', 'w') as outfile:
        yaml.dump(prod_kustomization, outfile)
        
    with open("sandbox/kustomize/base-openshift/shard/patches/deploy-config.yaml", "r") as stream:
        try:
            shard_patch = yaml.full_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

    shard_patch['data']['EVENT_BRIDGE_EXECUTOR_IMAGE'] = "quay.io/5733d9e2be6485d52ffa08870cabdee0/executor:" + current_executor

    with open('sandbox/kustomize/base-openshift/shard/patches/deploy-config.yaml', 'w') as outfile:
        yaml.dump(shard_patch, outfile)

    # ci overlay
    with open("sandbox/kustomize/overlays/ci/kustomization.yaml", "r") as stream:
        try:
            ci_kustomization = yaml.full_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

    # Manager
    manager = next(filter(lambda x: x['name'] == 'event-bridge-manager', ci_kustomization['images']))
    manager['newTag'] = current_fleet_manager

    # Shard
    shard = next(filter(lambda x: x['name'] == 'event-bridge-shard-operator', ci_kustomization['images']))
    shard['newTag'] = "k8s-" + current_fleet_shard + "-jvm"

    with open('sandbox/kustomize/overlays/ci/kustomization.yaml', 'w') as outfile:
        yaml.dump(ci_kustomization, outfile)

    with open("sandbox/kustomize/overlays/ci/shard/patches/deploy-config.yaml", "r") as stream:
        try:
            shard_patch = yaml.full_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

    shard_patch['data']['EVENT_BRIDGE_EXECUTOR_IMAGE'] = "quay.io/5733d9e2be6485d52ffa08870cabdee0/executor:" + current_executor

    with open('sandbox/kustomize/overlays/ci/shard/patches/deploy-config.yaml', 'w') as outfile:
        yaml.dump(shard_patch, outfile)

    # prod overlay
    with open("sandbox/kustomize/overlays/prod/kustomization.yaml", "r") as stream:
        try:
            prod_kustomization = yaml.full_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

    # Shard
    shard = next(filter(lambda x: x['name'] == 'event-bridge-shard-operator', prod_kustomization['images']))
    shard['newTag'] = "ocp-" + current_fleet_shard + "-jvm"

    with open('sandbox/kustomize/overlays/prod/kustomization.yaml', 'w') as outfile:
        yaml.dump(prod_kustomization, outfile)

    with open("sandbox/kustomize/overlays/prod/patches/deploy-config.yaml", "r") as stream:
        try:
            shard_patch = yaml.full_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

    shard_patch['data']['EVENT_BRIDGE_EXECUTOR_IMAGE'] = "quay.io/5733d9e2be6485d52ffa08870cabdee0/executor:" + current_executor

    with open('sandbox/kustomize/overlays/prod/patches/deploy-config.yaml', 'w') as outfile:
        yaml.dump(shard_patch, outfile)
        
if __name__ == "__main__":
    current_fleet_manager = sys.argv[1]
    current_fleet_shard = sys.argv[2]
    current_executor = sys.argv[3]
    patch(current_fleet_manager, current_fleet_shard, current_executor)
