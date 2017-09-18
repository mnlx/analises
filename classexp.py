from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import datetime





class Analise():

    aaa = 1

    def __init__(self,dominio,psswrd):
        print('started')


        # print(os.environ['GOOGLE_CHROME_BIN'])
        # webdriver.ChromeOptions.binary_location = "/app/.apt/usr/bin/google-chrome"

        self.driver = webdriver.Chrome()

        self.URL = "http://{0}.emailmanager.com".format(dominio)
        self.del_completa = False
        self.psswrd = psswrd
    def click(self,id_class):
        try:
            e = self.driver.find_element_by_class_name(id_class)
        except:
            e.click()
        e.click()

    def xpath(self,locator ,isclass , classname ,n=0 ):
        # Função proucura elementos por meio de XPATH
        # Será necessário acrescentar mais locators (id,img,...)

        if n == 0:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//{0}[@{1}='{2}']".format(locator,isclass,classname))))
            return self.driver.find_element(By.XPATH, "//{0}[@{1}='{2}']".format(locator, isclass, classname))
        elif n>0:
            #Não há como esperar para uma lista carregar, portanto temos que procurar por um elemento apenas
            init = 1
            final = -1
            while init != final:
                init = len(self.driver.find_elements(By.XPATH, "//{0}[@{1}='{2}']".format(locator, isclass, classname)))
                time.sleep(1)
                final = len(self.driver.find_elements(By.XPATH, "//{0}[@{1}='{2}']".format(locator, isclass, classname)))
            return self.driver.find_elements(By.XPATH, "//{0}[@{1}='{2}']".format(locator, isclass, classname))

    def login(self):
        URL= self.URL
        self.driver.get(URL)
        self.country = 'Brasil'
        if '¿Olvidó su contraseña?' in self.driver.page_source:
            print('yes')
            self.country = 'Espanha'
        elif 'Did you forget your password?' in self.driver.page_source:
            self.country = 'USA'
        elem = self.driver.find_element_by_name("login")
        elem.clear()
        elem.send_keys("andre.duarte/admin")
        self.driver.execute_script("$('pass2').value = '{0}'".format(self.psswrd))

        """DEBUG:START"""
        self.driver.save_screenshot('/home/monolux/Heroku/debugss/ss1.png')
        """DEBUG:STOP"""
        # elem2 = self.driver.find_element_by_id('pass')
        # elem2.send_keys(self.psswrd)
        self.click('bt-gr-orange')
        """DEBUG:START"""
        self.driver.save_screenshot('/home/monolux/Heroku/debugss/ss2.png')
        """DEBUG:STOP"""
        time.sleep(8)


        try:
            elem = self.driver.find_elements_by_xpath(
                "//div[@class='x-btn app-btn orange add x-box-item x-toolbar-item x-btn-default-toolbar-medium x-noicon x-btn-noicon x-btn-default-toolbar-medium-noicon']")
            elem[0].click()
        except:
            print('all good')

        time.sleep(1)
        try:
            elem = self.driver.find_elements_by_xpath("//img[@class='x-tool-close']")
            elem[0].click()
        except:
            print('all good')

    def consolidado(self):
        def table_get(driver):
            elem = driver.find_elements_by_tag_name('td')
            return [str(x.text) for x in elem]

        def table_value(table_list, index):
            ind = table_list.index(index)
            visualstr = table_list[ind + 1]
            return float(visualstr.split('(')[1].split('%')[0].replace(',', '.'))

        URL = self.URL
        self.driver.get(URL + "/#Report/Consolidated")
        self.visua = []
        self.clicks = []
        time.sleep(7)
        for x in range(3):
            try:
                if x > 0:
                    elem = self.xpath('table', 'class', 'x-form-trigger-wrap', 1)
                    elem[0].click()
                    time.sleep(2)
                    elem = self.driver.find_elements_by_tag_name('li')
                    elem[x].click()
                    time.sleep(3)
                try:
                    elem = table_get(self.driver)
                    self.visua.append(table_value(elem, "total de visualizações"))
                    self.clicks.append(table_value(elem, "total de cliques"))
                except:
                    self.visua.append( "NaN") # caso não haja dados BR
                    self.clicks.append( "NaN") # caso não haja dados BR
                    pass
                try:
                    elem = table_get(self.driver)
                    self.visua.append(table_value(elem, "total views")) # para clientes americanos
                    self.clicks.append(table_value(elem, "total clicks")) # para clientes americanos
                except:
                    self.visua.append( "NaN") # caso não haja dados  US
                    self.clicks.append( "NaN") # caso não haja dados  US
                    pass

            except IndexError:
                print('No visualizations or click data for month {0}'.format(x))
        # print(self.visua)
        mean = []
        for x in self.visua:
            if type(x)==float:
                mean.append(x)
        self.visua_mean = sum(mean)/len(mean)

        mean = []
        for x in self.clicks:
            if type(x)==float:
                mean.append(x)
        self.clicks_mean = sum(mean)/len(mean)

    def acc_info(self):

        URL = self.URL
        self.driver.get(URL + "/#ControlPanel/Domain")
        time.sleep(5)

        # Obtendo informações do dominio

        elem = self.driver.find_elements_by_tag_name('img')
        self.valido = 0
        for x in elem:
            if 'ic_valido.png' in x.get_attribute('src'):
                self.valido = self.valido + 1

        # SPF e DKIM

        self.driver.get(URL + "/#ControlPanel/AccountSender")
        time.sleep(5)
        elem = self.driver.find_elements_by_tag_name('td')
        a = [x.text for x in elem]
        while '' in a:
            a.remove('')
        while 'Verificada' in a:
            a.remove('Verificada')
        while 'Verificar\nEditar\nApagar' in a:
            a.remove('Verificar\nEditar\nApagar')
        while 'Editar\nApagar' in a:
            a.remove('Editar\nApagar')
        while 'Não verificada' in a:
            a.remove('Não verificada')
        while 'Verified' in a:
            a.remove('Verified')
        while 'Verified\nEdit\nDelete' in a:
            a.remove('Verified\nEdit\nDelete')
        while 'Editr\nDelete' in a:
            a.remove('Edit\nDelete')
        while 'Not verified' in a:
            a.remove('Not verified')

        self.spf = []
        self.dkim = []
        for x in range(int(len(a) / 4)):
            self.spf.append(a[x * 4 + 2])
            self.dkim.append(a[x * 4 + 3])

        ################################### Qualidade e tamanho da base
        self.driver.get(URL + "/#Dashboard")
        time.sleep(7)
        try:
            elem = self.driver.find_elements_by_xpath("//img[@class='x-tool-close']")
            elem[0].click()
        except:
            pass

        elem = self.driver.find_elements_by_class_name('number ')
        self.cadast = elem[0].text
        elem = self.driver.find_element_by_class_name('quality_letter')
        self.quali = elem.text


    def specific_report(self,num_inter):
        def get_errors(driver):
            value_checker = ['Endereço inativo', 'Usuário desconhecido', 'Domínio desconhecido', 'Permanente']
            value_checker = [x[0:8] for x in value_checker]
            value_checker_en = ['Invalid address', 'Unknown user', 'Unknown domain', 'Permanent']
            value_checker_en = [x[0:8] for x in value_checker_en]

            elem = driver.find_elements_by_tag_name('text')
            error_list = [x.text for x in elem]
            error_list_checker = [x.text[0:8] for x in elem]
            values = []
            values_en = []

            for k in value_checker:
                if k in error_list_checker:
                    ind = error_list_checker.index(k)
                    value = error_list[ind]

                    values.append(float(value.split('(')[0].split(' ')[-2]))
                    values.append(float(value.split('(')[1].split('%')[0].replace(',', '.')))
                else:
                    values.append(0)
                    values.append(0)

            for k in value_checker_en:
                if k in error_list_checker:
                    ind = error_list_checker.index(k)
                    value = error_list[ind]

                    values_en.append(float(value.split('(')[0].split(' ')[-2]))
                    values_en.append(float(value.split('(')[1].split('%')[0].replace(',', '.')))
                else:
                    values_en.append(0)
                    values_en.append(0)
            if values_en.count(0) > values.count(0):
                return values
            elif values_en.count(0) < values.count(0):
                return values_en
            else:
                return values
        ###################################### Listas, erros, cancelamentos e denuncias
        URL = self.URL
        self.driver.get(URL + '/#CampaignList')
        time.sleep(4)
        elem = self.driver.find_elements_by_xpath("//input[@class='x-form-field x-form-empty-field x-form-text']")
        elem[1].click()
        time.sleep(3)
        elem = self.driver.find_elements_by_xpath("//li[@class='x-boundlist-item']")
        for x in elem:
            if x.get_attribute('textContent') == 'Interrompido':
                x.click()

                break
            if x.get_attribute('textContent') == 'Interrupted':
                x.click()

                break
        time.sleep(8)
        elem = self.driver.find_elements_by_xpath("//div[@class='status red']")
        print(num_inter)
        hover = ActionChains(self.driver).move_to_element(elem[num_inter])
        hover.perform()
        time.sleep(2)
        elem = self.driver.find_elements_by_xpath("//li[@class='ac summary']")
        elem[num_inter].click()
        time.sleep(1)
        elem = self.driver.find_elements_by_xpath("//td[@class = 'x-table-layout-cell ']")
        elemstr = [str(x.text) for x in elem]
        lst = ['Lista de inclusão', 'Lista de exclusão', 'Segmentação']
        self.lista = []
        for x in lst:
            if x in elemstr:

                self.lista.append(elem[elemstr.index(x) + 1].text)
            else:
                self.lista.append('nenhuma')

        listus = self.lista[0:2]
        if listus.count('nenhuma') == 3:
            self.lista = []
            lst = ['Inclusion list', 'Exclusion list', 'Segmentation']
            for x in lst:
                if x in elemstr:

                    self.lista.append(elem[elemstr.index(x) + 1].text)
                else:
                    self.lista.append('nenhuma')
        time.sleep(3)
        elem = self.driver.find_element_by_xpath("//div[@class = 'x-btn app-btn orange add x-box-item x-toolbar-item x-btn-default-toolbar-medium x-noicon x-btn-noicon x-btn-default-toolbar-medium-noicon']")  ##elem.click()
        elem.click()
        time.sleep(3)
        elem = self.driver.find_elements_by_xpath("//input[@class='x-form-field x-form-empty-field x-form-text']")
        hover = ActionChains(self.driver).move_to_element(elem[0])
        hover.perform()
        elem = self.driver.find_elements_by_xpath("//div[@class='status red']")
        hover = ActionChains(self.driver).move_to_element(elem[num_inter])
        hover.perform()
        elem = self.driver.find_elements_by_xpath("//li[@class='ac report']")
        elem[num_inter].click()
        time.sleep(8)
        elem = self.driver.find_element_by_tag_name('h1')
        try:
            self.campanha = ''.join(elem.text.split(':')[1:])
        except:
            self.campanha = ''.join(elem.text.split(':')[1:])
        elem = self.driver.find_elements_by_class_name('x-form-trigger-wrap')
        elem[4].click()
        time.sleep(2)
        # Aba de erros
        elem = self.driver.find_elements_by_class_name('x-grid-cell-inner')
        elem[16].click()
        time.sleep(3)
        self.erros = get_errors(self.driver)
        # Aba denúncias
        elem = self.driver.find_elements_by_class_name('x-form-trigger-wrap')
        elem[4].click()
        elem = self.driver.find_elements_by_class_name('x-grid-cell-inner')
        ind = [x.text for x in elem]
        try:
            elem[ind.index('Denúncias')].click()
        except:
            elem[ind.index('Complaints')].click()
        time.sleep(1)
        elem = self.driver.find_elements_by_class_name('x-grid-cell-inner')
        a = [a.text for a in elem]
        self.denuncias = a.count('Denúncia de Spam')
        denuncias_en = a.count('Reporting Spam')
        if self.denuncias != denuncias_en:
            if denuncias_en > self.denuncias:
                self.denuncias = denuncias_en
            elif self.denuncias > denuncias_en:
                pass
        # Aba cancelamento
        elem = self.driver.find_elements_by_class_name('x-form-trigger-wrap')
        elem[4].click()
        elem = self.driver.find_elements_by_class_name('x-grid-cell-inner')
        ind = [x.text for x in elem]
        try:
            elem[ind.index('Cancelamentos')].click()
        except:
            elem[ind.index('Cancellations')].click()
        time.sleep(1)
        elem = self.driver.find_elements_by_class_name('x-grid-cell-inner')
        a = [a.text for a in elem]
        self.cance = 0
        for p in a:
            if '@' in p:
                self.cance = self.cance + 1
            elif 'excluído' in p:
                self.cance = self.cance + 1
            elif 'removed' in p:
                self.cance = self.cance + 1

    def del_seg(self):
        # ----------------------------- removendo segmentação antiga

        URL = self.URL
        self.driver.get(URL + '/#DataMining')

        time.sleep(6)

        self.driver.execute_script(
            "document.getElementsByClassName('x-form-field x-form-text x-form-empty-field').item(2).value='(EMMr'")
        self.driver.execute_script(
            "document.getElementsByClassName('x-trigger-index-1 x-form-trigger x-form-search-trigger x-form-trigger-last x-unselectable').item(1).click()")
        self.driver.execute_script(
            "document.getElementsByClassName('x-trigger-index-1 x-form-trigger x-form-search-trigger x-form-trigger-last x-unselectable').item(1).click()")
        time.sleep(2)

        try:
            aaa = self.driver.find_elements_by_xpath("//span[@class = 'name']")
        except:
            self.del_completa = True
            return 'sem analises completadas'
        time.sleep(2)
        jk = [x.get_attribute('innerHTML')[0:5] for x in aaa]

        for x in jk:
            if x == '(EMMr':
                check = True
            else:
                check = False
                break

        if len(jk) == 0:
            check = False

        lll = jk.count('(EMMr')
        if check and lll!= 0:
            time.sleep(3)
            if jk.count('(EMMr') <= 6:
                for x in range(jk.count('(EMMr')):
                    elem = self.driver.find_element_by_xpath("//div[@class = 'icon-del']")
                    elem.click()

                    demo = self.driver.find_elements_by_css_selector("button.x-btn-center span.x-btn-inner")
                    print(demo[len(demo)-3].text)
                    if demo[len(demo)-3].text == "Assine agora mesmo":
                        self.driver.execute_script("document.getElementsByClassName('x-btn-center').item(12).click()")

                    else:
                        self.driver.execute_script("document.getElementsByClassName('x-btn-center').item(11).click()")
                    time.sleep(3)
        self.del_completa = True
        print('No previous segments to be deleted')

    def criar_seg(self, seg_num):
        ######## Criando segmentações
        URL = self.URL
        time.sleep(2)
        self.driver.get(URL + '/#DataMiningForm')

        NOME_SEG_LIST = ['(EMMr CI12M)', '(EMMr CI6M)', '(EMMr SI2010)']
        DIAS_SEG_LIST = [366, 180]

        # xp(self.driver, 'empty', 'class', 'x-form-field x-form-required-field x-form-text', 'list')
        time.sleep(5)
        self.driver.execute_script(
            "document.getElementsByClassName('x-form-field x-form-required-field x-form-text').item(0).value = '{0}';".format(
                NOME_SEG_LIST[seg_num]))
        time.sleep(0.5)
        self.driver.execute_script(
            "document.getElementsByClassName('x-trigger-index-0 x-form-trigger x-form-trigger-last x-unselectable').item(0).click(); ")
        time.sleep(1)
        self.driver.execute_script("document.getElementsByClassName('x-grid-cell-inner ').item(0).click();")

        if seg_num <= 1:
            self.driver.execute_script(
                "document.getElementsByClassName('x-trigger-index-0 x-form-trigger x-form-trigger-last x-unselectable').item(1).click(); ")
            time.sleep(0.1)
            self.driver.execute_script(
                "document.getElementsByClassName('x-grid-row x-grid-tree-node-leaf').item(16).click();")
            time.sleep(0.1)
            self.driver.execute_script(
                "document.getElementsByClassName('x-trigger-index-0 x-form-trigger x-form-trigger-last x-unselectable').item(2).click();")
            time.sleep(0.1)
            self.driver.execute_script(
                "document.getElementsByClassName('x-boundlist-item').item(2).click();")
            time.sleep(0.1)

            b = datetime.date.today() - datetime.timedelta(days=DIAS_SEG_LIST[seg_num])
            a = b.strftime("%Y-%m-%d")
            c = b.strftime("%d/%m/%Y")
            aaa = self.driver.find_elements_by_xpath("//td[@class = 'x-form-trigger-input-cell']")
            """DEBUG:START"""
            self.driver.save_screenshot('/home/monolux/Heroku/debugss/ss3.png')
            """DEBUG:STOP"""
            aaa[3].click()
            n = aaa[3]
            u = ActionChains(self.driver).move_to_element(aaa[3])
            u.perform()
            """DEBUG:START"""
            self.driver.save_screenshot('/home/monolux/Heroku/debugss/ss4.png')
            """DEBUG:STOP"""
            self.driver.execute_script(

            "document.getElementsByClassName('x-form-field x-form-text x-form-focus x-field-form-focus x-field-default-form-focus').item(0).value = '{0}'".format(c)


            )
            # aaa[3].send_keys(a)

            self.driver.execute_script(
               """ document.querySelectorAll("[name*='field-date']").item(0).value = '{0}'""".format(a))

            """DEBUG:START"""
            self.driver.save_screenshot('/home/monolux/Heroku/debugss/ss5.png')
            """DEBUG:STOP"""
            time.sleep(.5)
            aaa[2].click()
            aaa = self.driver.find_elements_by_xpath(
                "//div[@class='x-btn x-box-item x-toolbar-item x-btn-default-toolbar-large x-noicon x-btn-noicon x-btn-default-toolbar-large-noicon']")

            time.sleep(.5)
            """DEBUG:START"""
            self.driver.save_screenshot('/home/monolux/Heroku/debugss/ss6.png')
            """DEBUG:STOP"""
            aaa[0].click()
            time.sleep(.5)
            """DEBUG:START"""
            self.driver.save_screenshot('/home/monolux/Heroku/debugss/ss7.png')
            """DEBUG:STOP"""

        else:
            self.driver.execute_script(
                "document.getElementsByClassName('x-trigger-index-0 x-form-trigger x-form-trigger-last x-unselectable').item(1).click(); ")
            time.sleep(0.1)
            self.driver.execute_script(
                "document.getElementsByClassName('x-grid-row x-grid-tree-node-leaf').item(18).click();")
            time.sleep(0.1)
            self.driver.execute_script(
                "document.getElementsByClassName('x-trigger-index-0 x-form-trigger x-form-trigger-last x-unselectable').item(2).click();")
            time.sleep(0.1)
            self.driver.execute_script(
                "document.getElementsByClassName('x-boundlist-item').item(2).click();")
            time.sleep(0.1)
            """DEBUG:START"""
            self.driver.save_screenshot('/home/monolux/Heroku/debugss/ss9.png')
            """DEBUG:STOP"""
            aaa = self.driver.find_elements_by_xpath("//td[@class = 'x-form-trigger-input-cell']")
            aaa[3].click()
            # aaa[3].send_keys('01/01/2010')
            time.sleep(0.1)
            """DEBUG:START"""
            self.driver.save_screenshot('/home/monolux/Heroku/debugss/ss30.png')
            """DEBUG:STOP"""
            self.driver.execute_script(

            "document.getElementsByClassName('x-form-field x-form-text x-form-focus x-field-form-focus x-field-default-form-focus').item(0).value = '01/01/2010'"


            )
            """DEBUG:START"""
            self.driver.save_screenshot('/home/monolux/Heroku/debugss/ss10.png')
            """DEBUG:STOP"""
            self.driver.execute_script(
               """ document.querySelectorAll("[name*='field-date']").item(0).value = '2010-01-01'""")
            """DEBUG:START"""
            self.driver.save_screenshot('/home/monolux/Heroku/debugss/ss11.png')
            """DEBUG:STOP"""
            time.sleep(.5)
            aaa[2].click()
            time.sleep(.5)
            aaa = self.driver.find_elements_by_xpath(
                "//div[@class='x-btn x-box-item x-toolbar-item x-btn-default-toolbar-large x-noicon x-btn-noicon x-btn-default-toolbar-large-noicon']")
            aaa[0].click()
            time.sleep(.5)
            """DEBUG:START"""
            self.driver.save_screenshot('/home/monolux/Heroku/debugss/ss12.png')
            """DEBUG:STOP"""
            time.sleep(1)

            """DEBUG:START"""
            self.driver.save_screenshot('/home/monolux/Heroku/debugss/ss13.png')
            """DEBUG:STOP"""


    def seg_values(self):
        URL = self.URL
        self.driver.get(URL + '/#DataMining')
        time.sleep(5)
        """DEBUG:START"""
        self.driver.save_screenshot('/home/monolux/Heroku/debugss/ss20.png')
        """DEBUG:STOP"""
        print('ggg2')
        """DEBUG:START"""
        self.driver.save_screenshot('/home/monolux/Heroku/debugss/ss21.png')
        """DEBUG:STOP"""
        self.driver.execute_script("document.getElementsByClassName('x-form-field x-form-text x-form-empty-field').item(2).value='(EMMr'")
        time.sleep(1)
        print('ggg3')
        self.driver.execute_script("document.getElementsByClassName('x-trigger-index-1 x-form-trigger x-form-search-trigger x-form-trigger-last x-unselectable').item(1).click()")
        # self.driver.execute_script("document.getElementsByClassName('x-trigger-index-1 x-form-trigger x-form-search-trigger x-form-trigger-last x-unselectable').item(1).click()")
        time.sleep(3)

        aaa = self.driver.find_elements_by_xpath("//span[@class = 'name']")
        jkk = [o.get_attribute('innerHTML') for o in aaa]
        jk = [u.get_attribute('innerHTML')[0:5] for u in aaa]
        for x in jk:
            if x == '(EMMr':
                check = True
            else:
                check = False
                break
        a = []
        for x in range(3):
            if check:
                self.driver.execute_script("document.getElementsByClassName('icon-total icon-open-node').item({0}).click();".format(x))
                time.sleep(1.5)
                self.driver.execute_script("document.getElementsByClassName('x-grid-cell-inner ').item(0).click();")
                time.sleep(1.5)
                demo = self.driver.find_elements_by_css_selector("button.x-btn-center span.x-btn-inner")

                print(demo[len(demo) - 3].text)
                if demo[len(demo) - 3].text == "Calcular":
                    demo[len(demo) - 3].click()
                    # self.driver.execute_script("document.getElementsByClassName('x-btn-center').item(12).click()")
                else:
                    self.driver.execute_script("document.getElementsByClassName('x-btn-center').item(11).click();")
                time.sleep(7)
                aaa = self.driver.find_elements_by_xpath("//span[@class='number-blue']")
                try:
                    a.append(aaa[0].get_attribute('innerHTML'))
                except IndexError:
                    a.append('null')
                self.driver.execute_script("document.getElementsByClassName('x-tool-close').item(0).click();")
                time.sleep(1.5)
        self.segmen = ['a', 'a', 'a']
        for c in jkk:
            if c == '(EMMr CI6M)':
                self.segmen[0] = a[jkk.index(c)]
            elif c == '(EMMr CI12M)':
                self.segmen[1] = a[jkk.index(c)]
            elif c == '(EMMr SI2010)':
                self.segmen[2] = a[jkk.index(c)]
