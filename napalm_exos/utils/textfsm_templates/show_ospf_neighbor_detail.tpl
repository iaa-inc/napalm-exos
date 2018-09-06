Value Required neighbor (\S+)
Value interface_addr (\S+)
Value area_id (\S+)
Value vlan (\S+)
Value priority (\S+)
Value state (\S+)
Value uptime (\S+)
Value bfd_status (\S+)

Start
  ^ Neighbor ${neighbor}, interface address ${interface_addr}
  ^    In the area ${area_id} via interface ${vlan}
  ^    Neighbor priority is ${priority},\s+State is ${state},
  ^    Neighbor is up for ${uptime}
  ^    BFD Session State: ${bfd_status} -> Record