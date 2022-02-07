import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
from lxml import etree
import pandas as pd

strudex_dict = {
	'URL': [],
	'Structured Data': []
}

urls = st.text_area('Enter URLs, 1 per line')

submit = st.button('Submit')

if submit:

	lines = urls.split("\n")
	url_list = [line for line in lines]

	for u in url_list:

		try:

			response = requests.get(u)

			soup = BeautifulSoup(response.content, 'html.parser')

			data = json.loads(soup.find('script', type='application/ld+json').string)
			
			strudex_dict['URL'].append(u)
			strudex_dict['Structured Data'].append(data)

		except Exception as e:
			print(e, 'Nothing found')
			continue
			
	csv = pd.DataFrame(strudex_dict).to_csv(index=False)
	
	st.download_button(label="Download data as CSV", data=csv, file_name='strudex.csv', mime='text/csv')
