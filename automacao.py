from selenium import webdriver
from datetime import date
import pandas

navegador = webdriver.Chrome()
navegador.get('https://www.google.com/')

tabela = pandas.read_excel('commodities.xlsx')

for linha in tabela.index:

    produto = tabela.loc[linha, 'Produto']
    produto = produto.replace("ó", "o").replace("ã", "a").replace("á", "a").replace(
    "ç", "c").replace("ú", "u").replace("é", "e")

    navegador.get(f'https://www.melhorcambio.com/{produto}-hoje')
    cotacao = navegador.find_element('xpath', '//*[@id="comercial"]').get_attribute('value')
    cotacao = cotacao.replace('.', '').replace(',', '.')
    cotacao = float(cotacao)

    tabela.loc[linha, 'Preço Atual'] = cotacao

print(tabela)

tabela["Comprar"] = tabela["Preço Atual"] < tabela["Preço Ideal"]
print(tabela)

data_atual = date.today()

tabela.to_excel(f'commodities_{data_atual}.xlsx', index=False)
navegador.quit()