# gem5 hello word using stdlib
# Ref: https://www.gem5.org/documentation/gem5-stdlib/hello-world-tutorial

# Resolved warnings with following issues:
# https://www.mail-archive.com/gem5-dev@gem5.org/msg42815.html
# https://www.mail-archive.com/gem5-users@gem5.org/msg21671.html
    
from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
from gem5.isas import ISA

# Obtain the components.
cache_hierarchy = NoCache()
memory = SingleChannelDDR3_1600("8GiB")
processor = SimpleProcessor(cpu_type=CPUTypes.ATOMIC, num_cores=1, isa=ISA.RISCV)

#Add them to the board.
board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)
  
# Set the workload.
binary = obtain_resource("riscv-hello")
board.set_se_binary_workload(binary)  

# Setup the Simulator and run the simulation.
simulator = Simulator(board=board)
simulator.run()
