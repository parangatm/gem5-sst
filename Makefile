SST_VERSION=SST-13.1.0 # Name of the .pc file in lib/pkgconfig where SST is installed
GEM5_LIB=gem5_opt
ARCH=RISCV
OFLAG=3

LDFLAGS=-shared -fno-common ${shell pkg-config ${SST_VERSION} --libs} -L../../build/${ARCH}/ -Wl,-rpath ../../build/${ARCH}

CXXFLAGS=-std=c++17 -g -O${OFLAG} -fPIC ${shell pkg-config ${SST_VERSION} --cflags} ${shell python3-config --includes} -I../../build/${ARCH}/ -I../../ext/pybind11/include/ -I../../build/softfloat/ -I../../ext -I${SST_ELEMENTS_HOME}/include/

CPPFLAGS+=-MMD -MP
SRC=$(wildcard *.cc)

.PHONY: clean all

all: libgem5.so

libgem5.so: $(SRC:%.cc=%.o)
    ${CXX} ${CPPFLAGS} ${LDFLAGS} $? -o $@ -l${GEM5_LIB}
-include $(SRC:%.cc=%.d)

clean:
    ${RM} *.[do] libgem5.so
