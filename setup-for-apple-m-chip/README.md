# setup Env for Apple M chip

## with micro-mamba

1. install micromamba, please refer to [mamba doc](https://mamba.readthedocs.io/en/latest/installation.html#automatic-installation)

   ```shell
   brew install micromamba
   # persist shell command setting with micromamba
   /opt/homebrew/opt/micromamba/bin/micromamba shell init -s zsh -p ~/micromamba
   # alias micromamba
   alias mmb=micromamba
   # reload zsh shell
   source ~/.zshrc
   ```

2. set package channels in the file [~/.mambarc](./.mambarc)

   ```shell
   vi ~/.mambarc
   ---
   channels:
     - conda-forge
   ---
   ```

3. install numpy

   create env

   ```shell
   #micromamba create -n finlab -c conda-forge
   micromamba create -n finlab
   micromamba activate finlab
   ```

   install numpy with accelerate

   ```shell
   micromamba install numpy "libblas=*=*accelerate"
   ```

   to check accelerate

   ```shell
   micromamba list | grep blas
   # output
     libblas          3.9.0      16_osxarm64_accelerate  conda-forge
     libcblas         3.9.0      16_osxarm64_accelerate  conda-forge
   ```

4. verify and benchmark

   ```shell
   python svd.py
   # output
   mean of 10 runs: 0.81013s
   
   python dario.py
   # output
   Dotted two 4096x4096 matrices in 0.24 s.
   Dotted two vectors of length 524288 in 0.10 ms.
   SVD of a 2048x1024 matrix in 0.29 s.
   Cholesky decomposition of a 2048x2048 matrix in 0.06 s.
   Eigendecomposition of a 2048x2048 matrix in 3.20 s.
   ```

**additional setting to keep the `accelerate` on updating**

edit the file `~/micromamba/envs/<YOUR_ENV_NAME>/conda-meta/pinned` and add the following line

```
libblas=*=*accelerate
```

## with mini-conda

[install miniconda3](https://docs.conda.io/en/latest/miniconda.html)

[manage conda env](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

install numpy with accelerate, please refer to mamba part

disable auto activation of conda base environment, set environment variable CONDA_AUTO_ACTIVATE_BASE,

```shell
export CONDA_AUTO_ACTIVATE_BASE=false
```

## create env with yaml spec file

the content of [spec file](./finlab.yaml)

```yaml
name: finlab
channels:
  - conda-forge
dependencies:
  - python=3.10
  - libblas=*=*accelerate
  - numpy
  - ipykernel
  - ipywidgets
```

create env

```shelll
conda env create -f mlab.yaml
micromamba create -f finlab.yaml
```

## reference

- https://gist.github.com/MarkDana/a9481b8134cf38a556cf23e1e815dafb
- [Installing TensorFlow on the M1 Mac](https://towardsdatascience.com/installing-tensorflow-on-the-m1-mac-410bb36b776)
- [Customizing with conda and mamba](https://www.ibm.com/docs/en/cloud-paks/cp-data/4.6.x?topic=pip-customizing-conda-mamba)
