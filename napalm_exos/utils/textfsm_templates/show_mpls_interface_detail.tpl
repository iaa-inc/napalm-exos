Value Required vlan (\S+)
Value interface_addr (\S+)
Value ip_forwarding (\S+)
Value mpls_if_mtu (\d+)
Value php_status (\S+)
Value bfd_status (\S+)
Value mpls_admin_status (\S+)
Value mpls_oper_status (\S+)
Value Required rsvp_admin_status (\S+)
Value rsvp_oper_status (\S+)
Value rsvp_uptime (\S+)
Value rsvp_num_neighbors (\d+)
Value Required ldp_admin_status (\S+)
Value ldp_oper_status (\S+)
Value ldp_uptime (\S+)
Value ldp_num_adj (\d+)

Start
  ^VLAN Name\s+: ${vlan}
  ^\s+Local IP Address\s+: ${interface_addr}
  ^\s+IP Forwarding\s+: ${ip_forwarding}
  ^\s+MPLS I/F MTU\s+: ${mpls_if_mtu}
  ^\s+PHP Status\s+: ${php_status}
  ^\s+BFD Status\s+: ${bfd_status}
  ^\s+MPLS Admin Status\s+: ${mpls_admin_status}
  ^\s+MPLS Oper Status\s+: ${mpls_oper_status}
  ^\s+RSVP-TE Admin Status\s+: ${rsvp_admin_status}
  ^           Oper Status\s+: ${rsvp_oper_status}
  ^           UpTime\s+: ${rsvp_uptime}
  ^           # Neighbors\s+: ${rsvp_num_neighbors}
  ^\s+LDP Admin Status\s+: ${ldp_admin_status}
  ^       Oper Status\s+: ${ldp_oper_status}
  ^       UpTime\s+: ${ldp_uptime}
  ^       # Link Adjacencies\s+: ${ldp_num_adj} -> Record