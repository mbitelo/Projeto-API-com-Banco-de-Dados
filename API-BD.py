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

cursor.execute("select id_veiculo from todos_veiculos limit 5")

data_inicio = input( 'Digite a data de inicio que deseja consultar (ex: AAAA-MM-DD):' )
data_fim = input( 'Digite a data de fim que deseja consultar (ex: AAAA-MM-DD): ' )

veiculos = []
for x in cursor:
    veiculos.append(x)
    for y in veiculos:
        req = requests.get(
            f'http://backend.rassystem.com.br/app/v1/api/veiculos/{y[0]}/rastreio?dataInicio={data_inicio}T12:00:00-03:00&dataFim={data_fim}T12:00:00-03:00',
            auth=('aboliveira', 'alison00'))
        dados = json.loads(req.text)
        for i in dados['features']:
            idveiculo = i['properties']['idVeiculo']
            print('IdVeiculo...:', idveiculo)
            data = i['properties']['data']
            print('Data...:', data)
            latitude = i['geometry']['coordinates'][0]
            print('Latitude...:', latitude)
            longitude = i['geometry']['coordinates'][1]
            print('Longitude...:', longitude)
            print('\n')
            query = (
                'INSERT INTO log2(idveiculo, datas, latitude, longitude) VALUES ("%s", %s, "%s", "%s")')
            var = idveiculo, data, latitude, longitude
            cursor.execute(query, var)
            conexao.commit()