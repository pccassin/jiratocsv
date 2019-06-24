# import de modulos/libs
import json
import csv
import requests

##########################################################################################

# Api-endpoint do JIRA
URL = "< your JIRA API endpoint - URL da API da sua instancia do JIRA >"
# Paramentros da Request / Request Params
PARAMS = {'jql':'project = MyTeam AND statusCategory in (Done) AND issuetype not in (Sub-task, Epic)','maxResults':'600','expand':'changelog'}

# Envio de request do tipo GET, passando dados para autenticação
s = requests.Session()
s.auth = ('user', 'password') # alterar dados de usuário acesso quando utilizar
r = s.get(url = URL, params = PARAMS, verify=False)
#print (r.status_code)

# Extrasão do response da request no formato json para um dicionário Python
data = r.text
parsedData = json.loads(data)
issues = parsedData['issues']

# Dicionários para guardar o cabeçalho e as linhas que vão para csv
row = []

# Criar arquivo csv e prepara para a escrita ** Caso arquivo já exista vai inserir após ultima linha **
csvFile = open('C:/<path where you want to save export>/export.csv', 'at', newline='')
csvwriter = csv.writer(csvFile)

#Looping sobre todos os issues retornados na busca JQL
for issue in issues:

    # Captura a chave da issue, a lista de campos e o log de transições (history)
    key = issue['key']
    fields = issue['fields']
    changes = issue['changelog']['histories']

    # Adiciona valor a lista "row" que será gravada como uma linha do CSV
    row.append(key)

    # Tipo do issue
    issuetype = fields['issuetype']['name']
    row.append(issuetype)

    # Data de criação da issue
    created = fields['created']
    # Data da última atualização da issue
    updated = fields['updated']

    row.append(created)
    row.append(updated)

    for change in changes:
        # Data da transição
        changeDate = change['created']
        items = change['items']
        for item in items:
            if item['field'] == 'status':
                # Coluna em que a história estava
                changeFrom = item['fromString']
                # Coluna para que a história foi movida
                changeTo = item['toString']
                #if changeTo == 'Entregue' or changeTo == 'Done':
                row.append(changeDate)
                row.append(changeFrom)
                row.append(changeTo)
    # Grava linha para o CSV
    csvwriter.writerow(row)

    # Limpa dados para capturar proxima linha
    row.clear()

# Fecha arquivo após inserir
csvFile.close()
print("Concluido - Done")
