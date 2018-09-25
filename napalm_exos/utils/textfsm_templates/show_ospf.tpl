Value ospf_enabled (\S+)
Value mpls_as_nexthop (\S+)
Value router_id (\S+)
Value router_id_selection (\S+)

Start
  ^OSPF\s+:\s+${ospf_enabled}\s+MPLS LSP as Next-Hop:\s+${mpls_as_nexthop}
  ^RouterId\s+:\s+${router_id}\s+RouterId Selection\s+:\s+${router_id_selection} -> Record