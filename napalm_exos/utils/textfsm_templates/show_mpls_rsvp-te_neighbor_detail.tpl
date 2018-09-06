Value Required neighbor_addr (\S+)
Value vlan (\S+)
Value num_lsps (\d+)
Value neighbor_support_hello (\S+)
Value rsvp_hello_state (\S+)
Value two_way_hello_state (\S+)
Value uptime (\S+)

Start
  ^Neighbor IP Address\s+: ${neighbor_addr}
  ^\s+Signaling Interface\s+: ${vlan}
  ^\s+Num LSPs to Neighbor\s+: ${num_lsps}
  ^\s+Neighbor supports RSVP Hello\s+: ${neighbor_support_hello}
  ^\s+RSVP Hello State\s+: ${rsvp_hello_state}
  ^\s+Two-way Hello State\s+: ${two_way_hello_state}
  ^\s+Uptime\s+: ${uptime} -> Record