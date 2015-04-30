#!/bin/bash

# Provide DNAT for SSH to internal hosts

{% for host in groups["internal"] -%}
{%- set dport = hostvars[host].networking.nat.ssh.external_port| int -%}
{%- if dport %}
{%- set daddr = hostvars[host].networking.if.internal_ipv4.address -%}
iptables -t nat -i ${public_ip4_iface} -A PREROUTING -j DNAT -p tcp -d ${public_ip4} --dport '{{dport}}' --to-destination '{{daddr}}:22'
{% endif %} 
{% endfor %}

