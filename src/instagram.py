
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

def minerar():
    url = 'https://www.instagram.com/'
    driver = webdriver.Remote("http://selenium:4444/wd/hub", desired_capabilities={'browserName':'firefox'})

    driver.get(url)
    time.sleep(5)
    username = driver.find_element_by_name('username')
    password = driver.find_element_by_name('password')

    username.send_keys("carlos__webs")
    password.send_keys("cafe1234")

    time.sleep(3)
    login_attempt = driver.find_element_by_xpath('//button[@class="sqdOP  L3NKy   y3zKF     "]')
    login_attempt.submit()

    time.sleep(3)
    pesquisar = driver.find_element_by_xpath('//input[@class="XTCLo  x3qfX "]')
    pesquisar.send_keys('rodrigues_a91')

    time.sleep(5)


    pagina = driver.find_element_by_xpath('//a[@href="/rodrigues_a91/"]')
    pagina.click()

    time.sleep(3)
    seguidores = driver.find_element_by_xpath('//a[@href="/rodrigues_a91/followers/"]')
    seguidores.click()

    time.sleep(5)

    element = []

    for i in range(30):
        element = driver.find_elements_by_xpath('//div[@class="PZuss"]/li')
        element[-1].click()
        time.sleep(2)

    listaDePerfis = driver.find_elements_by_xpath('//div[@class="PZuss"]/li')
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
                    
    jsonNicks = {'nicks':listaDeNicks}
    driver.quit()

    return jsonNicks