from lxml import html
import requests
import pymongo

####################################################### DECLARACAO DE VARIAVEIS #######################################################################
Linha = 977
a = 0
cont = 2
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
especiais01 = [['\\xc0', 'À'], ['\\xc1', 'Á'],	['\\xc2', 'Â'],	['\\xc3', 'Ã'],	['\\xc4', 'Ä'],	['\\xc7', 'Ç'],	['\\xc8', 'È'],	['\\xc9', 'É'],	['\\xca', 'Ê'],	['\\xcb', 'Ë'],	['\\xcc', 'Ì'],	['\\xcd', 'Í'],	['\\xce', 'Î'],	['\\xcf', 'Ï'],	['\\xd1', 'Ñ'],	['\\xd2', 'Ò'],	['\\xd3', 'Ó'],	['\\xd4', 'Ô'],	['\\xd5', 'Õ'],	['\\xd6', 'Ö'],	['\\xd9', 'Ù'],	['\\xda', 'Ú'],	['\\xdb', 'Û'],	[
    '\\xdc', 'Ü'],	['\xe0', 'à'],	['\\xe2', 'â'],	['\\xe3', 'ã'],	['\xe4', 'ä'],	['\\xe7', 'ç'],	['\\xe8', 'è'],	['\\xe9', 'é'],	['\\xea', 'ê'],	['\\xeb', 'ë'],	['\\xec', 'ì'],	['\\xed', 'í'],	['\\xee', 'î'],	['\\xef', 'ï'],	['\\xf1', 'ñ'],	['\\xf2', 'ò'],	['\\xf3', 'ó'],	['\\xf4', 'ô'],	['\\xf5', 'õ'],	['\\xf6', 'ö'],	['\\xf9', 'ù'],	['\\xfa', 'ú'],	['\\xfb', 'û'],	['\\xfc', 'ü'],	['\\xfd', 'ÿ']]
####################################################### DESENVOLVIMENTO ###############################################################################
# ---------------------------------------------------INTERACAO DO USUARIO-------------------------------------------------------------------------------
nome_cien = raw_input(
    'Digite o nome cientifico da planta-daninha\n').lower().capitalize()
n_nome_cient = str(nome_cien)
# Cnidoscolus urens
# -------------------------------------------------CONDICAO DOENCA OU INSETO----------------------------------------------------------------------------
for x in especiais01:
    if x[1] in nome_cien:
        n_nome_cient = str.replace(n_nome_cient, x[1], str(x[0]))

conexao = pymongo.MongoClient("localhost", 27017)
db = conexao["MongoDB_Samuel_01"]

Novo = open('PRAGAS COBWEB - Planta-Daninha(%s).csv' % (nome_cien), 'w')
while Linha <= 1400:
    page = requests.get(str(
        'http://agrofit.agricultura.gov.br/agrofit_cons/!ap_planta_detalhe_cons?p_id_planta_daninha=%d' % Linha))
    tree = html.fromstring(page.content)
    nome_cien_site = str(tree.xpath('id("N1")/table[1]/tr/td[2]/input/@value'))
    # print str(nome_cien_site)
    if str(nome_cien) in "*"+str(nome_cien_site)+"*":
        div = tree.xpath(
            'id("N2")/table[1]/tr[3]/td/table/tr/td/table/tr[2]/td[2]/input/@value')
        cic = tree.xpath(
            'id("N2")/table[1]/tr[3]/td/table/tr/td/table/tr[3]/td[2]/input/@value')
        rep = tree.xpath(
            'id("N2")/table[1]/tr[3]/td/table/tr/td/table/tr[4]/td[2]/input/@value')
        habit = tree.xpath(
            'id("N2")/table[1]/tr[3]/td/table/tr/td/table/tr[5]/td[2]/input/@value')
        adap = tree.xpath(
            'id("N2")/table[1]/tr[3]/td/table/tr/td/table/tr[6]/td[2]/input/@value')
        alt = tree.xpath(
            'id("N2")/table[1]/tr[3]/td/table/tr/td/table/tr[7]/td[2]/input/@value')

        fil = tree.xpath(
            'id("N2")/table[1]/tr[4]/td/table/tr/td/table/tr[2]/td[2]/input/@value')
        for_limb = tree.xpath(
            'id("N2")/table[1]/tr[4]/td/table/tr/td/table/tr[3]/td[2]/input/@value')
        sup = tree.xpath(
            'id("N2")/table[1]/tr[4]/td/table/tr/td/table/tr[4]/td[2]/input/@value')
        consist = tree.xpath(
            'id("N2")/table[1]/tr[4]/td/table/tr/td/table/tr[5]/td[2]/input/@value')
        nerv = tree.xpath(
            'id("N2")/table[1]/tr[4]/td/table/tr/td/table/tr[6]/td[2]/input/@value')
        comp = tree.xpath(
            'id("N2")/table[1]/tr[4]/td/table/tr/td/table/tr[7]/td[2]/input/@value')

        inf = tree.xpath(
            'id("N2")/table[1]/tr[5]/td/table/tr/td/table/tr[2]/td[2]/input/@value')

        tip_fruto = tree.xpath(
            'id("N2")/table[1]/tr[6]/td/table/tr/td/table/tr[2]/td[2]/input/@value')
        obs = tree.xpath(
            'id("N2")/table[2]/tr/td/table/tr[1]/td/textarea/text()')
