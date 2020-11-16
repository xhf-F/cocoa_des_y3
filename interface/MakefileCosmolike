CC = $(C_COMPILER)
CXX = $(CXX_COMPILER)

# LINK ARMADILLO LIBRARY
ARMA := 1 

# LINK GSL LIBRARY
GSL   := 1

# LINK FFTW
FFTW := 1

# LINK FMT
#FMT := 1

# LINK SPDLOG
SPDLOG := 1

# LINK INTEL THREAD BUILDING BLOCKS
#TBB := 1

# LINK NAG LIBRARY
#NAG := 1

# LINK C LOG LIBRARY
CLOG :=1

# LINK PYBIND LIBRARY
PYBIND := 1

# DEFINE TEST CODE
TEST := 1

CSOURCES = 
OBJECTC = 
CFLAGS =  -std=c99 -I ${ROOTDIR}/include/ 
CXXFLAGS = -std=c++14 -I ${ROOTDIR}/include/ 
LDFLAGS = -L ${ROOTDIR}/lib

ifdef COSMOLIKE_DEBUG_MODE
	COMMON_FLAGS += -O0  -DDEBUG -W -Wall -Wextra -Wcomment -pedantic -g -fmax-errors=1 -Wno-unknown-pragmas
else
	ifdef OCELOTE_MAKEFILE_COSMOLIKE_FLAGS
		COMMON_FLAGS += -foptimize-strlen -finline-functions-called-once -fmerge-all-constants -Wno-unused-result -Wno-format-overflow -fmax-errors=1 -fthread-jumps -fcse-follow-jumps -fsplit-wide-types -fcse-skip-blocks -faggressive-loop-optimizations -fif-conversion -fif-conversion2 -fexpensive-optimizations -free -fschedule-insns -fschedule-insns2 -fsched-spec-load-dangerous -fshrink-wrap -fcaller-saves -fcombine-stack-adjustments -fipa-ra -ftree-reassoc -ftree-partial-pre -ftree-forwprop -ftree-fre -ftree-phiprop -fhoist-adjacent-loads -ftree-copy-prop -fipa-pure-const -fipa-reference -fipa-pta -fipa-profile -fipa-cp -fipa-cp-clone -fipa-icf -ftree-loop-distribution -ftree-loop-if-convert -ftree-loop-distribute-patterns -ftree-scev-cprop -ftree-parallelize-loops=4 -ftree-pta -ftree-sra -ftree-loop-vectorize -fpartial-inlining -fpredictive-commoning -fpeephole2 -fguess-branch-probability -freorder-blocks-algorithm=stc -freorder-blocks-and-partition -freorder-functions -falign-functions -falign-loops -falign-jumps -flto -fcprop-registers -funsafe-math-optimizations -fassociative-math -freciprocal-math -ffinite-math-only -fno-signed-zeros -fvpt -funroll-loops -fschedule-fusion -fpeel-loops -fmove-loop-invariants -fexcess-precision=fast -fgcse-after-reload -ftree-slp-vectorize -foptimize-sibling-calls -ffast-math -fvect-cost-model=dynamic -fvect-cost-model -funswitch-loops -ffp-contract=fast -fivopts -fopenmp
		CXXFLAGS += -O3 -ffast-math
	else
	CFLAGS += -O0
		COMMON_FLAGS += -foptimize-strlen -finline-functions-called-once -fmerge-all-constants -Wno-unused-result -Wno-format-overflow -fmax-errors=1 -fthread-jumps -fcse-follow-jumps -fsplit-wide-types -fcse-skip-blocks -faggressive-loop-optimizations -fif-conversion -fif-conversion2 -fexpensive-optimizations -free -fschedule-insns -fschedule-insns2 -fsched-spec-load-dangerous -fshrink-wrap -fcaller-saves -fcombine-stack-adjustments -fipa-ra -ftree-reassoc -fcode-hoisting -ftree-partial-pre -ftree-forwprop -ftree-fre -ftree-phiprop -fhoist-adjacent-loads -ftree-copy-prop -fipa-pure-const -fipa-reference -fipa-reference-addressable -fipa-stack-alignment -fipa-pta -fipa-profile -fipa-cp -fipa-cp-clone -fipa-icf -floop-nest-optimize -floop-parallelize-all -ftree-loop-distribution -ftree-loop-if-convert -ftree-loop-distribute-patterns -floop-interchange -ftree-scev-cprop -ftree-parallelize-loops=4 -ftree-pta -ftree-sra -ftree-loop-vectorize -fpartial-inlining -fpredictive-commoning -fpeephole2 -fguess-branch-probability -freorder-blocks-algorithm=stc -freorder-blocks-and-partition -freorder-functions -falign-functions -falign-loops -falign-jumps -flto -fcprop-registers -funsafe-math-optimizations -fassociative-math -freciprocal-math -ffinite-math-only -fno-signed-zeros -fvpt -funroll-loops -fschedule-fusion -fpeel-loops -fmove-loop-invariants -fexcess-precision=fast -fgcse-after-reload -floop-unroll-and-jam -fsplit-loops -ftree-slp-vectorize -foptimize-sibling-calls -ffast-math -fvect-cost-model=dynamic -fvect-cost-model -funswitch-loops -ffp-contract=fast -march=native -fivopts -fopenmp
		CXXFLAGS += -O3 -ffast-math
	endif
