#encoding: utf-8
#encoding: iso-8859-9
#encoding: win-1252

################################################################ IMPORT ##############################################################################
from lxml import html
import requests
import csv
import sys
import pymongo

####################################################### DECLARACAO DE VARIAVEIS #######################################################################
a = 0
Linha = 2417
nome_cien = []
desc =[]
sintoma = []
bioecologia = []
controle = []
tiposite = ""
culturasite = ""
#especiais = [['ã','\\xe3'], ['á','\\xe1'], ['â','\\xe2'], ['ç','\\xe7'], ['é','\\xe9'], ['ê','\\xea'], ['í','\\xed'], ['ó','\\xf3'], ['ô','\\xf4'], ['ú','\\xfa']]
especiais01 = [['\\xc0','À'],['\\xc1','Á'],	['\\xc2','Â'],	['\\xc3','Ã'],	['\\xc4','Ä'],	['\\xc7','Ç'],	['\\xc8','È'],	['\\xc9','É'],	['\\xca','Ê'],	['\\xcb','Ë'],	['\\xcc','Ì'],	['\\xcd','Í'],	['\\xce','Î'],	['\\xcf','Ï'],	['\\xd1','Ñ'],	['\\xd2','Ò'],	['\\xd3','Ó'],	['\\xd4','Ô'],	['\\xd5','Õ'],	['\\xd6','Ö'],	['\\xd9','Ù'],	['\\xda','Ú'],	['\\xdb','Û'],	['\\xdc','Ü'],	['\xe0','à'],	['\\xe2','â'],	['\\xe3','ã'],	['\xe4','ä'],	['\\xe7','ç'],	['\\xe8','è'],	['\\xe9','é'],	['\\xea','ê'],	['\\xeb','ë'],	['\\xec','ì'],	['\\xed','í'],	['\\xee','î'],	['\\xef','ï'],	['\\xf1','ñ'],	['\\xf2','ò'],	['\\xf3','ó'],	['\\xf4','ô'],	['\\xf5','õ'],	['\\xf6','ö'],	['\\xf9','ù'],	['\\xfa','ú'],	['\\xfb','û'],	['\\xfc','ü'],	['\\xfd','ÿ']]
####################################################### DESENVOLVIMENTO ###############################################################################
#http://agrofit.agricultura.gov.br/agrofit_cons/!ap_praga_detalhe_cons?p_id_cultura_praga=2417		Min registro
#http://agrofit.agricultura.gov.br/agrofit_cons/!ap_praga_detalhe_cons?p_id_cultura_praga=6264		Max registro

#--------------------------------------------------------INTERACAO-------------------------------------------------------------------------------------

tipo = str(raw_input('Tipo (Inseto ou Doença): ').lower().capitalize())
cultura = str(raw_input('Cultura: ').lower().capitalize())
n_cultura = str(cultura)

for x in especiais01:
	if x[1] in cultura:
		n_cultura = str.replace(n_cultura,x[1],str(x[0]))


conexao = pymongo.MongoClient("localhost", 27017)
db = conexao["MongoDB_Samuel_01"]

