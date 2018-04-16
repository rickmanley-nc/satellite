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

- Create host-level network on Laptop, 192.168.126.x on LibVirt - Easy with the 'libvirtd' role and the 'create-libvirt-network' role within my Laptop-Configure repo: https://github.com/rickmanley-nc/laptop-configure
- Build Gold Image (This needs an overhaul, but it currently works and is not urgent)
  - Create VM: 4 vCPU, 12228 MB RAM, 125 GB Storage, RHEL 7.3 - place on sat-isolated network with the following static ip info:
  - Configure static networking as
    - IP -  192.168.126.2
    - Netmask - 255.255.255.0
    - Gateway - 192.168.126.1
    - DNS - 192.168.126.1 (note: this is temporary. After we install Satellite, we'll change this to the IP of the Satellite as it will be running DNS)
  - Ensure partition layout has just "/" at 120.8 GiB, "swap" at 4096 MiB, and "/boot" at 200 MiB.
  - Clone vm as gold image.
- Create an Activation Key (from https://access.redhat.com/management/activation_keys) and add at least 1 Satellite subscription to it. Call the Activation Key "satellite"
- Create a Subscription Allocation (from https://access.redhat.com/management/subscription_allocations) and at at least 1 Red Hat Enterprise Linux (and hopefully EAP) subscription to it.
  - Download the Subscription Manifest, via the Export Manifest button, and rename it to 'manifest-USERNAME-sales-6.3.zip', where 'USERNAME' is your username
    - Copy the manifest to /var/www/html
- Update group_vars/all

## Gotchas!

I'll keep this updated with current gotchas that you'll have to be mindful of before having a successful deploy.

- Within group_vars/all, both development_subscription_ids and lab_subscription_ids are dependent on your manifest. I have several different subscriptions on my test account, and the ordering of them is not logical. Currently the 'hammer' tool has to connect through a numerical Subscription ID. This is something that could be done by querying 'hammer subscription list' and filtering on specific subscription names to then store the Sub ID. I haven't gotten to this yet, but it's doable.

- There are 3 different scenarios for installing Satellite. I have this hard coded for Scenario 3 (install with DHCP, TFTP, and DNS). The other scenarios have not been tested.

- If the playbook fails, it is not idempotent yet. You will likely need to redeploy from the Gold Image and kick of the playbook again. Some of this is due to improper tagging, some because there's not a 'hammer' module, and some due to not having the correct conditionals. The 'check-for-existing-satellite' role is not used as effectively as it could, and that's something I'm currently working on.


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
- ansible-tower-sync-prep

## Vars

All variables are located in `group_vars/all`. Update that file with your environment details.

## Tags


## Remaining Items to Complete

- Redo Tag taxonomy and make tag notes in the 'Tags' section above.
- Verify that EPEL7 filters work correctly, as well as make the filter date a variable so you can schedule this monthly in Ansible Tower!
- After subnet is created from hammer, need to manually add remote execution capsule under the web UI for subnet. Not listed in hammer, is there a way to use API call to add this?
- Need to manually update Compute Profiles to point to correct libvirt network, and storage point for VM disk. Hammer commands do not currently exist, https://projects.theforeman.org/issues/6344
- Need to inherit puppet environment to location before host group creation.
- Need to manually create hostgroups, medium not found during hammer execution. Looks like an easy fix, but the formatting changed from 6.2 to 6.3. Just need to determine new path.
- Need to manually create OpenSCAP policy AFTER hostgroup is created. Create both Standard with tailoring file and STIG build... likely remove some requirements from STIG that require 3rd party applications to be installed.
- Break OpenSCAP out into its own role, including uploading the tailoring files. https://github.com/Ansible-Security-Compliance
- Copy existing partition templates and make a role for STIG builds. After importing template, will need to run the following command to add OS version: # hammer partition-table add-operatingsystem --name "Kickstart default - STIG" --operatingsystem "RedHat 7.4"
- Need to enable ansible-tower-sync-prep role with users locked to lifecycle environments.
- Make use of 'check-for-existing-satellite' tag. Currently it is not utilized and running the playbook will perform actions when we don't want them to.
- Make role notes
- Update Gold Image Build with proper partition layout... or preferably have a separate ansible role with variables for CPU, RAM, and Network settings to then build from ISO? This has been done in other projects, but not sure the best path here.

## License

Red Hat, the Shadowman logo, Ansible, and Ansible Tower are trademarks or registered trademarks of Red Hat, Inc. or its subsidiaries in the United States and other countries.

All other parts of this project are made available under the terms of the [MIT License](LICENSE).
