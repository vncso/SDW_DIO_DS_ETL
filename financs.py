import pandas as pd
import numpy as np
import util


def converte_valor(valor):
    """
    Função para converter o dado referente ao valor extraído do CSV como texto para float
    :param valor: str numérico. Valor da operação financeira a ser convertido para float
    :return: float valor_final (valor convertido)
    """
    # verifica se o número é negativo (saídas/pagamentos)
    if '-' in valor:
        # caso valor tenha casa de milhar, formata para a conversão
        if len(dados['Valor']) > 6:
            valor = str(valor).strip().replace('-', '')
            valor = str(valor).replace('.', '')
            valor = str(valor).replace(',', '.')
        else:
            valor = str(valor).strip().replace('-' , '')
            valor = str(valor).replace(',', '.')
        valor_final = float(valor) * - 1

    # valores positivos (entradas/recebimentos)
    else:
        if len(valor) > 6:
            valor = str(valor).replace('.', '')
            valor = str(valor).strip().replace(',', '.') 
        else:
            valor = str(valor).strip().replace(',', '.')
        valor_final = float(valor)
    # se não tiver valor converte para zero
    if linha["Valor"] == '':
        valor_final = 0
    
    return valor_final

# leitura dos dados
dados = pd.DataFrame(pd.read_csv('extrato.csv', sep=';'))
print(dados.shape)
print(dados.head())
print(dados.columns)
print('Descrição:')
print(dados['Descrição'])
print(len(dados['Valor']))
print(dados.iterrows())

investimentos, resgate_investimento, dividendos, pix_enviado, pix_recebido, pagamentos = 0, 0, 0, 0, 0, 0
estorno, compras, saque, emprestimo, transferencia, renda, outros = 0, 0, 0, 0, 0, 0, 0

print(renda)

# itera as linhas importadas do CSV
for index, linha in dados.iterrows():
    # classifica o tipo de operação
    op = str(linha['Descrição']).split('-')
    op = op[0].strip()
    # chamada da função para conversão do valor
    valor = converte_valor(linha['Valor'])
    # classifica a operação com base nos dados em util.py
    if op in util.pix_recebido:
        pix_recebido += valor
    elif op in util.investimentos:
        investimentos += valor
    elif op in util.renda:
        renda += valor
    elif op in util.saque:
        saque += valor
    elif op in util.estorno:
        estorno += valor
    elif op in util.compras:
        compras += valor
    elif op in util.dividendos:
        dividendos += valor
    elif op in util.emprestimo:
        emprestimo += valor
    elif op in util.pagamentos:
        pagamentos += valor
    elif op in util.pix_enviado:
        pix_enviado += valor
    elif op in util.resgate_investimento:
        resgate_investimento += valor
    elif op in util.transferencia:
        transferencia += valor
    else:
        outros += valor       

# gera a carga que será exportada para o arquivo xlsx
carga = [['renda', renda], ['investimento', investimentos], ['resgate', resgate_investimento],
['dividendos', dividendos], ['pix enviado', pix_enviado], ['pix recebido', pix_recebido],
['pagamentos', pagamentos],  ['estornos', estorno], ['compras', compras], ['saques', saque],
['emprestimos', emprestimo], ['transf', transferencia], ['outros', outros]]

# gera o dataframe
arquivo = pd.DataFrame(carga, columns=['Tipo', 'Valor R$'])

# exportação para xlsx
arquivo.to_excel('teste.xlsx')
