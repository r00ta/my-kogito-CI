printf $MY_TOKEN > /tmp/token.txt
gh auth login --with-token < /tmp/token.txt
gh config set prompt disabled

rhoas login --token $OPENSHIFT_OFFLINE_TOKEN

export MANAGED_CONNECTORS_CLUSTER_ID=none
export MANAGED_KAFKA_INSTANCE_NAME=smart-events

# OPENSHIFT_OFFLINE_TOKEN already injected in env var

git clone https://github.com/5733d9e2be6485d52ffa08870cabdee0/sandbox.git

cd sandbox

rhoas kafka list | grep smart-events

if [ $? -ne 0 ]; then   
    # Clean up service accounts 
    ocm login --token $OPENSHIFT_OFFLINE_TOKEN
    chmod +x ./dev/bin/troubleshoot/cleanup-service-accounts.sh
    ./dev/bin/troubleshoot/cleanup-service-accounts.sh jrota
    
    chmod +x ./dev/bin/kafka-setup.sh
    ./dev/bin/kafka-setup.sh

    gh gist edit $SMART_EVENTS_GIST_ID -a ./dev/bin/credentials/smart-events.json
    gh gist edit $SMART_EVENTS_ADMIN_GIST_ID -a ./dev/bin/credentials/smart-events-admin.json
    gh gist edit $SMART_EVENTS_OPS_GIST_ID -a ./dev/bin/credentials/smart-events-ops.json
    gh gist edit $SMART_EVENTS_MC_GIST_ID -a ./dev/bin/credentials/smart-events-mc.json
fi