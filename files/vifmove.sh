#!/bin/bash
# usage ~/vifmove.sh <virsh_domain_name/id> <interface_name> <new_source_network_name>
tmpxml=$(mktemp /tmp/ifcfg.XXX)
macaddr="$(virsh domiflist $1 | awk "/$2\s/ {print \$NF}")"
cat > "$tmpxml" <<EOF
<interface type='network'>
  <mac address='$macaddr'/>
  <source network='$3'/>
  <model type='rtl8139'/>
  <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
</interface>
EOF
virsh update-device "$1" "$tmpxml"
rm "$tmpxml"
