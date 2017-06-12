#encoding: utf-8
#encoding: iso-8859-1
#encoding: win-1252
################################################################ IMPORT ##############################################################################
from lxml import html
import requests
####################################################### DECLARACAO DE VARIAVEIS #######################################################################
Linha = 977
a = 0
cont = 2
regiao = ""
regiaosite = []
nome_cien_site = []

div = []
cic = []
rep = []
habit = []
adap = []
alt = []

fil = []
for_limb = []
sup = []
consist = []
nerv = []
comp = []

inf = []
peri = []

tip_fruto = []
obs = []
####################################################### DESENVOLVIMENTO ###############################################################################
#---------------------------------------------------INTERACAO DO USUARIO-------------------------------------------------------------------------------
#regiao = raw_input('Digite a Sigla da Região\n(S- Sul\nSE- Sudeste\nNE- Nordeste\nN- Norte\nCO- Centro-Oeste)\n').decode('utf-8')
nome_cien = raw_input('Digite o nome cientifico da planta-daninha\n').decode('utf-8')
#Cnidoscolus urens
#-------------------------------------------------CONDICAO DOENCA OU INSETO----------------------------------------------------------------------------
while Linha <= 1400:
	page = requests.get(str('http://agrofit.agricultura.gov.br/agrofit_cons/!ap_planta_detalhe_cons?p_id_planta_daninha=%d' % Linha))
	tree = html.fromstring(page.content)
	nome_cien_site = str(tree.xpath('id("N1")/table[1]/tr/td[2]/input/@value'))
	print str(nome_cien_site)
	if str(nome_cien) in "*"+str(nome_cien_site)+"*":
		div.append(str(tree.xpath('id("N2")/table[1]/tr[3]/td/table/tr/td/table/tr[2]/td[2]/input/@value')))
		cic.append(str(tree.xpath('id("N2")/table[1]/tr[3]/td/table/tr/td/table/tr[3]/td[2]/input/@value')))
		rep.append(str(tree.xpath('id("N2")/table[1]/tr[3]/td/table/tr/td/table/tr[4]/td[2]/input/@value')))
		habit.append(str(tree.xpath('id("N2")/table[1]/tr[3]/td/table/tr/td/table/tr[5]/td[2]/input/@value')))
		adap.append(str(tree.xpath('id("N2")/table[1]/tr[3]/td/table/tr/td/table/tr[6]/td[2]/input/@value')))
		alt.append(str(tree.xpath('id("N2")/table[1]/tr[3]/td/table/tr/td/table/tr[7]/td[2]/input/@value')))

		fil.append(str(tree.xpath('id("N2")/table[1]/tr[4]/td/table/tr/td/table/tr[2]/td[2]/input/@value')))
		for_limb.append(str(tree.xpath('id("N2")/table[1]/tr[4]/td/table/tr/td/table/tr[3]/td[2]/input/@value')))
		sup.append(str(tree.xpath('id("N2")/table[1]/tr[4]/td/table/tr/td/table/tr[4]/td[2]/input/@value')))
		consist.append(str(tree.xpath('id("N2")/table[1]/tr[4]/td/table/tr/td/table/tr[5]/td[2]/input/@value')))
		nerv.append(str(tree.xpath('id("N2")/table[1]/tr[4]/td/table/tr/td/table/tr[6]/td[2]/input/@value')))
		comp.append(str(tree.xpath('id("N2")/table[1]/tr[4]/td/table/tr/td/table/tr[7]/td[2]/input/@value')))

		inf.append(str(tree.xpath('id("N2")/table[1]/tr[5]/td/table/tr/td/table/tr[2]/td[2]/input/@value')))

		tip_fruto.append(str(tree.xpath('id("N2")/table[1]/tr[6]/td/table/tr/td/table/tr[2]/td[2]/input/@value')))
		obs.append(str(tree.xpath('id("N2")/table[2]/tr/td/table/tr[1]/td/textarea/text()')))

		carac_plant = str('INFORMAÇÕES DA PLANTA\n\nDivisão: ' + str(div) + '\nCiclo: ' + str(cic) + '\nPropagação: ' + str(rep) + '\nHabitat: ' + str(habit) + '\nAdaptação: ' + str(adap) + '\nAltura(cm): ' + str(alt) + "\n").decode('utf-8')
		carac_folha =  str('\nINFORMAÇÕES DA FOLHA\n\nFilotaxia: ' + str(fil) + '\nFormato do Limbo: ' + str(for_limb) + '\nSuperfície: ' + str(sup) + '\nConsistencia: ' + str(consist) + '\nNervação: ' + str(nerv) + '\nComprimeto: ' + str(comp) + "\n").decode('utf-8')
		floruto = str('\nFLOR, FRUTO E OBSERVAÇÃO\nInflorecência: ' + str(inf) +' | '+'Tipo do Fruto: ' + str(tip_fruto) + '\nObrservação: ' + str(obs)).decode('utf-8')
		esp = '_________________________________________________________________________________________________________________________________________'
		print carac_plant
		print carac_folha
		print floruto
		print esp
		break
		#Linha += 1
		#a += 1
	else:
		Linha += 1