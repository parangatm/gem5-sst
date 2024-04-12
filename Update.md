Setting up gem5 and DRAMSim compatible with an SST installation

### Installation

#### Install SST Core
Version: 13.1.0

**Prerequisite** - Install OpenMPI first

Add to PATH
```Shell
export MPIHOME=/usr/local/bin/OpenMPI-4.1.4
export PATH=$MPIHOME/bin:$PATH
export MPICC=mpicc
export MPICXX=mpicxx

export LD_LIBRARY_PATH=$MPIHOME/lib:$LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=$MPIHOME/lib:$DYLD_LIBRARY_PATH
export MANPATH=$MPIHOME/share/man:$DYLD_LIBRARY_PATH
```

Then install SST Core as per https://sst-simulator.org/SSTPages/SSTBuildAndInstall_13dot1dot0_SeriesQuickStart/

Add to PATH
```Shell
export SST_CORE_HOME=/usr/local/sstcore-13.1.0
export PATH=$SST_CORE_HOME/bin:$PATH
```

#### Install DRAMSim2

Following Adding External Component DRAMSim2 as per this guide - 

https://sst-simulator.org/SSTPages/SSTBuildAndInstall_13dot0dot0_SeriesAdditionalExternalComponents/#:~:text=to%20be%20built.-,DRAMSim2%202.2.2,-OPTIONAL%20EXTERNAL%20COMPONENT

Add to PATH
`export DRAMSIM2_HOME=/usr/local/DRAMSim2`

#### Install SST Elements
Version: 13.1.0

Follow the steps as per https://sst-simulator.org/SSTPages/SSTBuildAndInstall_13dot1dot0_SeriesQuickStart/

Modify the installation step as follows - 

`./configure --prefix=$SST_ELEMENTS_HOME --with-sst-core=$SST_CORE_HOME --with-dramsim=$DRAMSIM2_HOME`

Add to PATH
```Shell
export SST_ELEMENTS_HOME=/usr/local/sstelements-13.1.0
export PATH=$SST_ELEMENTS_HOME/bin:$PATH
```

#### Install gem5
Version: 23.0.1.0

Install as per the following instructions, but for the specified version - 

https://www.gem5.org/documentation/general_docs/building

### Compilation

#### Building gem5
`scons build/RISCV/gem5.opt -j8`

#### Compile gem5 as library for SST
`scons build/RISCV/libgem5_opt.so -j8 --without-tcmalloc --duplicate-sources`

**Note:**
- `--without-tcmalloc` is required to avoid a conflict with SST's malloc.
- `--duplicate-sources` is required as the compilation of SST depends on sources to be present in the "build" directory.

#### Compiling the SST integration inside gem5/ext/sst

Ensure that `PKG_CONFIG_PATH` is updated with sst-core path
`export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/sstcore-13.1.0/lib/pkgconfig`

Modify the Makefile as follows:
- SST_VERSION=SST-13.1.0
- ARCH=RISCV
- `CXXFLAGS=.... -I{SST_ELEMENTS_HOME}/include/`

`make`

### Running the Simulation

**On SST**:

In `gem5_helloworld.py` make sure last three lines are commented from `m5.instantiate()` onwards

`sst --add-lib-path=./ sst_helloworld.py`

**On gem5**: (for correlation)

In `gem5_helloworld.py` uncomment last three lines from `m5.instantiate()`

`build/X86/gem5.opt gem5_helloworld.py`
