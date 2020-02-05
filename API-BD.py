# Importando a Biblioteca PyMysql, requests e array
import mysql.connector
import requests
import json

# Conectando a base de dados 'veiculos'
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='veiculos'
)
cursor = conexao.cursor(buffered=True)

#fazendo consulta na tabela veiculos e selecionado os ids, Ao todo são 739 ids, mas coloquei os 5 primeiros.
cursor.execute("select id_veiculo from veiculos limit 5") 

data_inicio = input( 'Digite a data de inicio que deseja consultar (ex: AAAA-MM-DD):' )
data_fim = input( 'Digite a data de fim que deseja consultar (ex: AAAA-MM-DD): ' )

#Aqui armazeno os 5 ids da consulta nessa lista (veiculo =[])
veiculos = []
for x in cursor:
    veiculos.append(x)
    
    #Aqui pego os 5 ids e jogo na url da api para pega os dados de json de cada id.
    for y in veiculos:
        req = requests.get(
            f'http://backend.rassystem.com.br/app/v1/api/veiculos/{y[0]}/rastreio?dataInicio={data_inicio}T12:00:00-03:00&dataFim={data_fim}T12:00:00-03:00',
            auth=('aboliveira', 'alison00'))
        dados = json.loads(req.text)
        
        #Aqui faço a iteração dos resultados do json, so preciso desses 4 dados da api (idveiculo, data, latitude e longitude)
        for i in dados['features']:
            idveiculo = i['properties']['idVeiculo']
            #print('IdVeiculo...:', idveiculo)
            data = i['properties']['data']
            #print('Data...:', data)
            latitude = i['geometry']['coordinates'][0]
            #print('Latitude...:', latitude)
            longitude = i['geometry']['coordinates'][1]
            #print('Longitude...:', longitude)
            #print('\n')
            
            #Faço a inserção dos dados em outra tabela (log2)
            insert_query = "INSERT INTO log2(idveiculo, datas, latitude, longitude) VALUES ('" + str(idveiculo ) + "','" + data + "','" + str( latitude ) + "','" + str( longitude ) + "')"
            print( insert_query )
            cursor.execute(insert_query)
            
            conexao.commit()
             
            
            #OBS: Quando coloco para imprimir o insert_query, todos os 5 ids são impressos na tela.
            #Mas se colocar o cursor.execute(insert_qery) com ta ai, so imprimi o 1º id e so salva esse 1º no banco.
            #Como fazer para imprimir e salvar no banco de dados todos os ids que eu colocar la na consulta?
