printf $MY_TOKEN > /tmp/token.txt
gh auth login --with-token < /tmp/token.txt
gh config set prompt disabled

LATEST_VERSION_MANAGER=$(python3 event-bridge/get_latest_image_version.py fleet-manager)
LATEST_VERSION_SHARD_OPERATOR=$(python3 event-bridge/get_latest_image_version.py fleet-shard)
LATEST_VERSION_EXECUTOR=$(python3 event-bridge/get_latest_image_version.py executor)

printf "Latest version for manager is: $LATEST_VERSION_MANAGER\n"
printf "Latest version for shard operator is: $LATEST_VERSION_SHARD_OPERATOR\n"
printf "Latest version for executor is: $LATEST_VERSION_EXECUTOR\n"

COMMIT_VERSION_MANAGER=$(printf $LATEST_VERSION_MANAGER | grep -Eio '[A-Za-z0-9]{8,}' -m 1)
COMMIT_VERSION_SHARD_OPERATOR=$(printf $LATEST_VERSION_SHARD_OPERATOR | grep -Eio '[A-Za-z0-9]{8,}' -m 1)
COMMIT_VERSION_EXECUTOR=$(printf $LATEST_VERSION_EXECUTOR | grep -Eio '[A-Za-z0-9]{8,}' -m 1)

printf "Found commit $COMMIT_VERSION_MANAGER for manager\n"
printf "Found commit $COMMIT_VERSION_SHARD_OPERATOR for shard operator\n"
printf "Found commit $COMMIT_VERSION_EXECUTOR for executor\n"

git clone git@github.com:r00ta/sandbox.git

cd sandbox
git remote add upstream git@github.com:5733d9e2be6485d52ffa08870cabdee0/sandbox.git
git fetch upstream

git merge upstream/main

MANAGER=$(date -d @$(git log -n1 --format="%at" $COMMIT_VERSION_MANAGER) +%Y%m%d%H%M)
SHARD=$(date -d @$(git log -n1 --format="%at" $COMMIT_VERSION_SHARD_OPERATOR) +%Y%m%d%H%M)
EXECUTOR=$(date -d @$(git log -n1 --format="%at" $COMMIT_VERSION_EXECUTOR) +%Y%m%d%H%M)

printf "Commit date for latest manager is $MANAGER\n"
printf "Commit date for latest shard operator is $SHARD\n"
printf "Commit date for latest executor is $EXECUTOR\n"

if [[ $MANAGER > $SHARD ]]
then
        if [[ $MANAGER > $EXECUTOR ]]
        then
                TO_USE=$COMMIT_VERSION_MANAGER
        else
                TO_USE=$COMMIT_VERSION_EXECUTOR
        fi
elif [[ $SHARD > $EXECUTOR ]]
then
        TO_USE=$COMMIT_VERSION_SHARD_OPERATOR
else
        TO_USE=$COMMIT_VERSION_EXECUTOR
fi

printf "Most recent commit is $TO_USE"

TAG=$(git rev-parse --short HEAD)
SHORT_TAG=${TAG:0:5}

JIRA=$(git log --format=%B -n 1 $TO_USE | grep -Ei 'MGDOBR-[0-9]+' -m 1)

printf "Retrieved jira is $JIRA"
OUT=$(gh pr list)

if [[ "$OUT" =~ .*"$JIRA - Update kustomization images".* ]]; then
    printf "A pull request for updating the kustomization images on $SHORT_TAG - $JIRA is already out"
    exit 0
fi

mvn --batch-mode package -Dmaven.test.skip=true -Dcheckstyle.skip
cp shard-operator/target/kubernetes/bridgeingresses.com.redhat.service.bridge-v1.yml kustomize/base/shard/resources/bridgeingresses.com.redhat.service.bridge-v1.yml
cp shard-operator/target/kubernetes/bridgeexecutors.com.redhat.service.bridge-v1.yml kustomize/base/shard/resources/bridgeexecutors.com.redhat.service.bridge-v1.yml

cd ..
python3 event-bridge/patch.py $LATEST_VERSION_MANAGER $LATEST_VERSION_SHARD_OPERATOR $LATEST_VERSION_INGRESS $LATEST_VERSION_EXECUTOR
cd sandbox


if [ $(git diff | wc -l) -lt 1 ]; then
    printf "VERSION IS ALREADY UPDATED"
    exit 0
fi


git branch $SHORT_TAG.updateImages
git checkout $SHORT_TAG.updateImages

git add *
git commit -m "$JIRA - Update kustomization images"
git push -u origin $SHORT_TAG.updateImages -f

sleep 15 # GH CLI can't find the branch on remote... needs some time :)

gh pr create --fill --draft --base main --repo 5733d9e2be6485d52ffa08870cabdee0/sandbox --title "$JIRA - Update kustomization images" --body "This Pull request aims to update the kustomization images for the PR $JIRA"

rm /tmp/token.txt
