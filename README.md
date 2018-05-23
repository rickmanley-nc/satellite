# Deploy and Configure Satellite 6.3
This repo is dedicated to building a Satellite 6.3 VM on LibVirt KVM through a series of Ansible playbooks. If you've used the previous Operations repo, consider that version 1.0. This is version 2.0, and is much more user-friendly. The original intent was to just learn how to use Ansible effectively while also needing to have a reliable Satellite 6 environment that was "rinse and repeat". This is something that I can use to demonstrate on my local laptop regardless of internet connectivity.

I cannot take all the credit. I've learned from many folks within Red Hat and Ansible as well as our customers, and users in the community. Thank you all!


After kicking off the playbook (on a decent wifi connection, this will take just under 3 hours consistently), and running through the manual steps listed in section "Remaining Items to Complete", the following Demo, Enablement Session, or Workshop is ready to be delivered:

 - General Layout and Overview (I have this listed for those first/initial walkthroughs with customers)
 - Provisioning (against LibVirt)
 - Patching (Promotion, Publishing, Apply Errata, Remote Execution)
 - Content Views and Composite Content Views
 - Content View filters for EPEL7
 - Red Hat Insights
 - OpenSCAP scanning and reporting against a Standard Policy system and a STIG policy
 - More to come... File Repos, IdM integration, Ansible Tower integration, ...


## Requirements and Steps

- Configure laptop with appropriate 'httpd', 'libvirtd', and 'create-libvirt-network' roles from the following repo: https://github.com/rickmanley-nc/laptop-configure
- Create an Activation Key (from https://access.redhat.com/management/activation_keys) and add at least 1 Satellite subscription to it. Call the Activation Key "ak-satellite"
- Create a Subscription Allocation (from https://access.redhat.com/management/subscription_allocations) and at least 1 Red Hat Enterprise Linux (and hopefully EAP) subscription to it.
  - Download the Subscription Manifest, via the Export Manifest button, and rename it to 'manifest-USERNAME-sales-6.3.zip', where 'USERNAME' is your username
    - Copy the manifest to /var/www/html
    - Run 'restorecon' against /var/www/html
- Update `group_vars/all` with your desired variables
- Execute the following command to fully deploy and configure Satellite on your laptop:
  - ***testing*** `wget -qO- https://github.com/rickmanley-nc/satellite/raw/master/run.sh | bash`

## Gotchas!

I'll keep this updated with current gotchas that you'll have to be mindful of before having a successful deploy.

- Once you have your manifest, you'll need to verify which subscriptions are attached to the activation keys in `roles/activation-keys/tasks/main.yml`. We're using hammer output to search for the RHEL Server Premium and EPEL subscriptions. This can be restructured to search for any other subscriptions by changing the '--search' argument.

- Using the 'wget' method with run.sh doesn't work completely yet due to missing 'become' arguments. You can execute the playbook as 'root' user and it will work as expected. I'm currently working through adding the necessary 'become' arguments.

- If the playbook fails, it is not idempotent yet. You will likely need to delete the deployed VM and kick of the playbook again. Some of this is due to improper tagging, some because there's not a 'hammer' module, and some due to not having the correct conditionals. The 'check-for-existing-satellite' role is not used as effectively as it could, and that's something I'm currently working on.


## Roles

- check-for-existing-satellite
- hostname
- firewall
- etc-hosts
- register
- install-satellite
- manifest
- sync-plan
- lazy-sync
- lifecycle-environments
- product-repo-RHEL7
- product-repo-EPEL7
- ccv-RHEL7-EPEL7
- product-repo-EAP7
- ccv-RHEL7-EAP7
- activation-keys
- provision-libvirt
- ansible-tower-sync-prep (not used yet)

## Vars

All variables are located in `group_vars/all`. Update that file with your environment details.

## Tags


## Remaining Items to Complete

- Breakout list of subscriptions used for this environment. (RHEL Server, Gluster, JBoss EAP)
- Fix LAB activation key (currently doesn't have EAP subscription)
- Enable setup through wget of run.sh, similar to tower repo.
- Go goferless: https://access.redhat.com/articles/3154811
- Enable remote execution
- update kickstart template with laptop_local_user and ssh key
- Redo Tag taxonomy and make tag notes in the 'Tags' section above.
- Make role notes
- Make use of 'check-for-existing-satellite' tag. Currently it is not utilized and running the playbook will perform actions when we don't want them to.
- Need to manually update Remote Execution on subnet. Hammer commands do not currently exist and there is no API: https://bugzilla.redhat.com/show_bug.cgi?id=1370460, http://projects.theforeman.org/issues/15249, http://projects.theforeman.org/issues/21231
- Need to manually update Compute Profiles to point to correct libvirt network, and storage point for VM disk. Hammer commands do not currently exist, and there is no API: https://projects.theforeman.org/issues/6344
- Need to manually create OpenSCAP policy AFTER hostgroup is created. Create both Standard with tailoring file and STIG build... likely remove some requirements from STIG that require 3rd party applications to be installed.
- Break OpenSCAP out into its own role, including uploading the tailoring files. https://github.com/Ansible-Security-Compliance
- Copy existing partition templates and make a role for STIG builds. After importing template, will need to run the following command to add OS version: # hammer partition-table add-operatingsystem --name "Kickstart default - STIG" --operatingsystem "RedHat 7.4"
- Need to enable ansible-tower-sync-prep role with users locked to lifecycle environments.

## License

Red Hat, the Shadowman logo, Ansible, and Ansible Tower are trademarks or registered trademarks of Red Hat, Inc. or its subsidiaries in the United States and other countries.

All other parts of this project are made available under the terms of the [MIT License](LICENSE).
