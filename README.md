# Deploy and Configure Satellite 6.3
This repo is dedicated to building a Satellite 6.3 VM on LibVirt KVM through a series of Ansible playbooks. If you've used the previous Operations repo, consider that version 1.0. This is version 2.0, and is much more user-friendly. The original intent was to just learn how to use Ansible effectively while also needing to have a reliable Satellite 6 environment that was "rinse and repeat". This is something that I can use to demonstrate on my local laptop regardless of internet connectivity.

I cannot take all the credit. I've learned from many folks within Red Hat and Ansible as well as our customers, and users in the community. Thank you all!


After kicking off the playbook (on a decent wifi connection, this will take just under 3 hours consistently, 3.5 hours if with IdM integration), and running through the manual steps listed in section "Remaining Items to Complete", the following Demo, Enablement Session, or Workshop is ready to be delivered:

 - General Layout and Overview (I have this listed for those first/initial walkthroughs with customers)
 - Provisioning (against LibVirt)
 - Patching (Promotion, Publishing, Apply Errata, Remote Execution)
 - Content Views and Composite Content Views
 - Content View filters for EPEL7
 - Red Hat Insights
 - OpenSCAP scanning and reporting against a Standard Policy system and a STIG policy
 - When installed with IdM integration... RBAC,
 - More to come... Ansible Tower integration, Gluster integration, OpenShift integration


## Requirements and Steps

- Configure laptop with appropriate `httpd`, `libvirtd`, and `create-libvirt-network` roles from the following repo: https://github.com/rickmanley-nc/laptop-configure
  - OPTIONAL - Deploy IdM server from https://github.com/rickmanley-nc/laptop-configure
- Create an Activation Key (from https://access.redhat.com/management/activation_keys) and add at least 1 Satellite subscription to it. Call the Activation Key "ak-satellite"
- Create a Subscription Allocation (from https://access.redhat.com/management/subscription_allocations) and at least 1 Red Hat Enterprise Linux (and hopefully EAP) subscription to it.
  - Download the Subscription Manifest, via the Export Manifest button, and rename it to 'manifest-USERNAME-6.3.zip', where 'USERNAME' is your username
    - Copy the manifest to /var/www/html
    - Run 'restorecon' against /var/www/html
- Update `group_vars/all`
- Execute the following command to fully deploy and configure Satellite on your laptop:
  - `wget -qO- https://github.com/rickmanley-nc/satellite/raw/master/run.sh | bash`
- Execute the following command to fully deploy and configure Satellite with integration to an existing IdM server on your laptop:
  - `wget -qO- https://github.com/rickmanley-nc/satellite/raw/master/run-idm-integrated.sh | bash`

## Gotchas!

I'll keep this updated with current gotchas that you'll have to be mindful of before having a successful deploy.

- Once you have your manifest, you'll need to verify which subscriptions are attached to the activation keys in `roles/activation-keys/tasks/main.yml`. We're using hammer output to search for the RHEL Server Premium and EPEL subscriptions. This can be restructured to search for any other subscriptions by changing the '--search' argument.

- If the playbook fails, it is not idempotent yet. You will likely need to delete the deployed VM and kick of the playbook again. Some of this is due to improper tagging, some because there's not a 'hammer' module, and some due to not having the correct conditionals. The 'check-for-existing-satellite' role is not used as effectively as it could, and that's something I'm currently working on.


## Roles

- check-for-existing-satellite
- hostname
- firewall
- etc-hosts
- register
- install-satellite
- configure-satellite
- install-satellite-idm-integrated
- configure-satellite-idm-integrated
- manifest
- domain
- openscap
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
#    - ansible-tower-sync-prep

## Vars

All variables are located in `group_vars/all`. Update that file with your environment details.

## Tags


## Remaining Items to Complete

- Breakout list of subscriptions and SKUs needed for this environment. (RHEL Server, Gluster, JBoss EAP)
- Fix LAB activation key (currently doesn't have EAP subscription)
- Go goferless: https://access.redhat.com/articles/3154811
- Enable remote execution
- Redo Tag taxonomy and make tag notes in the 'Tags' section above.
- Need to manually update Remote Execution on subnet. Hammer commands do not currently exist and there is no API: https://bugzilla.redhat.com/show_bug.cgi?id=1370460, http://projects.theforeman.org/issues/15249, http://projects.theforeman.org/issues/21231
- Need to manually update Compute Profiles to point to correct libvirt network, and storage point for VM disk. Hammer commands do not currently exist, and there is no API: https://projects.theforeman.org/issues/6344
- Copy existing partition templates and make a role for STIG builds. After importing template, will need to run the following command to add OS version: # hammer partition-table add-operatingsystem --name "Kickstart default - STIG" --operatingsystem "RedHat 7.4"
- Need to enable ansible-tower-sync-prep role with users locked to lifecycle environments.

## License

Red Hat, the Shadowman logo, Ansible, and Ansible Tower are trademarks or registered trademarks of Red Hat, Inc. or its subsidiaries in the United States and other countries.

All other parts of this project are made available under the terms of the [MIT License](LICENSE).
