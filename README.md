# cocoa_des_y3

This repository converts the Cosmolike only implementation of DES-Y3 3x2pt analysis in real space archived on [y3_production](https://github.com/CosmoLike/y3_production) repository. Below, we will summarize the conversion of projects already implemented in Cosmolike. The relevant Files on [y3_production](https://github.com/CosmoLike/y3_production) repository are listed below

    +-- y3_production
    |    +-- like_real_y3.c
    |    +-- init_y3.c
    |    +-- zdistris
    |    |   +-- nz_lens_Y3_unblinded_10_26_20.txt
    |    |   +-- nz_source_Y3_unblinded_10_26_20.txt
    |    +-- datav
    |    |   +-- Y3_unblinded_10_26_20.txt
    |    +-- yaml
    |    |   +-- 3x2pt_baseline.mask
    |    +-- cov
    |    |   +-- cov_unblinded_11_13_20.txt
    
### Step 1: create the project name and associated repository
  Repository names should always start with the prefix `cocoa_` followed by the project's name. Given how the bash scripts that automate Cocoa tasks were written, users must follow our proposed naming convention to avoid undefined behavior.

### Step 2: create the project's repository structure

Every project must have the following structure

    +-- cocoa_des_y3
    |    +-- likelihood
    |    +-- scripts
    |    +-- data
    |    +-- interface
    |    +-- chains

We suggest the `chains` path be included in the `.gitignore` file once the folder is added and committed to the project's repository.

### Step 3: copy the data products to the `data` folder

You must include the covariance matrice, data vector, source and lens redshift distributions, and mask files. 

### Step 4: Create a dataset file on the `data` folder.

Check [DES_Y3.dataset](https://github.com/CosmoLike/cocoa_des_y3/blob/main/data/DES_Y3.dataset) as a template. 

### Step 5: Create the interface files

The files [interface.cpp](https://github.com/CosmoLike/cocoa_des_y3/blob/main/interface/interface.cpp) and [interface.hpp](https://github.com/CosmoLike/cocoa_des_y3/blob/main/interface/interface.hpp) contains our C++ refactoring of many functions implemented on files `like_real_y3.c` and `init_y3.c`.
    
The interface files also contains the following functions:

    - void cpp_init_distances(vec io_z, vec io_chi);
    - void cpp_init_growth(vec io_z, vec io_G);
    - void cpp_init_linear_power_spectrum(vec io_log10k, vec io_z, vec io_lnP);
    - void cpp_init_non_linear_power_spectrum(vec io_log10k, vec io_z, vec io_lnP);

These routines initialize the interpolation tables of functions evaluated on the Boltzmann code and needed by Cosmolike. We understand that providing the growth factor as a redshift function is redundant given the linear power spectrum, but we chose to have such an API (Application Programming Interface) for runtime optimization (1D splines have faster evaluation times).

### Step 6: Create Makefile

[MakefileCosmolike](https://github.com/CosmoLike/cocoa_des_y3/blob/main/interface/MakefileCosmolike), located at the `interface` folder, contains the list of the necessary refactored [cosmolike_core](https://github.com/CosmoLike/cosmolike_core) files, as shown below.

    CSOURCES += \
	${ROOTDIR}/external_modules/code/cfftlog/cfftlog.c \
	(...)
	${ROOTDIR}/external_modules/code/cosmolike/pt_cfastpt.c \

    OBJECTC += \
	./cfftlog.o \
	(...)
	./pt_cfastpt.o \

[MakefileCosmolike](https://github.com/CosmoLike/cocoa_des_y3/blob/main/interface/MakefileCosmolike) creates a shared dynamical library for python linking, as shown below

	all:  shared
	shared: cosmolike_des_y3_interface.so
	
	(...)
	
	cosmolike_des_y3_interface.so: $(OBJECTC) $(CSOURCES) interface.cpp
	$(CXX) $(CXXFLAGS) -DCOBAYA_SAMPLER -shared -fPIC -o $@ $(OBJECTC) interface.cpp $(LDFLAGS)
	@rm *.o

### Step 7: Link the CPP functions implemented at interface.cpp to python
	
Linking C++ and Python is rather straightforward. First, we created the file named `cosmolike_des_y3_interface.py`, following the naming convention described above, and inserted the following snippet in it

	def __bootstrap__():
	   (...)
	   
	   __file__ = pkg_resources.resource_filename(__name__, 'cosmolike_des_y3_interface.so') // the only line that needs to be modified in different projects
	   
	   (...)
	__bootstrap__()

We've also inserted the following snippets of code at [interface.cpp](https://github.com/CosmoLike/cocoa_des_y3/blob/main/interface/interface.cpp)
	
	// Python Binding
	#include <pybind11/pybind11.h>
	#include <pybind11/stl.h>
	#include <pybind11/numpy.h>
	namespace py = pybind11;
	
	(...)
	
	PYBIND11_MODULE(cosmolike_des_y3_interface, m) {
	    m.doc() = "CosmoLike Interface for DES-Y3 3x2 Module";

	    m.def("initial_setup", &cpp_initial_setup, "Def Setup");
	    
	    (...) // list of all functions that will be called from the project python likelihood (see step 9).
	    
	    m.def("init_data_real", &cpp_init_data_real,"Init cov, mask and data", py::arg("COV"), py::arg("MASK"), py::arg("DATA"));
	}

### Step 8: Teach Cocoa how to compile, start/stop (i.e., set/unset environment variables) the project

See the files [compile_des_y3](https://github.com/CosmoLike/cocoa_des_y3/blob/main/scripts/compile_des_y3), [start_des_y3](https://github.com/CosmoLike/cocoa_des_y3/blob/main/scripts/start_des_y3) and [stop_des_y3](https://github.com/CosmoLike/cocoa_des_y3/blob/main/scripts/stop_des_y3) on `script` folder. 

Users should always adapt the snippet `cd $ROOTDIR/projects/des_y3/interface` on [compile_des_y3](https://github.com/CosmoLike/cocoa_des_y3/blob/main/scripts/compile_des_y3) to match the name of the desired project.

### Step 9: Create the Python likelihoods

Each two-point function must have its python and YAML files. On des-y3 project, the [likelihood](https://github.com/CosmoLike/cocoa_des_y3/tree/main/likelihood) folder contains

    +-- y3_production
    |    +-- des_2x2pt.py
    |    +-- des_2x2pt.yaml
    |    +-- des_3x2pt.py
    |    +-- des_3x2pt.yaml
    |    +-- des_clustering.py
    |    +-- des_clustering.yaml
    |    +-- des_cosmic_shear.py
    |    +-- des_cosmic_shear.yaml
    |    +-- des_ggl.py
    |    +-- des_ggl.yaml
    |    +-- des_xi_ggl.py
    |    +-- des_xi_ggl.yaml
    
Each Python file includes a class with the same name of the file; for instance, the schematic of the class `des_3x2pt` is shown below

	    class des_3x2pt(_cosmolike_prototype_base):
		def initialize(self):
			Initialize CosmoLike before the chain starts, including reading the keys stored at /data/DES_Y3.dataset
		def logp(self, **params_values):
			Evaluate \chi^2 
		def get_requirements(self):
			Tell the Boltzmann code what Cosmolike needs to evaluate chi^2
		
Python programming paradigm can help to avoid code repetition. In the des_y3 project, the base class `_cosmolike_prototype_base` contains almost all likelihood implementation.
