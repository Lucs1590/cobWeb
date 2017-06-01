################################################################ IMPORT ##########################################################################
from lxml import html
import requests
# encoding: utf-8
# encoding: iso-8859-1
# encoding: win-1252

############################################# DANDO VALOR AO XPATH COM *CIDADE MES *ANO #########################################################
print ("Digite o nome da cidade (sem caracteres especiais).")
escolher_cidade = raw_input('Cidade: ').lower()
escolher_mes = int(input("Mes: "))
escolher_ano = int(input("Ano: "))

####################################################### DECLARACAO DE VARIAVEIS #######################################################################
page = requests.get(str('http://freemeteo.com.br/clima/%s/historico/historico-por-mes/?gid=3451950&station=22868&month=%d&year=%d&language=portuguesebr&country=brazil') % (escolher_cidade,escolher_mes,escolher_ano))
tree = html.fromstring(page.content)

a = 0
Linha = 1
dia = []
temp_min_dia = []
temp_max_dia = []
vent_const_max = []
rajad_vent_max = []
prec_dia_total = []
descricao = []

############################################### PRINTS RECOLHIDOS PELO WEBBOT ###############################################################
#Novo = open('Hist_Tempo.csv','w')

print "Linha (Dia) | Temp. Min. | Temp. Max. | Vento Constante Max. | Corrente de Vento Max. | Precipitacao Total | Descricao"

while Linha < 32:
    #####dia.append(str(tree.xpath('//html/body/div[1]/div[2]/div[2]/div[3]/div[1]/div[3]/div/table/tbody/tr[1]/td[1]/a/text()' % Linha )))
    temp_min_dia.append(str(tree.xpath('id("monthly-archive")/div[3]/div/table/tbody/tr[%d]/td[2]/text()' % Linha )))
    temp_max_dia.append(str(tree.xpath('id("monthly-archive")/div[3]/div/table/tbody/tr[%d]/td[3]/text()' % Linha)))
    vent_const_max.append(str(tree.xpath('id("monthly-archive")/div[3]/div/table/tbody/tr[%d]/td[4]/text()' % Linha)))
    rajad_vent_max.append(str(tree.xpath('id("monthly-archive")/div[3]/div/table/tbody/tr[%d]/td[5]/text()' % Linha)))
    prec_dia_total.append(str(tree.xpath('id("monthly-archive")/div[3]/div/table/tbody/tr[%d]/td[6]/text()' % Linha)))
    descricao.append(str(tree.xpath('id("monthly-archive")/div[3]/div/table/tbody/tr[%d]/td[8]/text()' % Linha)))
    aux = str(Linha) + ' | ' + str(temp_min_dia[a].decode('utf-8')) + ' | ' + str(temp_max_dia[a].decode('utf-8')) + ' | ' +  str(vent_const_max[a].decode('utf-8')) + ' | ' +  str(rajad_vent_max[a].decode('utf-8')) + ' | ' +  str(prec_dia_total[a].decode('utf-8')) + ' | ' +  str(descricao[a].decode('utf-8') + '\n')
    print str(aux)
    Linha += 1
    a += 1