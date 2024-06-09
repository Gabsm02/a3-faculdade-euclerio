import matplotlib.pyplot as plt
import numpy as np
import openpyxl
import pandas as pd
import requests as req
from bs4 import BeautifulSoup as bs
import csv

response = req.get('https://www.mercadolivre.com.br/ofertas#nav-header')

html = response.text
soup = bs(html, 'html.parser')


tabela = soup.findAll(class_='promotion-item__description')

produtos = []


for item in tabela:
    if item.text > '15% OFF':
        cells = item.findAll(class_=['andes-money-amount__fraction', 'promotion-item__title',
                                     'promotion-item__produtos-text', 'promotion-item__discount-text'])
        if len(cells) >= 4:
            desconto_string = cells[2].text.strip()
            numero_desconto = ''.join(filter(str.isdigit, desconto_string))

            desconto_inteiro = int(numero_desconto)
            # print(cells)
            produto = {
                'Nome': cells[3].text.strip(),
                'Preco original': cells[1].text.strip(),
                'Desconto': desconto_inteiro,
                'Valor Final': cells[0].text.strip()
            }
            produtos.append(produto)


# Ordenando em ordem alfabética

produtos_ordernados = sorted(produtos, key=lambda x: x['Nome'])

# criando um arquivo

# Nome do arquivo CSV
nome_arquivo = 'a3_euclerio.csv'

# Campos do CSV
campos = ['Nome', 'Preco original', 'Desconto', 'Valor Final']

# Escrevendo para o arquivo CSV
with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
    escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=campos)
    escritor_csv.writeheader()
    escritor_csv.writerows(produtos_ordernados)

print(f"Arquivo CSV '{nome_arquivo}' gerado com sucesso!")

# criando arquivo excel


df = pd.DataFrame(produtos_ordernados)

valores_finais = [float(produto['Valor Final'])
                  for produto in produtos_ordernados]


print('Dados Estatísticos:')

# Média dos valores
media = np.mean(valores_finais)
print(f'Média dos valores de Desconto é: R$ {media:.2f}')

# Mediana dos valores
mediana = np.median(valores_finais)
print(f'Mediana dos valores de Desconto é: R$ {mediana:.2f}')

# Desvio padrão dos valores
desvio_padrao = np.std(valores_finais)
print(f'Desvio padrão dos valores de Desconto é: R$ {desvio_padrao:.2f}')

# Variância dos valores
variancia = np.var(valores_finais)
print(f'Variância dos valores de Desconto é: R$ {variancia:.2f}')


# Boxplot
plt.figure(figsize=(8, 6))
plt.boxplot(valores_finais, vert=True)
plt.title('Boxplot')
plt.xlabel('Desconto')

# Linha para a média
plt.axhline(y=media, color='r', linestyle='--', label=f'Média: R$ {media:.2f}')

# Linha para a mediana
plt.axhline(y=mediana, color='g', linestyle='--',
            label=f'Mediana: R$ {mediana:.2f}')

# Linha para o desvio padrão
plt.axhline(y=media + desvio_padrao, color='b', linestyle='--',
            label=f'Desvio Padrão: R$ {desvio_padrao:.2f}')

# Linha para a variância
plt.axhline(y=media - desvio_padrao, color='y', linestyle='--',
            label=f'Variância: R$ {variancia:.2f}')

# Mostrar a legenda
plt.legend()

plt.show()
