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

Start
  ^L2VPN Name:\s+${name} 
  ^\s+VPN ID\s+:\s+${vpn_id}\s+Admin State\s+:\s+${admin_state}
  ^\s+Source Address\s+:\s+${source_address}\s+Oper State\s+:\s+${oper_state}
  ^\s+VCCV Status\s+:\s+${vccv_status}\s+MTU\s+:\s+${mtu}
  ^\s+VCCV Interval Time\s+:\s+${vccv_interval_time}\s+sec.\s+Ethertype\s+:\s+${ethertype}
  ^\s+VCCV Fault Multiplier\s+:\s+${vccv_fault_multiplier}\s+.1q tag\s+:\s+${tag}
  ^\s+L2VPN Type\s+:\s+${l2vpn_type}\s+Redundancy\s+:\s+${redundancy}
  ^\s+Service Interface\s+:\s+${service_interface}
  ^\s+Created By\s+: ${created_by} -> Record

