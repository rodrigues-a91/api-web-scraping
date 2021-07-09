# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 21:35:50 2021

@author: CONSISTE
"""
from selenium import webdriver
from bs4 import BeautifulSoup

def minerar():
    url = 'https://www.reclameaqui.com.br/ranking/'

    driver = webdriver.Remote("http://selenium:4444/wd/hub", desired_capabilities={'browserName':'firefox'})

    driver.get(url)

    rankings = driver.find_elements_by_xpath('//div[@class="col-md-4 col-sm-6 flexbox-col ng-scope"]')
    docFinal = {}
    for ranking in rankings:
        html_ranking = ranking.get_attribute('outerHTML')
        soup_ranking = BeautifulSoup(html_ranking, 'html.parser')
        tipoRanking = soup_ranking.find('h2', class_="ng-binding").text
        data = soup_ranking.find('p', class_="ng-binding").text
        empresas = soup_ranking.ol.find_all('li')
        listaDocs = [] 
        
        for empresa in empresas:
            empresaPadronizada = empresa.a.text.split(' ')
            doc = {'nomeDaEmpresa':' '.join(empresaPadronizada[:len(empresaPadronizada)-1]),
                'nota/indice':empresa.span.text,
                'data': data}
            listaDocs.append(doc)
        
        docFinal[tipoRanking] = listaDocs
        
        
    driver.quit()
    return docFinal
     
