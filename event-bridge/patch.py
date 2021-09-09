
import sys
import re

def patch(current_version):
    f = open('sandbox/kustomize/overlays/prod/kustomization.yaml', 'r')
    data = f.read()
    f.close()

    data = re.sub("newTag:.*", "newTag: " + current_version, data)

    f = open('sandbox/kustomize/overlays/prod/kustomization.yaml', 'w')
    f.write(data)
    f.close()

if __name__ == "__main__":
    current = sys.argv[1]

    patch(current)
    