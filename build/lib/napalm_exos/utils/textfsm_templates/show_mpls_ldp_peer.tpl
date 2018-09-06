Value Required ip_addr (\S+)
Value peer (\S+)
Value state (\S+)
Value uptime (\S+)
Value adjacencies (\d+)


Start
  ^IP Address.*
  ^${ip_addr}\s+${peer}\s+${state}\s+${uptime}\s+${adjacencies} -> Record
