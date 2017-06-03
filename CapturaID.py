############################################################# IMPORT ##########################################################################
from lxml import html
import requests

############################################### DECLARACAO DE VARIAVEIS #######################################################################
#mes_str = str(escolher_mes)
#ano_str = str(escolher_ano)

page = requests.get(str('http://freemeteo.com.br/clima/quintana/historico/historico-por-mes/?gid=3451950&station=22891&month=5&year=2017&language=portuguesebr&country=brazil'))
tree = html.fromstring(page.content)

a = 0
Coluna = 1
Linha = 1
linkbruto = []
############################################### PRINTS RECOLHIDOS PELO WEBBOT ###############################################################
Novo = open('links.csv','w')


while (Coluna < 7):
    print ("Coluna %d" % Coluna)
    print "Linha | Cidade | ID"
    while Linha < 21:					
        linkbruto.append(str(tree.xpath('id("content")/div[3]/div[8]/div/ul[%d]/li[%d]/a/@href' % (Coluna,Linha) )))#linkbrutolin.append(str(tree.xpath('/li[%d]/a/@href' % Linha )))
        link = linkbruto[a].split("/")
        #0- 1- clima [2]-NOME DA CIDADE 3-clima-atual 4-local 5-?gid=3450253&language=portuguesebr&country=brazil
        aux = str(Linha) + ' | ' + str(link[2]) + ' | ' + str(link[5])+ ("\n")
        Novo.write(aux)
        print str(aux)
        Linha += 1
        a += 1
    Linha = 1
    Coluna += 1


Novo.close()