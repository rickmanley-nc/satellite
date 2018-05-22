cd /home/rnelson/git
git clone git@github.com:rickmanley-nc/satellite.git
cd satellite

ansible-playbook -i hosts --ask-become-pass deploy.yml
ansible-playbook -i hosts2 -u ansible --ask-become-pass --ask-vault-pass main.yml -k

source ~/.bashrc
exit 0

# wget -qO- https://github.com/rickmanley-nc/satellite/raw/master/run.sh | bash
