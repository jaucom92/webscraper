# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 10:22:11 2019

@author: Jaume Comas Sanchez
"""
s=None
class webscraper():
    
    def __init__(self, inital_url='https://www.atozflowers.com/', im_dir='images'):
        import requests
        import re
        from bs4 import BeautifulSoup
        from PIL import Image
        from io import BytesIO
        import os
        
        try:
            os.mkdir(im_dir)
        except FileExistsError:
            pass
        
        def url_to_soup(url, image=False):
            r = requests.get(url)
            if r.status_code == 200:
                if image:
                    im = Image.open(BytesIO(r.content))
                    return im
                else:
                    soup = BeautifulSoup(r.content)
                    return soup
            else:
                raise ValueError("Status Code isn't 200, probably wrong url.")
        
        
        self.url_to_soup = url_to_soup
        
        soup = url_to_soup(inital_url)
        self.letter_urls = [l for l in soup.findAll('a') if re.match('^[A-Z]$', l.text) is not None]
        self.main_dict = {}
        self.im_dir = im_dir
        self.re = re
        
        return
    
    def get_info(self, soup):
        global s
        s = soup
        
        char = zip(
                soup.find('div', {'class':'col-md-6 col-lg-5'}).findAll('h5'),
                soup.find('div', {'class':'col-md-6 col-lg-5'}).findAll('p')
                )
        
        images = soup.find('div', {'class':'content-main-wrapper'}).findAll('img')
        images_dict = {l:self.url_to_soup(i.get('src'), image=True) for i, l in zip(soup.find('div', {'class':'content-main-wrapper'}).findAll('img'), range(len(images)))}
        
        images = []        
        for l, im in images_dict.items():
            wd = self.im_dir + '/' + self.re.match('\w*', soup.find('h1').text).group().lower() + '_' + str(l) + '.jpg'
            im.convert("RGB").save(wd)
            images.append(wd)            
        
        features_dict = {h.text.replace(':', '').replace(' ', '_').lower():p.text for h, p in char}
        features_dict['images'] = ', '.join(images)
        
        return soup.find('h1').text, features_dict
    
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


    
        
            