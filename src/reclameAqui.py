
from selenium import webdriver
from bs4 import BeautifulSoup
import time


class ReclameAqui:
    def __init__(self, pathToDriver = None):
        self.driver = webdriver.Remote("http://selenium:4444/wd/hub", desired_capabilities={'browserName':'firefox'})
        #self.driver = webdriver.Chrome(executable_path=pathToDriver)
        self.documents = []

    def verificarRepeticaoEmpresa(self):
        time.sleep(10)
        self.nome = self.driver.find_element_by_xpath(
            '//h1[@class="short-name"]').text.strip()
        for documento in self.documents:
            if documento['empresa'] == self.nome:
                return True

        return False

    def extrairEstatisticas(self):
        time.sleep(5)
        self.driver.find_element_by_id('reputation-tab-5').click()
        time.sleep(7)
        painelDeNotas = self.driver.find_element_by_id('reputation')
        html_painel = painelDeNotas.get_attribute('outerHTML')
        soup_painel = BeautifulSoup(html_painel, 'html.parser')

        detalhes = list(soup_painel.stripped_strings)
        self.docAtual = {'empresa': self.nome,
                         'nota_principal': detalhes[7],
                         'periodo': detalhes[9],
                         'qtd_reclamacoes': detalhes[11],
                         'qtd_respondidas': detalhes[13],
                         'percentual_reclamacoes_respondidas': detalhes[15],
                         'percentual_voltariam_a_fazer_negocio': detalhes[17],
                         'percentual_indice_de_solucao': detalhes[19],
                         'nota_consumidor': detalhes[21],
                         'qtd_nao_respondidas': detalhes[23],
                         'qtd_avaliadas': detalhes[25]}

    def extrairSobre(self):
        sobre = self.driver.find_element_by_xpath(
              '//*[@id="about"]/div/ul/li[1]').text
        self.docAtual.update({'sobre': sobre})

    def extrairComentarios(self):
        time.sleep(5)
        maisComentarios = self.driver.find_element_by_id(
          'box-complaints-read-all')
        linkMaisComentarios = maisComentarios.get_attribute('href')
        self.driver.execute_script(f'window.open("{linkMaisComentarios}")')
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(20)
        qtdCometarios = len(self.driver.find_elements_by_xpath('//ul[@class="complain-list"]/li[@class="ng-scope"]/a'))
        comentarios = []

        for cont in range(qtdCometarios):
            comentario = self.driver.find_elements_by_xpath('//ul[@class="complain-list"]/li[@class="ng-scope"]/a')[cont]
            linkComentario = comentario.get_attribute('href')
            self.driver.execute_script(f'window.open("{linkComentario}")')
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(7)
            
            tituloComentario = self.driver.find_element_by_xpath('//h1[@class="ng-binding"]').text
            descricaoComentario = self.driver.find_element_by_xpath('//p[@ng-bind-html="reading.complains.description|textModerateDecorator"]').text
            jsonComentario = {'titulo': tituloComentario, 'descricao': descricaoComentario}
            
            comentarios.append(jsonComentario)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(8)
                
        self.docAtual.update({'comentarios': comentarios})

        self.documents.append(self.docAtual)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[-1])

    def selecionarEmpresa(self, qtdEmpresas):
      for cont in range(qtdEmpresas):
          time.sleep(7)
          empresa = self.driver.find_elements_by_xpath(
              '//a[@class="business-name ng-binding ng-scope"]')[cont]
          link = empresa.get_attribute("href")
          self.driver.execute_script(f'window.open("{link}")')
          self.driver.switch_to.window(self.driver.window_handles[-1])
          time.sleep(7)
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
        url = 'https://www.reclameaqui.com.br/ranking/'
        self.driver.get(url)
        time.sleep(3)
        aceitarCookies = self.driver.find_element_by_id(
            'onetrust-accept-btn-handler')
        aceitarCookies.click()
        empresas = self.driver.find_elements_by_xpath(
            '//a[@class="business-name ng-binding ng-scope"]')
        qtdEmpresas = len(empresas)
        self.selecionarEmpresa(qtdEmpresas)
        self.driver.quit()
        return self.documents
    
    def minerarEmpresa(self, empresa):
        url = 'https://www.reclameaqui.com.br/'
        self.driver.get(url)
        time.sleep(5)
        
        aceitarCookies = self.driver.find_element_by_id(
            'onetrust-accept-btn-handler')
        aceitarCookies.click()
        buscarEmpresa = self.driver.find_element_by_xpath('//input[@class="form-search input-auto-complete-search"]')
        buscarEmpresa.send_keys(empresa)
        time.sleep(7)
        
        paginaEmpresa = self.driver.find_element_by_xpath('//div[@class="vueperslides__track-inner"]/a[1]')
        link = paginaEmpresa.get_attribute("href")
        self.driver.execute_script(f'window.open("{link}")')
        self.driver.switch_to.window(self.driver.window_handles[-1])
        time.sleep(5)
        
        self.nome = self.driver.find_element_by_xpath(
            '//h1[@class="short-name"]').text.strip()
        self.extrairEstatisticas()
        self.extrairSobre()
        self.extrairComentarios()
        self.driver.quit()
        return self.documents
    
if __name__ == '__main__':
    minerador = ReclameAqui('C:/Users/CONSISTE/Downloads/chromedriver.exe')
    print(minerador.minerarEmpresa("kinvo"))
        