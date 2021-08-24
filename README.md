ocean-model-skill-assessor
==============================
[![Build Status](https://img.shields.io/github/workflow/status/axiom-data-science/model_assessor/Tests?logo=github&style=for-the-badge)](https://github.com/axiom-data-science/model_assessor/actions)
[![Code Coverage](https://img.shields.io/codecov/c/github/axiom-data-science/model_assessor.svg?style=for-the-badge)](https://codecov.io/gh/axiom-data-science/model_assessor)
[![License:MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://img.shields.io/readthedocs/model_assessor/latest.svg?style=for-the-badge)](https://model_assessor.readthedocs.io/en/latest/?badge=latest)
[![Code Style Status](https://img.shields.io/github/workflow/status/axiom-data-science/model_assessor/linting%20with%20pre-commit?label=Code%20Style&style=for-the-badge)](https://github.com/axiom-data-science/model_assessor/actions)


A package to fully run the comparison between data and model to assess model skill.

--------

<p><small>Project based on the <a target="_blank" href="https://github.com/jbusecke/cookiecutter-science-project">cookiecutter science project template</a>.</small></p>


## Installation

<!-- Install the package plus its requirements from PyPI with
``` bash
$ pip install ocean_data_gateway
```

or from `conda-forge` with
``` bash
$ conda install -c conda-forge ocean_data_gateway
``` -->

Clone the repo:
``` bash
$ git clone https://github.com/axiom-data-science/ocean_model_skill_assessor.git
```

In the `ocean_model_skill_assessor` directory, install conda environment:
``` bash
$ conda env create -f environment.yml
```

For local package install, in the `ocean_model_skill_assessor` directory:
``` bash
$ pip install -e .
```

To also develop this package, install additional packages with:
``` bash
$ conda install --file requirements-dev.txt
```

To then check code before committing and pushing it to github, locally run
``` bash
$ pre-commit run --all-files
```
