curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null

sudo apt update
sudo apt install gh
sudo apt install jq

# RH
curl -o- https://raw.githubusercontent.com/redhat-developer/app-services-cli/main/scripts/install.sh | bash
mkdir -p ~/bin
curl -Lo ~/bin/ocm https://github.com/openshift-online/ocm-cli/releases/download/v0.1.61/ocm-linux-amd64
chmod +x ~/bin/ocm

git config --global user.name $GH_USER 
git config --global user.email $GH_EMAIL

pip install pyyaml

mkdir -p ~/.ssh/
echo "$MY_KEY" > ~/.ssh/id_rsa
chmod 600 ~/.ssh/id_rsa

eval `ssh-agent`
ssh-add ~/.ssh/id_rsa
