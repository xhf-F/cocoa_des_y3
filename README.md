This repository converts the Cosmolike only implementation of DES-Y3 3x2pt analysis in real space  ([y3_production](https://github.com/CosmoLike/y3_production) repository). 

To facilitate the conversion of other projects from Cosmolike to Cocoa, we summarize below the steps necessary for this refactoring, using the cocoa_des_y3 repository as a guideline.
    
### Step 1: name the project and create the repository
Repository names must always start with the prefix `cocoa_` followed by the project's name. Users must follow this proposed naming convention to avoid undefined behavior, given how we wrote the bash scripts that automate Cocoa's tasks. Also, projects must have the following directory structure

    +-- cocoa_des_y3
    |    +-- likelihood
    |    +-- scripts
    |    +-- data
    |    +-- interface
    |    +-- chains

We suggest the path for the `chains` folder to be included in `.gitignore` once the folder is added and committed to the project's repository. This exclusion avoids filling the project's repository with large chain files. See [.gitignore](https://github.com/CosmoLike/cocoa_des_y3/blob/main/.gitignore) as a template. 

### Step 2: copy the project's data products to `/data`

The data products must include the covariance matrice, data vector, source and lens redshift distributions, and mask files. See [cocoa_des_y3/data](https://github.com/CosmoLike/cocoa_des_y3/tree/main/data) as a template 

### Step 3: create a dataset file on `/data`

The dataset file is the place to include options about the project's dataset that users can alter at runtime. See [DES_Y3.dataset](https://github.com/CosmoLike/cocoa_des_y3/blob/main/data/DES_Y3.dataset) as a template. 

### Step 4: create the Cosmolike interface on `/interface`.

The C++ code on files [interface.cpp](https://github.com/CosmoLike/cocoa_des_y3/blob/main/interface/interface.cpp) and [interface.hpp](https://github.com/CosmoLike/cocoa_des_y3/blob/main/interface/interface.hpp)  consists of refactoring of several functions originally implemented at [like_real_y3.c](https://github.com/CosmoLike/y3_production/blob/master/like_real_y3.c) and [init_y3.c](https://github.com/CosmoLike/y3_production/blob/master/init_y3.c). Most Cosmolike only projects contains C files with similar structure to [like_real_y3.c](https://github.com/CosmoLike/y3_production/blob/master/like_real_y3.c) and [init_y3.c](https://github.com/CosmoLike/y3_production/blob/master/init_y3.c).

PS we've adopted a C++ interface given the straightforward procedure to link C++ code with Python. Advanced developers who prefer to code exclusively in C can create a pure C interface without any issues.

### Step 5: create a makefile on `/interface`.

The Makefile contains the list of the necessary refactored [cosmolike_core](https://github.com/CosmoLike/cosmolike_core) files, located at [${ROOTDIR}/external_modules/code](https://github.com/CosmoLike/cocoa/tree/main/Cocoa/external_modules/code). See [MakefileCosmolike](https://github.com/CosmoLike/cocoa_des_y3/blob/main/interface/MakefileCosmolike) as a template. A snippet of the places that need to be modified in [MakefileCosmolike](https://github.com/CosmoLike/cocoa_des_y3/blob/main/interface/MakefileCosmolike) for different projects is shown below.

    CSOURCES += \
	    ${ROOTDIR}/external_modules/code/cfftlog/cfftlog.c \
	  
	    (...)
	  
	    ${ROOTDIR}/external_modules/code/cosmolike/pt_cfastpt.c \

    OBJECTC += \
	    ./cfftlog.o \
	  
	    (...)
	  
	    ./pt_cfastpt.o \

[MakefileCosmolike](https://github.com/CosmoLike/cocoa_des_y3/blob/main/interface/MakefileCosmolike) also creates a shared dynamical library that will be loaded from the python likelihood code, as shown below

	all:  shared
	shared: cosmolike_des_y3_interface.so
	
	(...)
	
	cosmolike_des_y3_interface.so: $(OBJECTC) $(CSOURCES) interface.cpp
	    $(CXX) $(CXXFLAGS) -DCOBAYA_SAMPLER -shared -fPIC -o $@ $(OBJECTC) interface.cpp $(LDFLAGS)
	    @rm *.o

PS given that Cocoa can load multiple Cosmolike projects simultaneously, the mandatory nomenclature for the dynamical library is the prefix `cosmolike_` followed by the name of the project followed by the suffix `_interface`.  

### Step 6: create a script on `/script` that teaches Cocoa how to compile the project 

See files [compile_des_y3](https://github.com/CosmoLike/cocoa_des_y3/blob/main/scripts/compile_des_y3) as a template. Users should adapt the snippet `cd $ROOTDIR/projects/des_y3/interface` on [compile_des_y3](https://github.com/CosmoLike/cocoa_des_y3/blob/main/scripts/compile_des_y3) script to match the name of the desired project.

### Step 7: create scripts on `/script` to set/unset environment variables for the project

See [start_des_y3](https://github.com/CosmoLike/cocoa_des_y3/blob/main/scripts/start_des_y3) and [stop_des_y3](https://github.com/CosmoLike/cocoa_des_y3/blob/main/scripts/stop_des_y3) as templates. 

### Step 8: create the project's python likelihoods on `/likelihood`

Each two-point function (or a particular combination of two-point functions) must have its python file (and class) and YAML files. For instance, the [likelihood](https://github.com/CosmoLike/cocoa_des_y3/tree/main/likelihood) folder contains the following files

    +-- likelihood
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
    
Each Python file includes a class with the same name as the file. For instance, the schematic of the class `des_3x2pt` is shown below.

    class des_3x2pt(_cosmolike_prototype_base):
	    def initialize(self):
            Initialize CosmoLike before the chain starts, including reading the keys stored at /data/DES_Y3.dataset
	    def logp(self, **params_values):
            Evaluate \chi^2 
	    def get_requirements(self):
            Tell the Boltzmann code what Cosmolike needs to evaluate chi^2
		
Python programming paradigm can help to avoid code repetition. In the des_y3 project, the base class `_cosmolike_prototype_base`, located at [\_cosmolike_prototype_base.py](https://github.com/CosmoLike/cocoa_des_y3/blob/main/likelihood/_cosmolike_prototype_base.py) contains almost all likelihood implementation.

The YAML files should point to the dataset file (step 3) as shown below
	
	data_file: DES_Y3.dataset
	
Finally, the YAML file should also include the list of nuisance parameters, their priors, and reference points (initial distribution of points in the chains), as exemplified below

	DES_DZ_S1:
	    prior:
	        dist: norm
	        loc: 0.0
	        scale: 0.018
	    ref:
	        dist: norm
	        loc: 0.0
	        scale: 0.036
	    proposal: 0.018
	    latex: \Delta z_\mathrm{s,DES}^1
	 
To avoid repetition of code among multiple YAML files, we suggest the usage of the following command,  included in [des_3x2pt.yaml](https://github.com/CosmoLike/cocoa_des_y3/blob/main/likelihood/des_3x2pt.yaml), [des_ggl.yaml](https://github.com/CosmoLike/cocoa_des_y3/blob/main/likelihood/des_ggl.yaml), [des_xi_ggl.yaml](https://github.com/CosmoLike/cocoa_des_y3/blob/main/likelihood/des_xi_ggl.yaml) and [des_2x2.yaml](https://github.com/CosmoLike/cocoa_des_y3/blob/main/likelihood/des_2x2pt.yaml) sripts.

	params: !defaults [params_des_3x2pt]
	
### Step 9: link the Cosmolike interface to the python likelihoods
	
Linking C++ and Python is rather straightforward. First, we've created the file named [cosmolike_des_y3_interface.py](https://github.com/CosmoLike/cocoa_des_y3/blob/main/interface/cosmolike_des_y3_interface.py) on the `interface` folder, and inserted the following snippet in it

	def __bootstrap__():
	    (...)
	   
	    __file__ = pkg_resources.resource_filename(__name__, 'cosmolike_des_y3_interface.so')
	   
	    (...)
	__bootstrap__()

Second, we've inserted the following snippets of code at [interface.cpp](https://github.com/CosmoLike/cocoa_des_y3/blob/main/interface/interface.cpp)
	
	// Python Binding
	#include <pybind11/pybind11.h>
	#include <pybind11/stl.h>
	#include <pybind11/numpy.h>
	namespace py = pybind11;
	
	(...)
	
	PYBIND11_MODULE(cosmolike_des_y3_interface, m) {
	    m.doc() = "CosmoLike Interface for DES-Y3 3x2 Module";

	    m.def("initial_setup", &cpp_initial_setup, "Def Setup");
	    
	    (...)
	    
	    m.def("init_data_real", &cpp_init_data_real,"Init cov, mask and data", py::arg("COV"), py::arg("MASK"), py::arg("DATA"));
	}

Notice that the module's name, shown in the snippet `PYBIND11_MODULE(cosmolike_des_y3_interface, m)`, follows the mandatory naming convention for the dynamical library file (cosmolike_des_y3_interface.so). The python file with the bootstrap snippet is also named following this rule. 

Third, we've added the following flags, which do not need to be modified for different projects, in [MakefileCosmolike](https://github.com/CosmoLike/cocoa_des_y3/blob/main/interface/MakefileCosmolike)

	# LINK PYBIND LIBRARY
	PYBIND := 1
	
	(...)
	
	ifdef PYBIND
	    CXXFLAGS += $(shell python3 -m pybind11 --includes) -DPYBIND11
	    LDFLAGS += $(shell python3-config --ldflags)
	endif

Finally, we've added the project's directory to the `LD_LIBRARY_PATH` and `PYTHONPATH` by inserting the following snippet on [start_des_y3](https://github.com/CosmoLike/cocoa_des_y3/blob/main/scripts/start_des_y3) (the script that set environment variables for the project - see step 7).

	addvar LD_LIBRARY_PATH $ROOTDIR/projects/des_y3/interface
	addvar PYTHONPATH $ROOTDIR/projects/des_y3/interface

The python likelihoods (see step 8), can then load the Cosmolike interface with the line

	import cosmolike_des_y3_interface

**The consistency of the required mandatory naming conventions allows Cocoa to load multiple projects without mixing their code**. Users must be diligent in updating all `_des_y3_` snippets with the appropriate project's name. 

### Step 10: [cosmolike_core/theory](https://github.com/CosmoLike/cosmolike_core/tree/master/theory) refactoring

Check that all needed functions implemented at [cosmolike_core/theory](https://github.com/CosmoLike/cosmolike_core/tree/master/theory) have been refactored in [external_modules/code/cosmolike](https://github.com/CosmoLike/cocoa/tree/main/Cocoa/external_modules/code/cosmolike), which is an incomplete port to streamline development. Such refactoring require a few steps that we are going to explain below:

#### Refactoring Step 1: Create header files

See [bias.c](https://github.com/CosmoLike/cocoa/blob/main/Cocoa/external_modules/code/cosmolike/bias.c) and [bias.h](https://github.com/CosmoLike/cocoa/blob/main/Cocoa/external_modules/code/cosmolike/bias.h) as templates. Don't forget the following special guards on every header file to allow linking between C and C++:
 
 	#ifdef __cplusplus
	extern "C" {
	#endif
	
	(...)
	
	#ifdef __cplusplus
	}
	#endif

#### Refactoring Step 2: update the project's code to take into account the API changes on window weights

For optimzations, we've changed the APIs of a few radial window weights (see [radial_weights.c](https://github.com/CosmoLike/cocoa/blob/main/Cocoa/external_modules/code/cosmolike/radial_weights.c)), including

	double W_gal(double a, double nz, double chi, double hoverh0);
	double W_source(double a, double nz, double hoverh0);
	double W_HOD(double a, double nz, double hoverh0);
	
#### Refactoring Step 3 (optional): thread with OpenMP most expensive functions call

This is an optional but important step that can significantly speed up the chains as Cobaya samplers utilize OpenMP to accelerate convergence. Given Cosmolike design, which caches critical information on static variables, threading loops that are computationally expensive was performed with the following general strategy

	// single-thread version of the loop
	for(int i=0; i<N; i++) {
	    // call functions that hold static variables. If they need to be changed, 
	    // that will happen at the i=0 iteration (please check that in your particular code)
	}
	
	// multi--thread version
	{
	    const int i = 0;
	    // do the i=0 iteration of the loop without threading
	}
	
	#pragma omp parallel for
	for(int i=1; i<N; i++) {
	    // repeat the same loop code - now static variables will be read-only (Cosmolike design)
	}

Users must carefully check the code against race conditions, by running chains with and without OpenMP threading and making sure they give consistent results.

On double loops, this general strategy can be used recursivelly to avoid the `i = 0` evaluation to dominate the runtime, as shown below

	// single-thread version of the loop
	for(int i=0; i<N; i++) {
	    for(int j=0; j<M; j++) {
	        // call functions that hold static variables. If they need to be changed, 
	        // that will happen at the i=0 iteration (please check that in your particular code)
	    }
	}
	
	// multi--thread version
	{
	    const int i = 0;
	    // do the i=0 iteration of the loop without threading
	    {
	    	const int j=0;
		// inner loop w/ i=0,j=0 (no threading)
	    }
	    #pragma omp parallel for
	    for(int j=0; j<M; j++) {
	    	// inner loop
	    }
	}
	
	#pragma omp parallel for // when possible threading only the outer loop is more optimal
	for(int i=1; i<N; i++) {
	    for(int j=0; j<M; j++) {
	    // repeat the same loop code - now static variables will be read-only (Cosmolike design)
	    }
	}
	
**Notice that our OpenMP threading requires duplication of code. Optimization and readability - as usual - are anticorrelated.** 
