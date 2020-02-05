import mysql.connector
import requests
import json

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='veiculos'
)
cursor = conexao.cursor()
req = requests.get(
    'http://backend.rassystem.com.br/app/v1/api/veiculos/14249/rastreio?dataInicio=2020-01-20T12:00:00-03:00&dataFim=2020-01-21T12:00:00-03:00',
    auth=('aboliveira', 'alison00') )
dados = json.loads( req.text )

for i in dados['features']:
    idveiculo = i['properties']['idVeiculo']
    print( 'IdVeiculo...:', idveiculo )

    data = i['properties']['data']
    print( 'Data...:', data )

    latitude = i['geometry']['coordinates'][0]
    print( 'Latitude...:', latitude )

    longitude = i['geometry']['coordinates'][1]
    print( 'Longitude...:', longitude )

    print( '\n')

    cursor.executemany("INSERT INTO log2 (idveiculo, datas, latitude, longitude) VALUES (%s, %s, %s, %s)", idveiculo, data, longitude, latitude)
    #var = (idveiculo, data, latitude, longitude))

conexao.commit()