endif

ifdef IGNORE_CPP_SPDLOG_INSTALLATION
	COMMON_FLAGS += -I ${GLOBAL_PACKAGES_INCLUDE}
endif

ifdef ARMA	
	CXXFLAGS += -DARMA
	LDFLAGS += -llapack
endif

ifdef GSL
	COMMON_FLAGS += -DHAVE_INLINE -DGSLLIB
	ifdef IGNORE_C_GSL_INSTALLATION
		COMMON_FLAGS += -I ${GLOBAL_PACKAGES_INCLUDE}
		LDFLAGS += -L ${GLOBAL_PACKAGES_LOCATION}/lib
	endif
	LDFLAGS += -lgsl -lgslcblas
endif

ifdef FMT
	LDFLAGS += -lfmt
endif

ifdef FFTW
	ifdef IGNORE_C_FFTW_INSTALLATION
		COMMON_FLAGS += -I ${GLOBAL_PACKAGES_INCLUDE}
		LDFLAGS += -L ${GLOBAL_PACKAGES_LOCATION}/lib
	endif
	LDFLAGS += -lfftw3
endif 

ifdef NAG
	COMMON_FLAGS += -I ${NAG_INC} -DNAGLIB
	LDFLAGS += ${NAG_LIB}/libnagc_mkl.so -lpthread
endif 

ifdef TBB
	COMMON_FLAGS += -DTBB
	LDFLAGS += -ltbb -ltbbmalloc
endif

ifdef CLOG
	COMMON_FLAGS += -DLOG_USE_COLOR
	CSOURCES += ../log.c/src/log.c
	OBJECTC += log.o
endif

ifdef SPDLOG
	ifndef IGNORE_CPP_SPDLOG_INSTALLATION
		LDFLAGS += ${ROOTDIR}/lib/libspdlog.a
	endif
endif

ifdef TEST
	COMMON_FLAGS += -DTEST 
endif

CFLAGS += ${COMMON_FLAGS} 
CXXFLAGS += ${COMMON_FLAGS}

ifdef PYBIND
	CXXFLAGS += $(shell python3 -m pybind11 --includes) -DPYBIND11
	LDFLAGS += $(shell python3-config --ldflags)
endif

LDFLAGS += -lm

all:  shared
shared: interface.so

CSOURCES += \
		../cfftlog/cfftlog.c \
		../cfftlog/utils_complex.c \
		../cfftlog/utils.c \
		../cfastpt/cfastpt.c \
		../cfastpt/utils_complex_cfastpt.c \
		../cfastpt/utils_cfastpt.c \
		../theory/basics.c \
		../theory/cosmo3D.c \
		../theory/cosmo2D_fourier.c \
		../theory/cosmo2D_exact_fft.c \
		../theory/cosmo2D_fullsky_TATT.c \
		../theory/halo.c \
		../theory/recompute.c \
		../theory/redshift_spline.c \
		../theory/structs.c \
		../theory/HOD.c \
		../theory/pt_cfastpt.c \

OBJECTC += \
		./cfftlog.o \
		./utils_complex.o \
		./utils.o \
		./cfastpt.o \
		./utils_complex_cfastpt.o \
		./utils_cfastpt.o \
		./basics.o \
		./cosmo3D.o \
		./cosmo2D_exact_fft.o \
		./cosmo2D_fourier.o \
		./cosmo2D_fullsky_TATT.o \
		./halo.o \
		./recompute.o \
		./redshift_spline.o \
		./structs.o \
		./HOD.o \
		./pt_cfastpt.o \

$(OBJECTC): $(CSOURCES) 
	$(CC) $(CFLAGS) -fPIC -DCOBAYA_SAMPLER -c $(CSOURCES)  

interface.so: $(OBJECTC) $(CSOURCES) interface.cpp 
	$(CXX) $(CXXFLAGS) -DCOBAYA_SAMPLER -shared -fPIC -o $@ $(OBJECTC) interface.cpp $(LDFLAGS)
	@rm *.o

test: $(OBJECTC) $(CSOURCES) interface.cpp 
	$(CXX) $(CXXFLAGS) -DCOBAYA_SAMPLER -fPIC -o $@ $(OBJECTC) interface.cpp $(LDFLAGS)

clean:
	@rm -rf interface.so interface.so.dSYM  *.o