#backend/extractors.py

import pandas as pd
from PyPDF2 import PdfFileReader
import requests 
from bs4 import BeautifulSoup
import io

def extract_text_from_pdf(file_path):
    with open(file_path,'rb') as f:
        reader = PdfFileReader(f)
        text = ''
        for page in range(reader.getNumPages()):
            text += reader.getPage(page).extract_text()
    return text
        
def extract_text_from_csv(file_path):
    df = pd.read_csv(file_path)
    return df.to_string()

def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    return soup.get_text()

