Value Required,Key name (\S+)
Value vpn_id (\d+)
Value admin_state (\S+)
Value source_address (\S+)
Value oper_state (\S+)
Value mtu (\d+)
Value ethertype (\S+)
Value tag (\S+)
Value redundancy (\S+)
Value vccv_status (\S+)
Value vccv_interval_time (\d+)
Value vccv_fault_multiplier (\d+)
Value service_interface (\S+)
Value l2vpn_type (\S+)
Value created_by (\S+)
Value peer_ip (\S+)
Value pw_state ([a-zA-Z() ]+)
Value pw_index (\d+)
Value pw_signaling (\S+)
Value pw_uptime (\S+)
Value pw_installed (\S+)
Value local_pw_status ([a-zA-Z ]+)
Value remote_pw_status ([a-zA-Z ]+)
Value remote_if_mtu (\d+)
Value pw_mode (\S+)
Value transport_lsp ([a-zA-z ()]+)
Value next_hop_if (\S+)
Value next_hop_addr (\S+)
Value tx_pkts (\S+)
Value tx_label (\S+)
Value tx_bytes (\S+)
Value pw_rx_label (\S+)
Value pw_tx_label (\S+)
Value pw_rx_pkts (\S+)
Value pw_tx_pkts (\S+)
Value pw_rx_bytes (\S+)
Value pw_tx_bytes (\S+)
Value mac_limit ([a-zA-Z ]+)
Value vccv_hc_status ([a-zA-Z0-9() ]+)
Value cc_type ((\w+(\s\w+)?)|--)
Value cv_type ((\w+(\s\w+)?)|--)
Value send_next_pkt (\S+)
Value total_failures (\d+)
Value last_failure_tm (\S+)
Value total_pkts_sent (\S+)
Value total_pkts_rcvd (\S+)
Value pkts_during_last_failure (\d+)


Start
  ^L2VPN Name:\s+${name} 
  ^\s+VPN ID\s+:\s+${vpn_id}\s+Admin State\s+:\s+${admin_state}
  ^\s+Source Address\s+:\s+${source_address}\s+Oper State\s+:\s+${oper_state}
  ^\s+VCCV Status\s+:\s+${vccv_status}\s+MTU\s+:\s+${mtu}
  ^\s+VCCV Interval Time\s+:\s+${vccv_interval_time}\s+sec.\s+Ethertype\s+:\s+${ethertype}
  ^\s+VCCV Fault Multiplier\s+:\s+${vccv_fault_multiplier}\s+.1q tag\s+:\s+${tag}
  ^\s+L2VPN Type\s+:\s+${l2vpn_type}\s+Redundancy\s+:\s+${redundancy}
  ^\s+Service Interface\s+:\s+${service_interface}
  ^\s+Created By\s+: ${created_by} 
  ^\s+VPN ID\s+:\s+${vpn_id}\s+
  ^\s+Peer IP:\s+${peer_ip} 
  ^\s+PW State\s+: ${pw_state}
  ^\s+PW Index\s+: ${pw_index}
  ^\s+PW Signaling\s+: ${pw_signaling}
  ^\s+PW Uptime\s+: ${pw_uptime}
  ^\s+PW Installed\s+: ${pw_installed}
  ^\s+Local PW Status\s+: ${local_pw_status}
  ^\s+Remote PW Status\s+: ${remote_pw_status}
  ^\s+Remote I/F MTU\s+: ${remote_if_mtu}
  ^\s+PW Mode\s+: ${pw_mode}
  ^\s+Transport LSP\s+: ${transport_lsp}
  ^\s+Next Hop I/F\s+: ${next_hop_if}
  ^\s+Next Hop Addr\s+: ${next_hop_addr}\s+Tx Label\s+: ${tx_label}
  ^\s+Tx Pkts\s+: ${tx_pkts}\s+Tx Bytes\s+: ${tx_bytes}
  ^\s+PW Rx Label\s+: ${pw_rx_label}\s+PW Tx Label\s+: ${pw_tx_label}
  ^\s+PW Rx Pkts\s+: ${pw_rx_pkts}\s+PW Tx Pkts\s+: ${pw_tx_pkts}
  ^\s+PW Rx Bytes\s+: ${pw_rx_bytes}\s+PW Tx Bytes\s+: ${pw_tx_bytes}
  ^\s+MAC Limit\s+: ${mac_limit}
  ^\s+VCCV HC Status\s+: ${vccv_hc_status}
  ^\s+CC Type\s+: ${cc_type}\s+Total Pkts Sent\s+:\s+${total_pkts_sent}
  ^\s+CV Type\s+: ${cv_type}\s+Total Pkts Rcvd\s+:\s+${total_pkts_rcvd}
  ^\s+Send Next Pkt\s+: ${send_next_pkt}
  ^\s+Total Failures\s+: ${total_failures}\s+Pkts During Last Failure\s+: ${pkts_during_last_failure}
  ^\s+Last Failure Tm\s+:\s+${last_failure_tm} -> Record

