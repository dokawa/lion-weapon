# Lion Weapon

Script to parse standard pdf files from stocks purchase and calculate the average buying price for each stock.

These values are important to calculate capital gains for tax declaration purposes in Brazil. 


# Setup

It is recommended to use virtualenv

Create a virtualenv

```
virtualenv lion-weapon-venv
source lion-weapon-venv/bin/activate
```

Install dependencies

```
pip3 install -r requirements.txt
```

# Usage

Put the receipts in `SINACOR` standard format in a folder called `receipts` in the root directory


```
python3 main.py
```

# Running Tests

```
py.test tests/
```


# Running a Jupyter Server (Optional)

It is useful for debugging and other data manipulation when necessary.


### Running the container

Replace `folder_path` with the repo path on the host and `container_name` with one to your liking.

```
docker run -it -p 8888:8888 -p 6006:6006 -v <folder_path>:/lion-weapon --name <container_name> tensorflow/tensorflow /bin/bash
```

E.g.
```
docker run -it -p 8888:8888 -p 6006:6006 -v ~/lion-weapon:/lion-weapon --name lion-weapon tensorflow/tensorflow /bin/bash
```

Install the requirements in the container
```
pip3 install -r requirements.txt
```

Run the Jupyter server
```
jupyter notebook --ip 0.0.0.0 --port 8888 --allow-root --NotebookApp.iopub_data_rate_limit=1.0e10
```