
import sys
import re

def patch(next_version):
    f = open('kogito-examples/trusty-demonstration/docker-compose/docker-compose.yml', 'r')
    data = f.read()
    f.close()

    data = re.sub("kogito-explainability:.*", "kogito-explainability:" + next_version, data)
    data = re.sub("kogito-trusty-infinispan:.*", "kogito-trusty-infinispan:" + next_version, data)
    data = re.sub("kogito-trusty-ui:.*", "kogito-trusty-ui:" + next_version, data)

    f = open('kogito-examples/trusty-demonstration/docker-compose/docker-compose.yml', 'w')
    f.write(data)
    f.close()

    f = open('kogito-examples/trusty-demonstration/kubernetes/README.md', 'r')
    data = f.read()
    f.close()

    data = re.sub("KOGITO_VERSION=v.*", "KOGITO_VERSION=v" + next_version + ".0", data)
    data = re.sub("kogito-trusty-ui:.*", "kogito-trusty-ui:" + next_version, data)

    f = open('kogito-examples/trusty-demonstration/kubernetes/README.md', 'w')
    f.write(data)
    f.close()

    f = open('kogito-examples/trusty-demonstration/kubernetes/resources/explainability.yaml', 'r')
    data = f.read()
    f.close()

    data = re.sub("kogito-explainability:.*", "kogito-explainability:" + next_version, data)

    f = open('kogito-examples/trusty-demonstration/kubernetes/resources/explainability.yaml', 'w')
    f.write(data)
    f.close()

    f = open('kogito-examples/trusty-demonstration/kubernetes/resources/trusty-ui.yaml', 'r')
    data = f.read()
    f.close()

    data = re.sub("kogito-trusty-ui:.*", "kogito-trusty-ui:" + next_version, data)

    f = open('kogito-examples/trusty-demonstration/kubernetes/resources/trusty-ui.yaml', 'w')
    f.write(data)
    f.close()

    f = open('kogito-examples/trusty-demonstration/kubernetes/resources/trusty.yaml', 'r')
    data = f.read()
    f.close()

    data = re.sub("kogito-trusty-infinispan:.*", "kogito-trusty-infinispan:" + next_version, data)

    f = open('kogito-examples/trusty-demonstration/kubernetes/resources/trusty.yaml', 'w')
    f.write(data)
    f.close()


if __name__ == "__main__":
    current = sys.argv[1]
    current = current.replace(".Final", "")
    splitted = current.split(".")
    major = splitted[0]
    minor = str(int(splitted[1]) + 1)
    next_version = major + "." + minor
    
    if sys.argv[2] == 'patch':
        patch(next_version)
     
    print (next_version + ".x")
