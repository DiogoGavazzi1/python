import os

arquivo_excel = 'automacao.xlsx'

# Verifique se o arquivo existe no diretório atual
if not os.path.exists(arquivo_excel):
    print(f"Arquivo não encontrado no diretório atual: {os.getcwd()}")
else:
    print(f"Arquivo encontrado: {os.path.abspath(arquivo_excel)}")