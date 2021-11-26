printf $MY_TOKEN > token.txt
gh auth login --with-token < token.txt
gh config set prompt disabled

LATEST_VERSION_MANAGER=$(python3 event-bridge/get_latest_image_version.py fleet-manager)
LATEST_VERSION_SHARD_OPERATOR=$(python3 event-bridge/get_latest_image_version.py fleet-shard)
LATEST_VERSION_INGRESS=$(python3 event-bridge/get_latest_image_version.py ingress)
LATEST_VERSION_EXECUTOR=$(python3 event-bridge/get_latest_image_version.py executor)

git clone git@github.com:r00ta/sandbox.git

cd sandbox
git remote add upstream git@github.com:5733d9e2be6485d52ffa08870cabdee0/sandbox.git
git fetch upstream

git merge upstream/main

TAG=$(git rev-parse --short HEAD)
SHORT_TAG=${TAG:0:5}

OUT=$(gh pr list)

if [[ "$OUT" =~ .*"[$SHORT_TAG] Update kustomization images".* ]]; then
    printf "A pull request for updating the kustomization images on $SHORT_TAG is already out"
    exit 0
fi

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
git commit -m "Update kustomization images"
git push -u origin $SHORT_TAG.updateImages

sleep 15 # GH CLI can't find the branch on remote... needs some time :) 

gh pr create --fill --draft --assignee @me --base main --repo 5733d9e2be6485d52ffa08870cabdee0/sandbox --title "[$SHORT_TAG] Update kustomization images" --body "This Pull request aims to update the kustomization images"
