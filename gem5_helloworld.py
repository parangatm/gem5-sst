import m5
import os
from m5.objects import *
from gem5.resources.resource import obtain_resource

system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

system.cpu = RiscvTimingSimpleCPU()
system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MB")]

system.membus = NoncoherentXBar(
        frontend_latency=0,
        forward_latency=0,
        response_latency=0,
        header_latency=0,
        width=64,
    )

system.cpu.icache_port = system.membus.cpu_side_ports
system.cpu.dcache_port = system.membus.cpu_side_ports
system.cpu.mmu.connectWalkerPorts(system.membus.cpu_side_ports, system.membus.cpu_side_ports)
system.cpu.createThreads()
system.cpu.createInterruptController()

system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

system.memory_outgoing_bridge = OutgoingRequestBridge()
system.memory_outgoing_bridge.port = system.membus.mem_side_ports

system.system_outgoing_bridge = OutgoingRequestBridge()
system.system_port = system.system_outgoing_bridge.port

binary = "/mnt/c/Users/paran/Code/gem5/gem5/tests/test-progs/hello/bin/riscv/linux/hello"

system.workload = SEWorkload.init_compatible(binary)
process = Process()
process.cmd = [binary]
system.cpu.workload = process

root = Root(full_system=False, system=system)
# m5.instantiate()

# print("Beginning simulation!")
# exit_event = m5.simulate()
# print("Exiting @ tick %i because %s" % (m5.curTick(), exit_event.getCause()))
