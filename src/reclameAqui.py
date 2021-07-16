
from selenium import webdriver
from bs4 import BeautifulSoup
import time


class ReclameAqui:
    def __init__(self):
        self.url = 'https://www.reclameaqui.com.br/ranking/'
        self.driver = webdriver.Chrome(
            executable_path='C:/Users/CONSISTE/Downloads/chromedriver.exe')
        self.documents = []

    def verificarRepeticaoEmpresa(self):
        time.sleep(4)
        self.nome = self.driver.find_element_by_xpath(
            '//h1[@class="short-name"]').text.strip()
        for documento in self.documents:
            if documento['empresa'] == self.nome:
                return True

        return False

    def extrairEstatisticas(self):
        time.sleep(3)
        painelDeNotas = self.driver.find_element_by_id('reputation')
        html_painel = painelDeNotas.get_attribute('outerHTML')
        soup_painel = BeautifulSoup(html_painel, 'html.parser')

        detalhes = list(soup_painel.stripped_strings)
        self.docAtual = {'empresa': self.nome,
                         'notaPrincipal': detalhes[7],
                         'periodo': detalhes[9],
                         detalhes[10]: detalhes[11],
                         detalhes[12]: detalhes[13],
                         detalhes[14]: detalhes[15],
                         detalhes[16]: detalhes[17],
                         detalhes[18]: detalhes[19],
                         detalhes[20]: detalhes[21],
                         detalhes[22]: detalhes[23],
                         detalhes[24]: detalhes[25]}

    def extrairSobre(self):
        sobre = self.driver.find_element_by_xpath(
              '//*[@id="about"]/div/ul/li[1]').text
        self.docAtual.update({'sobre': sobre})

    def extrairComentarios(self):
        maisComentarios = self.driver.find_element_by_id(
          'box-complaints-read-all')
        linkComentarios = maisComentarios.get_attribute('href')
        self.driver.execute_script(f'window.open("{linkComentarios}")')
        time.sleep(4)
        self.driver.switch_to.window(self.driver.window_handles[-1])

        listaComentarios = self.driver.find_elements_by_xpath(
            '//ul[@class="complain-list"]/li[@class="ng-scope"]')
        comentarios = []
        for comentario in listaComentarios:
            html_comentario = comentario.get_attribute('outerHTML')
            soup_comentario = BeautifulSoup(html_comentario, 'html.parser')
            dados = soup_comentario.find_all('p')
            jsonComentario = {'titulo': dados[0].text,
                              'comentario': dados[1].text}
            comentarios.append(jsonComentario)

        self.docAtual.update({'comentarios': comentarios})
        #print(self.docAtual)

        self.documents.append(self.docAtual)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(5)

    def selecionarEmpresa(self, qtdEmpresas):
      for cont in range(qtdEmpresas):
          time.sleep(3)
          empresa = self.driver.find_elements_by_xpath(
              '//a[@class="business-name ng-binding ng-scope"]')[cont]
          link = empresa.get_attribute("href")
          self.driver.execute_script(f'window.open("{link}")')
          self.driver.switch_to.window(self.driver.window_handles[-1])
          time.sleep(3)
          jaExiste = self.verificarRepeticaoEmpresa()
          if jaExiste == True:
              self.driver.close()
              self.driver.switch_to.window(self.driver.window_handles[-1])
              continue
          else:
              self.extrairEstatisticas()
              self.extrairSobre()
              self.extrairComentarios()

    def minerar(self):
        self.driver.get(self.url)
        time.sleep(3)
        aceitarCookies = self.driver.find_element_by_id(
            'onetrust-accept-btn-handler')
        aceitarCookies.click()
        empresas = self.driver.find_elements_by_xpath(
            '//a[@class="business-name ng-binding ng-scope"]')
        qtdEmpresas = len(empresas) + 1
        self.selecionarEmpresa(qtdEmpresas)
        self.driver.quit()
        return self.documents
        
if __name__ == '__main__':
  minerador = ReclameAqui()
  documents = minerador.minerar()
