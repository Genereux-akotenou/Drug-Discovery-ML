# ------------------------------------------------------- 
# Requirements
# ------------------------------------------------------- 
import os, csv, base64, subprocess, pypickle
from padelpy import padeldescriptor
import streamlit as st
import pandas as pd
from PIL import Image

# ------------------------------------------------------- 
# Utils
# ------------------------------------------------------- 
def descriptor_calc():
    """
    Utils: Molecular descriptor calculator
    """
    padeldescriptor(mol_dir='molecule.smi',  d_file='descriptors_output.csv', descriptortypes='./PaDEL-Descriptor/PubchemFingerprinter.xml', 
                    fingerprints=True, standardizenitro=True, removesalt=True, threads=6
    )
    #os.remove('molecule.smi')


def filedownload(df):
    """
    Utils: File download
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="prediction.csv">Download Predictions</a>'
    return href

def build_model(input_data):
    """
    Utils: Model building and make prediction
    """
    load_model = pypickle.load('utils/best_model.pkl')
    prediction = load_model.predict(input_data)
    st.header('**Prediction output**')
    prediction_output = pd.Series(prediction, name='pIC50')
    molecule_name = pd.Series(load_data.iloc[:, 0], name='molecule_name')
    df = pd.concat([molecule_name, prediction_output], axis=1)
    st.write(df)
    st.markdown(filedownload(df), unsafe_allow_html=True)

# ------------------------------------------------------- 
# App Content
# ------------------------------------------------------- 
image = Image.open('utils/logo.png')
st.image(image, use_column_width=True)
st.markdown("""
    # Bioactivity Prediction App (Cancer breast drug discovery)
    
    This app allows you to predict the bioactivity towards inhibting the `Aromatose` enzyme. `Aromatose` is a drug target for breast cancer, particularly in postmenopausal women.
    
    **Credits**
    - App built by [Généreux Akotenou](https://github.com/Genereux-akotenou). Project inspired by [Chanin Nantasenamat](https://medium.com/@chanin.nantasenamat) works.
    - Descriptor calculated using [PaDEL-Descriptor Python version](https://github.com/ecrl/padelpy).[Read PaDEL-Descriptor Paper]]
    (https://doi.org/10.1002/jcc.21707).    
    ---
    """
)

with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input file", type=['txt', 'csv'])
    st.sidebar.markdown("""
        [Example input file](https://github.com/Genereux-akotenou/Drug-Discovery-ML/blob/main/Part_6_Deployment_App/sample_submission.txt)
    """)

if st.sidebar.button('Predict'):
    load_data = pd.read_table(uploaded_file, sep=' ', header=None)
    load_data.to_csv('molecule.smi', sep = '\t', header = False, index = False, quoting=csv.QUOTE_NONE, escapechar='\\')
    st.header('**Original input data**')
    st.write(load_data)

    with st.spinner("Calculating descriptors..."):
        descriptor_calc()

    # Read in calculated descriptors and display the dataframe
    st.header('**Calculated molecular descriptors**')
    desc = pd.read_csv('descriptors_output.csv')
    st.write(desc)
    st.write(desc.shape)

    # Read descriptor list used in previously built model
    st.header('**Subset of descriptors from previously built models**')
    Xlist = list(pd.read_csv('utils/descriptor_col.txt').columns)
    desc_subset = desc[Xlist]
    st.write(desc_subset)
    st.write(desc_subset.shape)

    # Apply trained model to make prediction on query compounds
    build_model(desc_subset)
    os.remove('descriptors_output.csv')
else:
    st.info('Upload input data in the sidebar to start!')
