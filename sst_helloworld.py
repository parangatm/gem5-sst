import sst
import sys
import os

cache_link_latency = "1ps"
cpu_clock_rate = "3GHz"
memory_size_gem5 = "4GiB"
memory_size_sst = "6GiB"
addr_range_end = sst.UnitAlgebra(memory_size_sst).getRoundedValue()

# adding a gem5 cpu to the sst
# from gem5.cc, three params and two ports are required for a gem5component
# params : frequency, cmd, debug_flags
# ports: systemPort, cachePort
gem5_node = sst.Component("gem5_node", "gem5.gem5Component")
cpu_params = {
    "frequency": cpu_clock_rate,
    "cmd": "../../work/tutorial/stdlib_helloworld.py",
    "debug_flags": ""
}
gem5_node.addParams(cpu_params)

# systemPort on gem5Component
system_port = gem5_node.setSubComponent("system_port", "gem5.gem5Bridge", 0) # for initialization
system_port.addParams({ "response_receiver_name": "system.system_outgoing_bridge"}) # tell the SubComponent the name of the corresponding SimObject  

# cachePort on gem5Component
cache_port = gem5_node.setSubComponent("cache_port", "gem5.gem5Bridge", 0) # SST -> gem5
cache_port.addParams({ "response_receiver_name": "system.memory_outgoing_bridge"})

# L1 cache
l1_cache = sst.Component("l1_cache", "memHierarchy.Cache")
l1_params = {
    "access_latency_cycles" : "1",
    "cache_frequency" : cpu_clock_rate,
    "replacement_policy" : "lru",
    "coherence_protocol" : "MESI",
    "associativity" : "4",
    "cache_line_size" : "64",
    "cache_size" : "4 KiB",
    "L1" : "1",
}

l1_cache.addParams(l1_params)

# Memory
memctrl = sst.Component("memory", "memHierarchy.MemController")
memctrl.addParams({
    "debug" : "0",
    "clock" : "1GHz",
    "request_width" : "64",
    "addr_range_end" : addr_range_end, # should be changed accordingly to memory_size_sst
})

memory = memctrl.setSubComponent("backend", "memHierarchy.simpleMem")
memory.addParams({
    "access_time" : "30ns",
    "mem_size" : memory_size_sst
})
  
cache_bus = sst.Component("cache_bus", "memHierarchy.Bus")
cache_bus.addParams( { "bus_frequency" : cpu_clock_rate } )

# Connections
# cpu <-> L1
cpu_cache_link = sst.Link("cpu_l1_cache_link")
cpu_cache_link.connect(
    (cache_port, "port", cache_link_latency),
    (cache_bus, "high_network_0", cache_link_latency)
)

system_cache_link = sst.Link("system_cache_link")
system_cache_link.connect(
    (system_port, "port", cache_link_latency),
    (cache_bus, "high_network_1", cache_link_latency)
)

cache_bus_cache_link = sst.Link("cache_bus_cache_link")
cache_bus_cache_link.connect(
    (cache_bus, "low_network_0", cache_link_latency),
    (l1_cache, "high_network_0", cache_link_latency)
)

# L1 <-> mem
cache_mem_link = sst.Link("l1_cache_mem_link")
cache_mem_link.connect(
    (l1_cache, "low_network_0", cache_link_latency),
    (memctrl, "direct_link", cache_link_latency)
)

# enable Statistics
stat_params = { "rate" : "0ns" }
sst.setStatisticLoadLevel(5)
sst.setStatisticOutput("sst.statOutputTXT", {"filepath" : "./sst-stats.txt"})
sst.enableAllStatisticsForComponentName("l1_cache", stat_params)
sst.enableAllStatisticsForComponentName("memory", stat_params)
