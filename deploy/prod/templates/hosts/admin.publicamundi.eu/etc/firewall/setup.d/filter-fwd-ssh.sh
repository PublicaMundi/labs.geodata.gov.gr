#!/bin/bash

# Filter SSH break-in attempts to internal hosts 

{% for host in groups["internal"] -%}
{%- set dport = hostvars[host].networking.nat.ssh.external_port| int -%}
{%- if dport %}
# Filter traffic to {{dport}} for host {{host}}
iptables -A FORWARD -i ${public_ip4_iface} -p tcp -m tcp \
  --dport '{{dport}}' -m state --state NEW -m recent --set --name 'SSH_FWD_{{dport}}' --rsource 
iptables -A FORWARD -i ${public_ip4_iface} -p tcp -m tcp \
  --dport '{{dport}}' -m state --state NEW -m recent --update --seconds 60 --hitcount 8 --name 'SSH_FWD_{{dport}}' --rsource -j REJECT
{% endif %} 
{% endfor %}

