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
    
### Step 1: create a project name and an associated repository
  Repository names should always start with the prefix `cocoa_` followed by the project's name. In our case, the project name is `des_y3`, and the repository is called `cocoa_des_y3`. Given the many bash scripts that automate Cocoa tasks, users must follow our proposed naming convention to avoid undefined behavior.

### Step 2: create the following file structure inside the project's repository

Every project must contain the following folders at minimum

    +-- cocoa_des_y3
    |    +-- likelihood
    |    +-- scripts
    |    +-- data
    |    +-- interface
    |    +-- chains

To avoid polluting the repository with large chain files, we suggest that its path is included in a `.gitignore` file once the `chains` folder is added and committed to the repository.

### Step 3: Copy the files that contains the source and lens redshift distributions, covariance matrix, data vector, and mask .

  The files listed below must be copied to the `data` folder 
    
    +-- y3_production
    |    +-- zdistris
    |    |   +-- nz_lens_Y3_unblinded_10_26_20.txt
    |    |   +-- nz_source_Y3_unblinded_10_26_20.txt
    |    +-- datav
    |    |   +-- Y3_unblinded_10_26_20.txt
    |    +-- yaml
    |    |   +-- 3x2pt_baseline.mask
    |    +-- cov
    |    |   +-- cov_unblinded_11_13_20.txt

### Step 4: Create a dataset file on `data` folder.

See [DES_Y3.dataset](https://github.com/CosmoLike/cocoa_des_y3/blob/main/data/DES_Y3.dataset) file that contains several runtime options such as

    data_file = Y3_unblinded_11_13_20.txt
    (...)
    theta_max_arcmin = 250.
    
### Step 5: Create the interface files 

The files [interface.cpp](https://github.com/CosmoLike/cocoa_des_y3/blob/main/interface/interface.cpp) and [interface.hpp](https://github.com/CosmoLike/cocoa_des_y3/blob/main/interface/interface.hpp) mainly contains C++ adaptation of many functions implemented on files `like_real_y3.c` and `init_y3.c`, as shown below
    
    +-- Adapted from y3_production/like_real_y3.c:
    |    - void cpp_set_cosmological_parameters(const double omega_matter, const double hubble, const bool is_cached_cosmology);
    |    - void cpp_set_nuisance_shear_photoz(vec SP);
    |    - void cpp_set_nuisance_clustering_photoz(vec CP);
    |    - void cpp_set_nuisance_linear_bias(vec B1);
    |    - void cpp_set_nuisance_nonlinear_bias(vec B1, vec B2);
    |    - void cpp_set_nuisance_bias(vec B1, vec B2, vec B_MAG); 
    |    - void cpp_set_nuisance_ia_mpp(vec A1, vec A2, vec B_TA);
    |    - void cpp_set_pm(vec pm);
    |    - double cpp_compute_chi2(vec datavector);
    |    - vec cpp_compute_data_vector();
    +-- Adapted from y3_production/init_y3.c: 
    |    - void cpp_init_lens_sample(std::string multihisto_file, const int Ntomo, const double ggl_cut);
    |    - void cpp_init_binning(const int Ntheta, const double theta_min_arcmin, const double theta_max_arcmin);
    |    - void cpp_init_cosmo_runmode(const bool is_linear);
    |    - void cpp_init_survey(std::string surveyname, double area, double sigma_e);
    |    - void cpp_init_probes(std::string possible_probes);
    |    - void cpp_initial_setup();
    |    - void cpp_init_data_real(std::string COV, std::string MASK, std::string DATA);
            
where `vec` is short for `std::vector<double>`. As a naming convention, the functions converted/adapted from Cosmolike starts with the prefix `cpp_` on `interface.cpp` (CPP stands for C++). There are also functions on how to initialize the interpolation tables of functions evaluated on the Boltzmann code

    - void cpp_init_distances(vec io_z, vec io_chi);
    - void cpp_init_growth(vec io_z, vec io_G);
    - void cpp_init_linear_power_spectrum(vec io_log10k, vec io_z, vec io_lnP);
    - void cpp_init_non_linear_power_spectrum(vec io_log10k, vec io_z, vec io_lnP);

We understand that providing the growth factor as a redshift function is redundant given the linear power spectrum, but we chose to have such an API (Application Programming Interface) for runtime optimization (1D splines have faster evaluation times).

### Step 6: Create Makefile for compiling/linking the necessary theory files

The Makefile [MakefileCosmolike](https://github.com/CosmoLike/cocoa_des_y3/blob/main/interface/MakefileCosmolike), located at the `interface` folder, requires a list of the necessary cosmolike files (adapted from [cosmolike_core](https://github.com/CosmoLike/cosmolike_core) repository and saved on `/external_modules/code/theory`) as shown below.

    CSOURCES += \
	${ROOTDIR}/external_modules/code/cfftlog/cfftlog.c \
	(...)
	${ROOTDIR}/external_modules/code/cosmolike/pt_cfastpt.c \

    OBJECTC += \
	./cfftlog.o \
	(...)
	./pt_cfastpt.o \

The makefile should create a shared dynamical library for python linking, which is done with the line `shared: cosmolike_des_y3_interface.so`. As a naming convention in our API, the python module created for linking Cocoa and Cosmolike should start with the prefix `cosmolike_` and ends with the suffix `_interface`. In between the prefix and the suffix, users should write the name of the project.

### Step 7: Link the CPP functions listed on interface.cpp to python
	
Linking C++ and Python is rather straightforward. First, we created the file named `cosmolike_des_y3_interface.py`, following the naming convention described above, and inserted the following snippet in it

	def __bootstrap__():
	   (...)
	   __file__ = pkg_resources.resource_filename(__name__, 'cosmolike_des_y3_interface.so')
	   (...)
	__bootstrap__()

We've also inserted the following snippets of code at the beginning and end of [interface.cpp](https://github.com/CosmoLike/cocoa_des_y3/blob/main/interface/interface.cpp) C++ file respectively

	// Python Binding
	#include <pybind11/pybind11.h>
	#include <pybind11/stl.h>
	#include <pybind11/numpy.h>
	namespace py = pybind11;

	PYBIND11_MODULE(cosmolike_des_y3_interface, m) {
	    m.doc() = "CosmoLike Interface for DES-Y3 3x2 Module";

	    m.def("initial_setup", &cpp_initial_setup, "Def Setup");
	    (...)
	    m.def("init_data_real", &cpp_init_data_real,"Init cov, mask and data", py::arg("COV"), py::arg("MASK"), py::arg("DATA"));
	}

### Step 8: Teach Cocoa how to compile, start and stop your project (start/stop important given possible enviroment variables)

	To accomplish this, we created the files [compile_des_y3](https://github.com/CosmoLike/cocoa_des_y3/blob/main/scripts/compile_des_y3), [start_des_y3](https://github.com/CosmoLike/cocoa_des_y3/blob/main/scripts/start_des_y3) and [stop_des_y3](https://github.com/CosmoLike/cocoa_des_y3/blob/main/scripts/stop_des_y3) on `script` folder 
