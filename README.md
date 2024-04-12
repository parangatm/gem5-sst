04/12 - Please refer to Update.md for latest instructions

# gem5-sst
Documenting some changes to the official gem5-sst bridge to run simulations

This document highlights the steps to run the basic hello-world binary on a RISCV CPU inside a gem5 simulator, running under an SST hood. 

Testing platform: Ubuntu 22.04.3 on Windows 11 WSL-2
#### Installing gem5 
Followed: https://www.gem5.org/documentation/general_docs/building
#### Installing sst
Followed: https://sst-simulator.org/SSTPages/SSTBuildAndInstall_13dot1dot0_SeriesDetailedBuildInstructions/

Additional step: Adding build area to path (Add to ~/.bashrc or similar file)

```Shell
export MPIHOME=/usr/local/bin/OpenMPI-4.1.4
export PATH=$MPIHOME/bin:$PATH
export MPICC=mpicc
export MPICXX=mpicxx

export LD_LIBRARY_PATH=$MPIHOME/lib:$LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=$MPIHOME/lib:$DYLD_LIBRARY_PATH
export MANPATH=$MPIHOME/share/man:$DYLD_LIBRARY_PATH

export SST_CORE_HOME=/usr/local/sstcore-13.1.0
export PATH=$SST_CORE_HOME/bin:$PATH

export SST_ELEMENTS_HOME=/usr/local/sstelements-13.1.0
export PATH=$SST_ELEMENTS_HOME/bin:$PATH

export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/sstcore-13.1.0/lib/pkgconfig
```
#### Compiling gem5 as a library for sst
At the root of the gem5 folder, you need to compile gem5 as a library.

```shell
scons build/RISCV/libgem5_opt.so -j $(nproc) --without-tcmalloc --duplicate-sources
```

**Note:**
- `--without-tcmalloc` is required to avoid a conflict with SST's malloc.
- `--duplicate-sources` is required as the compilation of SST depends on sources to be present in the "build" directory.

#### Compiling the SST integration
Inside the sst directory already present in the gem5 installation
```bash
cd ext/sst
```

Ensure that `PKG_CONFIG_PATH` is updated with sst-core path
```Shell
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/sstcore-13.1.0/lib/pkgconfig
```

Modify the Makefile as follows:
- SST_VERSION=SST-13.1.0
- ARCH=RISCV
- `CXXFLAGS=.... -I{SST_ELEMENTS_HOME}/include/`

#### Running the simulation

**On SST**:
```
sst --add-lib-path=./ <config.py>
```

**On gem5**: (for correlation)

Build a gem5 system:
```
scons build/RISCV/gem5.opt -j9
```

Run the Simulation
```
build/X86/gem5.opt <gem5_config.py>
```

### Required Files

**sst_helloworld.py**

**gem5_helloworld.py**

**hello world binary** - `riscv-hello` - already available at gem5-resources
