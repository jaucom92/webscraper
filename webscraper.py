# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 10:22:11 2019

@author: Jaume Comas Sanchez
"""

class webscraper():
    
    def __init__(self, inital_url='https://www.atozflowers.com/'):
        import requests
        import re
        from bs4 import BeautifulSoup
        
        def url_to_soup(url):
            r = requests.get(url)
            if r.status_code == 200:
                soup = BeautifulSoup(r.content)
                return soup
            else:
                raise ValueError("Status Code isn't 200, probably wrong url.")
        
        self.url_to_soup = url_to_soup
        
        soup = url_to_soup(inital_url)
        self.letter_urls = [l for l in soup.findAll('a') if re.match('^[A-Z]$', l.text) is not None]
        self.main_dict = {}
        
        return
    
    def get_info(self, soup):        
        char = zip(soup.find('div', {'class':'col-md-6 col-lg-5'}).findAll('h5'),
        soup.find('div', {'class':'col-md-6 col-lg-5'}).findAll('p'))
        
        return soup.find('h1').text, {h.text.replace(':', '').replace(' ', '_').lower():p.text for h, p in char} 
    
    def main(self):
        import numpy as np
        
        for u in self.letter_urls:
            soup = self.url_to_soup(u.get('href')).find('ul', {"class": "row list-unstyled"})
            for flower in np.unique([l.get('href') for l in soup.findAll('a')]):
                name, row = self.get_info(self.url_to_soup(flower))
                self.main_dict[name] = row

if __name__=='__main__':
    import pandas as pd
            
    fl = webscraper()
    fl.main()
    pd.DataFrame.from_dict(fl.main_dict, orient='index').reset_index().\
    rename(columns={'index':'flower'}).to_csv('flower_dataset.csv', index=False)


    
        
            
