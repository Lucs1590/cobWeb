#encoding: utf-8
#encoding: iso-8859-1
#encoding: win-1252

################################################################ IMPORT ##############################################################################
from lxml import html
import requests



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


####################################################### DESENVOLVIMENTO ###############################################################################
#http://agrofit.agricultura.gov.br/agrofit_cons/!ap_praga_detalhe_cons?p_id_cultura_praga=2417		Min registro
#http://agrofit.agricultura.gov.br/agrofit_cons/!ap_praga_detalhe_cons?p_id_cultura_praga=6264		Max registro
#page = requests.get(str('http://agrofit.agricultura.gov.br/agrofit_cons/!ap_praga_detalhe_cons?p_id_cultura_praga=2417'))
#tree = html.fromstring(page.content)

tipo = "Inseto" # raw_input('Tipo (Inseto ou Doença): ').lower().capitalize().decode('utf-8')
cultura = "Arroz" # raw_input('Cultura: ').encode('utf-8')


while Linha < 5079:
	page = requests.get(str('http://agrofit.agricultura.gov.br/agrofit_cons/!ap_praga_detalhe_cons?p_id_cultura_praga=%d' % Linha))
	tree = html.fromstring(page.content)

	tiposite=(str(tree.xpath('id("N1")/table[1]/tr[1]/td[2]/input/@value')[0]))
	culturasite=(str(tree.xpath('id("N1")/table[1]/tr[3]/td[2]/input/@value')))
	print cultura + ":" + culturasite + ":" + culturasite.encode("utf-8")

	if (str(tipo) in "*"+str(tiposite)+"*"):

		if (str(cultura) in "*"+str(culturasite)+"*"):
			#TIPO QUE ESTA NO SITE    // 6 LINHAS ACIMA
			nome_cien.append(str(tree.xpath('id("N1")/table[1]/tr[2]/td[2]/input/@value')))
			#CULTURA                  // 7 LINHAS ACIMA
			desc.append(str(tree.xpath('id("N2")/table/tr[3]/td/textarea/text()')))
			sintoma.append(str(tree.xpath('id("N2")/table/tr[5]/td/textarea/text()')))
			bioecologia.append(str(tree.xpath('id("N2")/table/tr[7]/td/textarea/text()')))
			controle.append(str(tree.xpath('id("N2")/table/tr[9]/td/textarea/text()')))


			cab = str(Linha) + ' | ' + str(tiposite) + ' | ' + str(nome_cien[0]) + ' | ' + str(culturasite) + "\n\n"
			inf = 'Descricao: '+ str(desc).decode('utf-8') + "\n\n" + 'Sintomas: ' + str(sintoma[a]).decode('utf-8') + "\n\n" +'Bioecologia: ' + str(bioecologia[a]).decode('utf-8') + "\n\n" + 'Controle: ' + str(controle[a]).decode('utf-8') + "\n\n"
			space = "________________________________________________________________________________________________________________________________________________________________\n"
			print str(cab) + str(inf) + str(space)
			Linha += 1
			a += 1

		else:
			Linha += 1
			#a += 1