# VERSION=$(curl https://api.github.com/repos/kiegroup/kogito-runtimes/tags -s | jq -r '.[0].name')
VERSION="1.7.0.Final"

printf $MY_TOKEN > token.txt
gh auth login --with-token < token.txt
gh config set prompt disabled

NEXT_VERSION=$(python3 patch.py $VERSION dry)

git clone git@github.com:r00ta/kogito-examples.git
cd kogito-examples
git remote add upstream git@github.com:kiegroup/kogito-examples.git
git fetch upstream

git checkout $NEXT_VERSION

exit_status=$?
if [ $exit_status -eq 1 ]; then
    printf "There is no branch $NEXT_VERSION available yet"
    exit 0
fi

OUT=$(gh pr list)

if [[ "$OUT" =~ .*"[$NEXT_VERSION] Update trusty images".* ]]; then
    printf "A pull request for updating the trusty images on $NEXT_RELEASE is already out"
    exit 0
fi

git merge upstream/$NEXT_VERSION

git branch $NEXT_VERSION.updateTrustyImages
git checkout $NEXT_VERSION.updateTrustyImages

cd ..
NEXT_VERSION=$(python3 patch.py $VERSION patch)
cd kogito-examples

git add * 
git commit -m "Update trusty images"
git push -u origin $NEXT_VERSION.updateTrustyImages

sleep 15 # GH CLI can't find the branch on remote... needs some time :) 

gh pr create --fill --draft --assignee @me --base $NEXT_VERSION --repo kiegroup/kogito-examples --title "[$NEXT_VERSION] Update trusty images" --body "This Pull request aims to update the trusty images and documentation according to the incoming release"
