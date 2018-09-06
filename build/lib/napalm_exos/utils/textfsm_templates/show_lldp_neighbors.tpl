Value port_number (\d+:?\d+?|\d+)
Value neighbor_chassis_id (([0-9A-F]{2}[:-]){5}([0-9A-F]{2}))
Value neighbor_port_number (\d+:?\d+?|\d+)
Value ttl (\d+)
Value age (\d+)
Value neighbor_system_id (.*)

Start
  ^${port_number}\s+${neighbor_chassis_id}\s+${neighbor_port_number}\s+${ttl}\s+${age}\s+${neighbor_system_id} -> Record