Novo = open('PRAGAS COBWEB - %s(%s).csv'% (tipo,cultura), 'w')
#---------------------------------------------------------CRAWLER----------------------------------------------------------------------------------------
while Linha < 6300:
	page = requests.get(str('http://agrofit.agricultura.gov.br/agrofit_cons/!ap_praga_detalhe_cons?p_id_cultura_praga=%d' % Linha))
	tree = html.fromstring(page.content)

	tiposite=tree.xpath('id("N1")/table[1]/tr[1]/td[2]/input/@value')
	culturasite=tree.xpath('id("N1")/table[1]/tr[3]/td[2]/input/@value')

	#print cultura.encode('utf-8') + ":" + culturasite + ":" + str(n_cultura).encode('utf-8')
	#print tipo + ":" + tiposite

	tiposite = str(tiposite[0].strip('\n\t').encode('utf-8')) if tiposite != [] else "NÃO REGISTRADO"
	culturasite = str(culturasite[0].strip('\n\t').encode('utf-8')) if culturasite != [] else "NÃO REGISTRADO"

	print tipo + ":" + tiposite + "| linha: " + str(Linha)

	if (str(tipo) in "*"+str(tiposite)+"*"):
		if (str(n_cultura) in "*"+str(culturasite)+"*"):
			#TIPO QUE ESTA NO SITE    // 6 LINHAS ACIMA
			nome_cien = tree.xpath('id("N1")/table[1]/tr[2]/td[2]/input/@value')
			n_nome_cien = nome_cien
			#CULTURA                  // 7 LINHAS ACIMA
			desc = tree.xpath('id("N2")/table/tr[3]/td/textarea/text()')
			n_desc = desc
			sintoma = tree.xpath('id("N2")/table/tr[5]/td/textarea/text()')
			n_sintoma = sintoma
			bioecologia = tree.xpath('id("N2")/table/tr[7]/td/textarea/text()')
			n_bioecologia = bioecologia
			controle = tree.xpath('id("N2")/table/tr[9]/td/textarea/text()')
			n_controle = controle
#---------------------------------------------------------------TRATAMENTO DO XPATH---------------------------------------------------------------------------
			if (len(str(n_cultura)) > 2) or (len(str(n_nome_cien)) > 2) or (len(str(n_desc)) > 2) or (len(str(n_sintoma)) > 2) or (len(str(n_bioecologia)) > 2) or (len(str(n_controle)) > 2) or (len(str(tiposite)) > 2):
				n_cultura = str(n_cultura[0].strip('\n\t').encode('utf-8')) if n_cultura != [] else "NÃO REGISTRADO"
				n_nome_cien = str(n_nome_cien[0].strip('\n\t').encode('utf-8')) if n_nome_cien != [] else "NÃO REGISTRADO"
				n_desc = str(n_desc[0].strip('\n\t').encode('utf-8')) if n_desc != [] else "NÃO REGISTRADO"
				n_sintoma = str(n_sintoma[0].strip('\n\t').encode('utf-8')) if n_sintoma != [] else "NÃO REGISTRADO"
				n_bioecologia = str(n_bioecologia[0].strip('\n\t').encode('utf-8')) if n_bioecologia != [] else "NÃO REGISTRADO"
				n_controle = str(n_controle[0].strip('\n\t').encode('utf-8')) if n_controle != [] else "NÃO REGISTRADO"
#---------------------------------------------------------------ESTRUTURA E IMPRESSÃO---------------------------------------------------------------------------
			cab = str(Linha) + ' | ' + str(tiposite) + ' | ' + str(n_nome_cien) + ' | ' + str(culturasite) + "\n\n"
			inf = 'Descricao: '+ str(n_desc) + "\n\n" + 'Sintomas: ' + str(n_sintoma) + "\n\n" +'Bioecologia: ' + str(n_bioecologia) + "\n\n" + 'Controle: ' + str(n_controle) + "\n\n"
			space = "_____________________________________________________________________________________________________________________________________________\n"
			Novo.write(str(cab) + str(inf) + str(space))

			collection = (db.pragas.update(
                                {"tipo" : str(tiposite),
                                "cultura" : str(culturasite)},
                                {"tipo" : str(tiposite),
                                "nome_cientifico" : str(n_nome_cien),
                                "cultura" : str(culturasite),
                                "descricao" : str(n_desc),
                                "sintomas" : str(n_sintoma),
                                "bioecologia" : str(n_bioecologia),
                                "controle" : str(n_controle)},
                                upsert = True))

			print str(cab) + str(inf) + str(space)
			Linha += 1
			a += 1

		else:
			Linha += 1
	else:
                Linha += 1
print("_____________________________________________________________FINALIZADO_____________________________________________________________________")
Novo.close()
