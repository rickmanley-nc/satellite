# Deploy and Configure Satellite 6.3
This repo is dedicated to building Satellite 6.3 on a VM on LibVirt KVM. After deploying, and running through some of the manual steps listed in "Status of Remaining Items to Complete", the following demo is ready to be done:

 - General Layout and Overview (I had to list this for those first/initial walkthroughs)
 - Provisioning
 - Patching
 - Content Views and Composite Content Views
 - Content View filters for EPEL
 - Red Hat Insights
 - OpenSCAP scanning and reporting against a Standard Policy system and a STIG system
 - More to come...

## Requirements and Steps

- Create host-level network, 192.168.126.x on LibVirt
- Build Gold Image
  - Create VM: 4 vCPU, 12228 MB RAM, 125 GB Storage, RHEL 7.3 - place on sat-isolated network with the following static ip info:
  - Configure static networking as
    - IP -  192.168.126.2
    - Netmask - 255.255.255.0
    - Gateway - 192.168.126.1
    - DNS - 192.168.126.1 (note: this is temporary. After we install Satellite, we'll change this to the IP of the Satellite as it will be running DNS)
  - Ensure partition layout has just "/" at 120.8 GiB, "swap" at 4096 MiB, and "/boot" at 200 MiB
  - Clone vm as gold image.
- Update group_vars/all

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

-

## Status of Remaining Items to Complete

- Verify that EPEL7 filters work correctly, as well as make the filter date a variable so you can schedule this monthly in Ansible Tower
- After subnet is created from hammer, need to manually add remote execution capsule under the web UI for subnet. Not listed in hammer, is there a way to use API call to add this?
- Need to manually update Compute Profiles to point to correct libvirt network, and storage point for VM disk. Hammer commands do not currently exist, https://projects.theforeman.org/issues/6344
- Need to inherit puppet environment to location before host group creation.
- Need to manually create hostgroups, medium not found during hammer execution
- Need to manually create OpenSCAP policy after hostgroup is created. Create both Standard with tailoring file and STIG build
- Break OpenSCAP out into its own role. Include uploading the tailoring files. https://github.com/Ansible-Security-Compliance
- Copy existing partition templates and make a role for STIG builds. After importing template, will need to run the following command to add OS version: # hammer partition-table add-operatingsystem --name "Kickstart default - STIG" --operatingsystem "RedHat 7.4"
- Need to enable ansible-tower-sync-prep role with users locked to lifecycle environments.
- Make use of 'check-for-existing-satellite' tag. Currently it is not utilized and running the playbook will perform actions when we don't want them to.
- Make tag notes
- Make role notes
- Update create network notes with libvirt network playbook from operations
- Update Gold Image Build with proper partition layout

## License

Red Hat, the Shadowman logo, Ansible, and Ansible Tower are trademarks or registered trademarks of Red Hat, Inc. or its subsidiaries in the United States and other countries.

All other parts of this project are made available under the terms of the [MIT License](LICENSE).
