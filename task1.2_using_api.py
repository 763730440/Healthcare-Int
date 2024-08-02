import streamlit as st
import requests

def fetch_drug_info(drug_name):
    base_url = 'https://api.fda.gov/drug/label.json'
    encoded_drug_name = requests.utils.quote(drug_name)
    url = f'{base_url}?search=openfda.brand_name:{encoded_drug_name}'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_response = response.json()
            if 'results' in json_response and json_response['results']:
                return json_response['results'][0]
            else:
                return None
        else:
            st.error(f'Failed to fetch drug info: {response.status_code}')
            return None
    except Exception as e:
        st.error(f'Failed to fetch drug info: {e}')
        return None

def display_section(title, content):
    if content:
        st.markdown(f'### {title}')
        st.markdown(f'<div style="padding: 10px; background-color: #333333; border: 1px solid #444444; border-radius: 5px; color: #ffffff;">{content}</div>', unsafe_allow_html=True)

# Streamlit page configuration
st.set_page_config(page_title="Drug Info", page_icon="💊", layout="wide")

# Streamlit app layout
st.title('💊 Drug Info')

st.markdown("""
    <style>
        .reportview-container {
            background: #1e1e1e;
        }
        .sidebar .sidebar-content {
            background: #333333;
        }
        h2, h3, h4, h5, h6 {
            color: #ffffff;
        }
        .stButton button {
            background-color: #444444;
            color: #ffffff;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stButton button:hover {
            background-color: #555555;
        }
        .stTextInput input {
            background-color: #2a2a2a;
            color: #ffffff;
            border: 1px solid #555555;
        }
        .stTextInput input::placeholder {
            color: #888888;
        }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center;">
        <h2 style="color: #ffffff;">Enter the drug name to search for its information.</h2>
    </div>
    """, unsafe_allow_html=True)

drug_name = st.text_input('', placeholder='Enter Drug Name', help='Type the brand name of the drug you want to search for.')

if st.button('Fetch Drug Info'):
    if drug_name:
        with st.spinner('Fetching drug information...'):
            drug_info = fetch_drug_info(drug_name)
            if drug_info:
                display_section('Description', drug_info.get('description', [''])[0])
                display_section('Indications and Usage', drug_info.get('indications_and_usage', [''])[0])
                display_section('Warnings', drug_info.get('warnings', [''])[0])
                display_section('Dosage and Administration', drug_info.get('dosage_and_administration', [''])[0])
                display_section('Adverse Reactions', drug_info.get('adverse_reactions', [''])[0])
                display_section('Active Ingredients', ', '.join(drug_info.get('active_ingredient', [])))
                display_section('Purpose', ', '.join(drug_info.get('purpose', [])))
                display_section('Contraindications', drug_info.get('contraindications', [''])[0])
                display_section('Drug Interactions', drug_info.get('drug_interactions', [''])[0])
                display_section('Manufacturer', drug_info.get('openfda', {}).get('manufacturer_name', [''])[0])
                display_section('Generic Name', drug_info.get('openfda', {}).get('generic_name', [''])[0])
                display_section('Brand Names', ', '.join(drug_info.get('openfda', {}).get('brand_name', [])))
            else:
                st.write('No information available for this drug.')
    else:
        st.warning('Please enter a drug name.')
