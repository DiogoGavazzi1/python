from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import openpyxl

numero_oab = 259155
planilha_dados_consulta = openpyxl.load_workbook('automacao.xlsx')
pagina_processos = planilha_dados_consulta['processos']

# Iniciar o navegador
driver = webdriver.Chrome()
driver.get("https://pje-consulta-publica.tjmg.jus.br/")

try:
    # Inserir número da OAB
    campo_numero_oab = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='fPP:Decoration:numeroOAB']"))
    )
    campo_numero_oab.send_keys(numero_oab)

    # Selecionar UF
    selecao_uf = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//select[@id='fPP:Decoration:estadoComboOAB']"))
    )
    Select(selecao_uf).select_by_visible_text('SP')

    # Clicar no botão Pesquisar
    botao_pesquisar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='fPP:searchProcessos']"))
    )
    botao_pesquisar.click()

    # Clicar nos links para abrir os processos
    links_abrir_processos = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[@title='Ver Detalhes']"))
    )

    # Coletar dados de cada processo
    dados_coletados = []
    janela_principal = driver.current_window_handle

    for link in links_abrir_processos:
        link.click()
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)

        for janela in driver.window_handles:
            if janela != janela_principal:
                driver.switch_to.window(janela)

                try:
                    # Extrair número do processo
                    elementos = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='propertyView ']//div[@class='col-sm-12 ']"))
                    )
                    numero_processo = elementos[0].text if elementos else "N/A"

                    # Extrair participantes
                    nome_dos_participantes = driver.find_elements(By.XPATH, "//tbody[contains(@id,'processoPartesPoloAtivoResumidoList:tb')]//span[@class='text-bold']")
                    lista_participantes = [participante.text for participante in nome_dos_participantes]

                    # Adicionar dados
                    if len(lista_participantes) == 1:
                        dados_coletados.append([numero_oab, numero_processo, lista_participantes[0]])
                    else:
                        dados_coletados.append([numero_oab, numero_processo, ','.join(lista_participantes)])
                except Exception as e:
                    print(f"Erro ao coletar dados: {e}")

                driver.close()
                driver.switch_to.window(janela_principal)

    # Adicionar dados na planilha
    for dado in dados_coletados:
        pagina_processos.append(dado)

    planilha_dados_consulta.save('automacao.xlsx')

except Exception as e:
    print(f"Erro no processo: {e}")
finally:
    print("Processo concluido com sucesso!!")
    driver.quit()
   
