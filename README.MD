# Lion Weapon

Script to parse standard pdf files from stocks purchase and calculate the average buying price for each stock

These values are important to calculate capital gains for tax declaration purposes in Brazil

**NOTE**: This is for my personal use, so it expects just stock names from the stocks that I've traded. I couldn't find a source with company names to be able to map for the ones that I don't own. You can change `get_abbreviation` method on `importer.py` to add more.

**NOTE 2**: For exceptional earnings like stock splits, bonus stocks and other events that are not registered in the receipts, are coded for my personal stocks, see `add_exceptional_earnings_since_2018` method

**NOTE 3**: Since it uses files in portuguese, some variables are named after the original names in portuguese from the files for easy mapping during development

# Requirements

* Python < 3.10 (tested with Python 3.9.20)

# Setup

It is recommended to use `virtualenv`

Create a `virtualenv`

```
virtualenv lion-weapon-venv
source lion-weapon-venv/bin/activate
```

Install dependencies

```
pip3 install -r requirements.txt
```

# Usage

Put the receipts in `SINACOR` standard format in a folder called `receipts` in the root directory. Run the code with:

```
python3 main.py
```

# Running Tests

```
py.test tests/
```

# Running a Jupyter Server (Optional)

It is useful for debugging and other data manipulation when necessary

### Running the container

Replace `folder_path` with the repo path on the host and `container_name` with one to your liking

```
docker run -it -p 8888:8888 -p 6006:6006 -v <local_folder_path>:/home/jovyan/work --name <container_name> jupyter/pyspark-notebook:python-3.9.6 /bin/bash
```

E.g.

```
docker run -it -p 8888:8888 -p 6006:6006 -v /$(pwd)/lion-weapon:/home/jovyan/work --name lion-weapon jupyter/pyspark-notebook:python-3.9.6 /bin/bash
```

Install the requirements in the container

```
pip3 install -r requirements.txt
```

Run the Jupyter server

```
jupyter notebook --ip 0.0.0.0 --port 8888 --allow-root --NotebookApp.iopub_data_rate_limit=1.0e10
```

### Troubleshooting

#### Venv error

I got this error while running with Python 3.10 (Python 3.10.14)

```
Building wheels for collected packages: pandas
  Building wheel for pandas (pyproject.toml) ... error
  error: subprocess-exited-with-error

  × Building wheel for pandas (pyproject.toml) did not run successfully.
  │ exit code: 1
  ╰─> [1159 lines of output]

[...]

      pandas/_libs/algos.c:785:10: fatal error: numpy/arrayobject.h: No such file or directory
        785 | #include "numpy/arrayobject.h"
            |          ^~~~~~~~~~~~~~~~~~~~~
      compilation terminated.
      error: command '/usr/sbin/gcc' failed with exit code 1
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for pandas
Failed to build pandas
ERROR: Could not build wheels for pandas, which is required to install pyproject.toml-based projects
```

#### Jupyter error

If you see an error like this on container bash:

```
[W 2024-01-30 11:21:41.345 ServerApp] 403 GET /api/kernelspecs?1706613701341 (172.17.0.1) 0.27ms referer=None
[W 2024-01-30 11:21:41.345 ServerApp] wrote error: 'Forbidden'
```

Try downgrading jupyter-server to `jupyter-server==1.24.0`