# --------------------------------------------------------TRATAMENTO DO XPATH------------------------------------------------------------------------
        if (len(str(div)) > 2) and (len(str(cic)) > 2) and (len(str(rep)) > 2) and (len(str(habit)) > 2) and (len(str(adap)) > 2) and (len(str(alt)) > 2) and (len(str(fil)) > 2) and (len(str(for_limb)) > 2) and (len(str(sup)) > 2) and (len(str(consist)) > 2) and (len(str(nerv)) > 2) and (len(str(comp)) > 2) and (len(str(inf)) > 2) and (len(str(tip_fruto)) > 2) and (len(str(obs)) > 2):
            div = str(div[0].strip('\n\t').encode(
                'utf-8')) if div != [] else ""
            if div == '[]':
                div == 'NÃO REGISTRADO'
            cic = str(cic[0].strip('\n\t').encode(
                'utf-8')) if cic != [] else ""
            if cic == '[]':
                cic = 'NÃO REGISTRADO'
            rep = str(rep[0].strip('\n\t').encode(
                'utf-8')) if rep != [] else ""
            if rep == '[]':
                rep = 'NÃO REGISTRADO'
            habit = str(habit[0].strip('\n\t').encode(
                'utf-8')) if habit != [] else ""
# if habit == '[]':
#	habit ='NÃO REGISTRADO'
            adap = str(adap[0].strip('\n\t').encode(
                'utf-8')) if adap != [] else ""
            if adap == '[]':
                adap = 'NÃO REGISTRADO'
            alt = str(alt[0].strip('\n\t').encode(
                'utf-8')) if alt != [] else ""
            if alt == '[]':
                alt = 'NÃO REGISTRADO'
            fil = str(fil[0].strip('\n\t').encode(
                'utf-8')) if fil != [] else ""
            if fil == '[]':
                fil = 'NÃO REGISTRADO'
            for_limb = str(for_limb[0].strip('\n\t').encode(
                'utf-8')) if for_limb != [] else ""
            if for_limb == '[]':
                for_limb = 'NÃO REGISTRADO'
            sup = str(sup[0].strip('\n\t').encode(
                'utf-8')) if sup != [] else ""
            if sup == '[]':
                sup = 'NÃO REGISTRADO'
            consist = str(consist[0].strip('\n\t').encode(
                'utf-8')) if consist != [] else ""
            if consist == '[]':
                consist = 'NÃO REGISTRADO'
            nerv = str(nerv[0].strip('\n\t').encode(
                'utf-8')) if nerv != [] else ""
            if nerv == '[]':
                nerv = 'NÃO REGISTRADO'
            comp = str(comp[0].strip('\n\t').encode(
                'utf-8')) if comp != [] else ""
            if comp == '[]':
                comp = 'NÃO REGISTRADO'
            inf = str(inf[0].strip('\n\t').encode(
                'utf-8')) if inf != [] else ""
            if inf == '[]':
                inf = 'NÃO REGISTRADO'
            tip_fruto = str(tip_fruto[0].strip('\n\t').encode(
                'utf-8')) if tip_fruto != [] else ""
            if tip_fruto == '[]':
                tip_fruto = 'NÃO REGISTRADO'
            obs = str(obs[0].strip('\n\t').encode(
                'utf-8')) if obs != [] else ""
            if obs == '[]':
                obs = 'NÃO REGISTRADO'
# -------------------------------------------------------- ESTRUTURA E IMPRESSÃO------------------------------------------------------------------------
        carac_plant = str('INFORMAÇÕES DA PLANTA\n\nDivisão: ' + str(div) + '\nCiclo: ' + str(cic) + '\nPropagação: ' + str(
            rep) + '\nHabitat: ' + str(habit) + '\nAdaptação: ' + str(adap) + '\nAltura(cm): ' + str(alt) + "\n")  # .decode('utf-8')
        carac_folha = str('\nINFORMAÇÕES DA FOLHA\n\nFilotaxia: ' + str(fil) + '\nFormato do Limbo: ' + str(for_limb) + '\nSuperfície: ' + str(
            sup) + '\nConsistencia: ' + str(consist) + '\nNervação: ' + str(nerv) + '\nComprimeto: ' + str(comp) + "\n")  # .decode('utf-8')
        floruto = str('\nFLOR, FRUTO E OBSERVAÇÃO\nInflorecência: ' + str(inf) + ' | ' +
                      'Tipo do Fruto: ' + str(tip_fruto) + '\nObrservação: ' + str(obs))  # .decode('utf-8')
        esp = '\n_________________________________________________________________________________________________________________________________________'
        tudo = str(carac_plant) + str(carac_folha) + str(floruto) + str(esp)

        collection = (db.plant_dan.update(
            {"linha": str(Linha),
             "divisao": str(div)},
            {"divisao": str(div),
             "ciclo": str(cic),
             "propagacao": str(rep),
             "habitat": str(habit),
             "adaptacao": str(adap),
             "altura(cm)": str(alt),
             "filotaxia": str(fil),
             "form_limbo": str(for_limb),
             "superficie": str(sup),
             "consistencia": str(consist),
             "nervacao": str(nerv),
             "comprimento": str(comp),
             "inflorecencia": str(inf),
             "tip_fruto": str(tip_fruto),
             "observacao": str(obs)}, upsert=True))

        print(str(tudo))
        Novo.write(str(tudo))
        break
    else:
        Linha += 1
Novo.close()
