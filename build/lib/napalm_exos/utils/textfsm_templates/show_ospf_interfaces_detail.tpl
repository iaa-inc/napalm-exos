Value Required vlan (\S+)
Value ospf_enabled (\S+)
Value area_id (\S+)
Value router_id (\S+)
Value link_type (\S+)
Value passive (\S+)
Value cost (\S+)
Value priority (\d+)
Value state (\S+)
Value bfd_protection (\S+)

Start
  ^Interface.*Vlan:\s+${vlan}\s+OSPF:\s+${ospf_enabled}
  ^AreaId:\s+${area_id}\s+RtId:\s+${router_id}\s+Link Type:\s+${link_type}\s+Passive:\s+${passive}
  ^Cost:\s+${cost}\s+Priority:\s+${priority}
  ^State:\s+${state}
  ^BFD\s+Protection:\s+${bfd_protection} -> Record