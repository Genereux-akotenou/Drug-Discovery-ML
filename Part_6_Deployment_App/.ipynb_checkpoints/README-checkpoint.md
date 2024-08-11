# drug_discovery_app

### Create conda environment
Firstly, we will create a conda environment called *lab1_env*
```
python -m venv bioactivity-env
```
Secondly, we will login to the *lab1_env* environement
```
source ./bioactivity-env/bin/activate
```
### Install prerequisite libraries
Pip install libraries
```
pip install -r requirements.txt
```

###  Launch the app
```
python -m streamlit run app.py
```