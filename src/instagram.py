
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

class Instagram:
    def __init__(self):
        self.url = 'https://www.instagram.com/'
        self.driver = webdriver.Remote("http://selenium:4444/wd/hub", desired_capabilities={'browserName':'firefox'})
        #self.driver = webdriver.Chrome(
        #    executable_path='C:/Users/CONSISTE/Downloads/chromedriver.exe')
    def pesquisarPerfil(self):
        pesquisar = self.driver.find_element_by_xpath('//input[@class="XTCLo  x3qfX "]')
        pesquisar.send_keys('rodrigues_a91')
        time.sleep(5)

        pagina = self.driver.find_element_by_xpath('//a[@href="/rodrigues_a91/"]')
        pagina.click()
        time.sleep(3)
    
    def fazerLogin(self):
        username = self.driver.find_element_by_name('username')
        password = self.driver.find_element_by_name('password')
        
        username.send_keys("carlos__webs")
        password.send_keys("cafe1234")
        time.sleep(1)
        
        login_attempt = self.driver.find_element_by_xpath('//button[@class="sqdOP  L3NKy   y3zKF     "]')
        login_attempt.submit()
        time.sleep(3)
        
    def extrairSeguidores(self):
        seguidores = self.driver.find_element_by_xpath('//a[@href="/rodrigues_a91/followers/"]')
        seguidores.click()
        time.sleep(5)

        element = []
        for i in range(30):
            element = self.driver.find_elements_by_xpath('//div[@class="PZuss"]/li')
            element[-1].click()
            time.sleep(2)

        listaDePerfis = self.driver.find_elements_by_xpath('//div[@class="PZuss"]/li')
        listaDeNicks = []

        for perfil in listaDePerfis:
            html_perfil = perfil.get_attribute('outerHTML')
            soup_perfil = BeautifulSoup(html_perfil, 'html.parser')
            nicks = soup_perfil.find_all("a")
            for nick in nicks:
                if nick != None:
                    nickText = nick.text
                    if nickText != '':
                        listaDeNicks.append(nickText)
                        
        self.jsonNicks = {'nicks':listaDeNicks}
        
    def minerar(self):
        self.driver.get(self.url)
        time.sleep(5)
        self.fazerLogin()
        self.pesquisarPerfil()
        self.extrairSeguidores()
        self.driver.quit()
        return self.jsonNicks
    
