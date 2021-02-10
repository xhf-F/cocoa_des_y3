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
  Repository names should always start with the prefix `cocoa_` followed by the name of the project. In our case, the project name is `des_y3`, and the repository is called `cocoa_des_y3`.

### Step 2: create the following file structure inside the project's repository

    +-- cocoa_des_y3
    |    +-- likelihood
    |    +-- scripts
    |    +-- data
    |    +-- interface
    |    +-- chains
    |    |   +-- README (blank file)

### Step 3: Copy the redshift distributions, covariance matrix, data vector, and mask.

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

See [DES_Y3.dataset](https://github.com/CosmoLike/cocoa_des_y3/blob/main/data/DES_Y3.dataset) file, which for the des_y3 project contains the following keys: 

    data_file = Y3_unblinded_11_13_20.txt
    cov_file = cov_unblinded_11_13_20.txt
    mask_file = 3x2pt_baseline.mask
    nz_lens_file = nz_lens_Y3_unblinded_11_13_20.txt
    nz_source_file = nz_source_Y3_unblinded_11_13_20.txt
    lensing_overlap_cut = 0.0015
    nuisance_params = DES.paramnames
    lens_ntomo = 5
    source_ntomo = 4
    n_theta = 20
    IA_model = 6
    theta_min_arcmin = 2.5
    theta_max_arcmin = 250.
    
Additional project specific runtime options can be added
    
### Step 5: Create the interface files 

The files [interface.cpp](https://github.com/CosmoLike/cocoa_des_y3/blob/main/interface/interface.cpp) and [interface.hpp](https://github.com/CosmoLike/cocoa_des_y3/blob/main/interface/interface.hpp) mainly contains C++ adaptation of many functions implemented on files `like_real_y3.c` and `init_y3.c`, as shown below
    
    +-- y3_production
    |    +-- like_real_y3.c
            - void cpp_set_cosmological_parameters(const double omega_matter, const double hubble, const bool is_cached_cosmology);
            - void cpp_set_nuisance_shear_photoz(vec SP);
            - void cpp_set_nuisance_clustering_photoz(vec CP);
            - void cpp_set_nuisance_linear_bias(vec B1);
            - void cpp_set_nuisance_nonlinear_bias(vec B1, vec B2);
            - void cpp_set_nuisance_bias(vec B1, vec B2, vec B_MAG); 
            - void cpp_set_nuisance_ia_mpp(vec A1, vec A2, vec B_TA);
            - void cpp_set_pm(vec pm);
            - double cpp_compute_chi2(vec datavector);
            - vec cpp_compute_data_vector();
    |    +-- init_y3.c
            - void cpp_init_lens_sample(std::string multihisto_file, const int Ntomo, const double ggl_cut);
            - void cpp_init_binning(const int Ntheta, const double theta_min_arcmin, const double theta_max_arcmin);
            - void cpp_init_cosmo_runmode(const bool is_linear);
            - void cpp_init_survey(std::string surveyname, double area, double sigma_e);
            - void cpp_init_probes(std::string possible_probes);
            - void cpp_initial_setup();
            
where `vec` is short for `std::vector<double>`. As a naming convention, the functions converted/adapted from Cosmolike starts with the prefix `cpp_` on `interface.cpp` (CPP stands for C++). There are also functions on how to initialize the interpolation tables of functions evaluated on the Boltzmann code

    - void cpp_init_distances(vec io_z, vec io_chi);
    - void cpp_init_growth(vec io_z, vec io_G);
    - void cpp_init_linear_power_spectrum(vec io_log10k, vec io_z, vec io_lnP);
    - void cpp_init_non_linear_power_spectrum(vec io_log10k, vec io_z, vec io_lnP);

We understand that providing the growth factor as a redshift function is redundant given the linear power spectrum, but we chose to have such an API (Application Programming Interface) for runtime optimization (1D splines have faster evaluation times).

### Step 6: Create a Makefile that will compile and link the necessary Cosmolike files with interface.cpp

The file `MakefileCosmolike` on the `interface` folder requires a list of the necessary Cosmolike files saved on `/external_modules/code/theory` as shown below.

    CSOURCES += \
		${ROOTDIR}/external_modules/code/cfftlog/cfftlog.c \
		${ROOTDIR}/external_modules/code/cfftlog/utils_complex.c \
		${ROOTDIR}/external_modules/code/cfftlog/utils.c \
		${ROOTDIR}/external_modules/code/cfastpt/cfastpt.c \
		${ROOTDIR}/external_modules/code/cfastpt/utils_complex_cfastpt.c \
		${ROOTDIR}/external_modules/code/cfastpt/utils_cfastpt.c \
		${ROOTDIR}/external_modules/code/cosmolike/basics.c \
		${ROOTDIR}/external_modules/code/cosmolike/bias.c \
		${ROOTDIR}/external_modules/code/cosmolike/cosmo3D.c \
		${ROOTDIR}/external_modules/code/cosmolike/cosmo2D_fourier.c \
		${ROOTDIR}/external_modules/code/cosmolike/cosmo2D_exact_fft.c \
		${ROOTDIR}/external_modules/code/cosmolike/cosmo2D_fullsky_TATT.c \
		${ROOTDIR}/external_modules/code/cosmolike/halo.c \
		${ROOTDIR}/external_modules/code/cosmolike/recompute.c \
		${ROOTDIR}/external_modules/code/cosmolike/radial_weights.c \
		${ROOTDIR}/external_modules/code/cosmolike/redshift_spline.c \
		${ROOTDIR}/external_modules/code/cosmolike/structs.c \
		${ROOTDIR}/external_modules/code/cosmolike/pt_cfastpt.c \

        OBJECTC += \
                ./cfftlog.o \
                ./utils_complex.o \
                ./utils.o \
                ./cfastpt.o \
                ./utils_complex_cfastpt.o \
                ./utils_cfastpt.o \
                ./basics.o \
                ./bias.o \
                ./cosmo3D.o \
                ./cosmo2D_exact_fft.o \
                ./cosmo2D_fourier.o \
                ./cosmo2D_fullsky_TATT.o \
                ./halo.o \
                ./radial_weights.o \
                ./recompute.o \
                ./redshift_spline.o \
                ./structs.o \
                ./pt_cfastpt.o \

The makefile should create a shared dynamical library for python linking, which is done with the line `shared: cosmolike_des_y3_interface.so`. As a naming convention in our API, the python module created for linking Cocoa and Cosmolike should start with the prefix `cosmolike_` and ends with the suffix `_interface`. In between the prefix and the suffix, users should write the name of the project.
            
