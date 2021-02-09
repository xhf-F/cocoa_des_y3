# cocoa_des_y3

This repository converts the Cosmolike only implementation of DES-Y3 3x2pt analysis in real space archived on [y3_production](https://github.com/CosmoLike/y3_production) repository. Below, we will summarize the conversion of projects already implemented in Cosmolike.

## Relevant Files on [y3_production](https://github.com/CosmoLike/y3_production) repository

    +-- y3_production
    |    +-- init_y3.c
    |    +-- like_test.c
    |    +-- like_test.c
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
