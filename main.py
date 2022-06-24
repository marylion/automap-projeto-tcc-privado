# -*- coding: utf-8 -*-

# INÍCIO
__author__ = "Djalma Filho"
__stage__ = 'BETA'
__version__ = '6.14'
__subversion__ = '16.53'

# 1st and 2nd lines area special in python code
# TODO Implementar limpar_tda()
# TODO EPSG SER UM DROPDOWN COM AS OPÇÕES
# TODO FAZER VÁRIOS PROJETOS SÓ PRA TROCAR O POSICIONAMENTO DO NOME
# TODO FAZER VÁRIOS PROJETOS SÓ PRA MUDAR O TAMANHO DAS GRADES
# TODO DROPDOWN COM VARIAS ESCALAS PRÉ-PRONTAS
# TODO CHECKBOX + LABEL E ENTRY ESCALA PERSONALIZADA
# TODO TROCAR DE PROJETO SE AS GRANDE FICAREM POPULOSAS DEMAIS
# TODO SALVAR TODAS AS IMGS DE PRE-VIZUALIZACAO


""" CONCLUIDOS """
# ATIVAR / DESATIVAR: LIMITES, GLEBAS, ASSENTAMENTOS, ETC
# MAKE SURE TO ADD BUFFER 300 TO AREA DE LIMITACAO
# AJEITAR A OPTIONBOX DE .TXT E .SHP, ALGO DEU ERRADO


# Primeiramente, importar ARCPY.
print("Importando Arcpy...")
# import arcpy
print("Importando outras bibliotecas...")

# Pythons 2.7 tweaks
from functools import partial
import tkFileDialog as fd
from tkinter import messagebox
from tkinter import ttk

# Imports
import tkinter
import os
import glob
import random 
import string
import shutil
import ctypes
import subprocess
import getpass
import requests

# Ainda não usados
import re
import sys
import json
import time
import base64
import fnmatch


# Carregar Constantes, funções e projeto
print("Carregando Projeto...")


# Agarrada na Tela, Classe e Funções complementares não fundamentais.
class Grip:
    """Faz com que a Janela fica Agaravel em qualquer lugar."""

    def __init__ (self, parent, disable=None, releasecmd=None) :
        self.parent = parent
        self.root = parent.winfo_toplevel()

        self.disable = disable
        if type(disable) == 'str':
            self.disable = disable.lower()

        self.releaseCMD = releasecmd

        self.parent.bind('<Button-1>', self.relative_position)
        self.parent.bind('<ButtonRelease-1>', self.drag_unbind)

    def relative_position (self, event) :
        cx, cy = self.parent.winfo_pointerxy()
        geo = self.root.geometry().split("+")
        self.oriX, self.oriY = int(geo[1]), int(geo[2])
        self.relX = cx - self.oriX
        self.relY = cy - self.oriY

        self.parent.bind('<Motion>', self.drag_wid)

    def drag_wid (self, event) :
        cx, cy = self.parent.winfo_pointerxy()
        d = self.disable
        x = cx - self.relX
        y = cy - self.relY
        if d == 'x' :
            x = self.oriX
        elif d == 'y' :
            y = self.oriY
        self.root.geometry('+%i+%i' % (x, y))

    def drag_unbind (self, event) :
        self.parent.unbind('<Motion>')
        if self.releaseCMD != None :
            self.releaseCMD()



class Constantes:

    """Constantes necessarias para o projeto"""
  
    nomes_municipios = {'ABAETETUBA':'ABAETETUBA',
        'ABEL FIGUEIREDO':'ABEL FIGUEIREDO',
        'ACARÁ':'ACARA',
        'AFUÁ':'AFUA',
        'ÁGUA AZUL DO NORTE':'AGUA AZUL DO NORTE',
        'ALENQUER':'ALENQUER',
        'ALMEIRIM':'ALMEIRIM',
        'ALTAMIRA':'ALTAMIRA',
        'ANAJÁS':'ANAJAS',
        'ANANINDEUA':'ANANINDEUA',
        'ANAPU':'ANAPU',
        'AUGUSTO CORRÊA':'AUGUSTO CORREA',
        'AURORA DO PARÁ':'AURORA DO PARA',
        'AVEIRO':'AVEIRO',
        'BAGRE':'BAGRE',
        'BAIÃO':'BAIAO',
        'BANNACH':'BANNACH',
        'BARCARENA':'BARCARENA',
        'BELÉM':'BELEM',
        'BELTERRA':'BELTERRA',
        'BENEVIDES':'BENEVIDES',
        'BOM JESUS DO TOCANTINS':'BOM JESUS DO TOCANTINS',
        'BONITO':'BONITO',
        'BRAGANÇA':'BRAGANCA',
        'BRASIL NOVO':'BRASIL NOVO',
        'BREJO GRANDE DO ARAGUAIA':'BREJO GRANDE DO ARAGUAIA',
        'BREU BRANCO':'BREU BRANCO',
        'BREVES':'BREVES',
        'BUJARU':'BUJARU',
        'CACHOEIRA DO ARARI':'CACHOEIRA DO ARARI',
        'CACHOEIRA DO PIRIÁ':'CACHOEIRA DO PIRIA',
        'CAMETÁ':'CAMETA',
        'CANAÃ DOS CARAJÁS':'CANAA DOS CARAJAS',
        'CAPANEMA':'CAPANEMA',
        'CAPITÃO POÇO':'CAPITAO POCO',
        'CASTANHAL':'CASTANHAL',
        'CHAVES':'CHAVES',
        'COLARES':'COLARES',
        'CONCEIÇÃO DO ARAGUAIA':'CONCEICAO DO ARAGUAIA',
        'CONCÓRDIA DO PARÁ':'CONCORDIA DO PARA',
        'CUMARU DO NORTE':'CUMARU DO NORTE',
        'CURIONÓPOLIS':'CURIONOPOLIS',
        'CURRALINHO':'CURRALINHO',
        'CURUÁ':'CURUA',
        'CURUÇÁ':'CURUCA',
        'DOM ELISEU':'DOM ELISEU',
        'ELDORADO DO CARAJÁS':'ELDORADO DO CARAJAS',
        'FARO':'FARO',
        'FLORESTA DO ARAGUAIA':'FLORESTA DO ARAGUAIA',
        'GARRAFÃO DO NORTE':'GARRAFAO DO NORTE',
        'GOIANÉSIA DO PARÁ':'GOIANESIA DO PARA',
        'GURUPÁ':'GURUPÁ',
        'IGARAPÉ-AÇU':'IGARAPE-ACU',
        'IGARAPÉ-MIRI':'IGARAPE-MIRI',
        'INHANGAPI':'INHANGAPI',
        'IPIXUNA DO PARÁ':'IPIXUNA DO PARA',
        'IRITUIA':'IRITUIA',
        'ITAITUBA':'ITAITUBA',
        'ITUPIRANGA':'ITUPIRANGA',
        'JACAREACANGA':'JACAREACANGA',
        'JACUNDÁ':'JACUNDA',
        'JURUTI':'JURUTI',
        'LIMOEIRO DO AJURU':'LIMOEIRO DO AJURU',
        'MÃE DO RIO':'MAE DO RIO',
        'MAGALHÃES BARATA':'MAGALHAES BARATA',
        'MARABÁ':'MARABA',
        'MARACANÃ':'MARACANA',
        'MARAPANIM':'MARAPANIM',
        'MARITUBA':'MARITUBA',
        'MEDICILÂNDIA':'MEDICILANDIA',
        'MELGAÇO':'MELGACO',
        'MOCAJUBA':'MOCAJUBA',
        'MOJU':'MOJU',
        'MOJUÍ DOS CAMPOS':'MOJUI DOS CAMPOS',
        'MONTE ALEGRE':'MONTE ALEGRE',
        'MUANÁ':'MUANA',
        'NOVA ESPERANÇA DO PIRIÁ':'NOVA ESPERANCA DO PIRIA',
        'NOVA IPIXUNA':'NOVA IPIXUNA',
        'NOVA TIMBOTEUA':'NOVA TIMBOTEUA',
        'NOVO PROGRESSO':'NOVO PROGRESSO',
        'NOVO REPARTIMENTO':'NOVO REPARTIMENTO',
        'ÓBIDOS':'OBIDOS',
        'OEIRAS DO PARÁ':'OEIRAS DO PARA',
        'ORIXIMINÁ':'ORIXIMINA',
        'OURÉM':'OUREM',
        'OURILÂNDIA DO NORTE':'OURILANDIA DO NORTE',
        'PACAJÁ':'PACAJA',
        'PALESTINA DO PARÁ':'PALESTINA DO PARA',
        'PARAGOMINAS':'PARAGOMINAS',
        'PARAUAPEBAS':'PARAUAPEBAS',
        "PAU D'ARCO":"PAU D'ARCO",
        'PEIXE-BOI':'PEIXE-BOI',
        'PIÇARRA':'PICARRA',
        'PLACAS':'PLACAS',
        'PONTA DE PEDRAS':'PONTA DE PEDRAS',
        'PORTEL':'PORTEL',
        'PORTO DE MOZ':'PORTO DE MOZ',
        'PRAINHA':'PRAINHA',
        'PRIMAVERA':'PRIMAVERA',
        'QUATIPURU':'QUATIPURU',
        'REDENÇÃO':'REDENCAO',
        'RIO MARIA':'RIO MARIA',
        'RONDON DO PARÁ':'RONDON DO PARA',
        'RURÓPOLIS':'RUROPOLIS',
        'SALINÓPOLIS':'SALINOPOLIS',
        'SALVATERRA':'SALVATERRA',
        'SANTA BÁRBARA DO PARÁ':'SANTA BARBARA DO PARA',
        'SANTA CRUZ DO ARARI':'SANTA CRUZ DO ARARI',
        'SANTA IZABEL DO PARÁ':'SANTA ISABEL DO PARA',
        'SANTA LUZIA DO PARÁ':'SANTA LUZIA DO PARA',
        'SANTA MARIA DAS BARREIRAS':'SANTA MARIA DAS BARREIRAS',
        'SANTA MARIA DO PARÁ':'SANTA MARIA DO PARA',
        'SANTANA DO ARAGUAIA':'SANTANA DO ARAGUAIA',
        'SANTARÉM':'SANTAREM',
        'SANTARÉM NOVO':'SANTAREM NOVO',
        'SANTO ANTÔNIO DO TAUÁ':'SANTO ANTONIO DO TAUA',
        'SÃO CAETANO DE ODIVELAS':'SAO CAETANO DE ODIVELAS',
        'SÃO DOMINGOS DO ARAGUAIA':'SAO DOMINGOS DO ARAGUAIA',
        'SÃO DOMINGOS DO CAPIM':'SAO DOMINGOS DO CAPIM',
        'SÃO FÉLIX DO XINGU':'SAO FELIX DO XINGU',
        'SÃO FRANCISCO DO PARÁ':'SAO FRANCISCO DO PARA',
        'SÃO GERALDO DO ARAGUAIA':'SAO GERALDO DO ARAGUAIA',
        'SÃO JOÃO DA PONTA':'SAO JOAO DA PONTA',
        'SÃO JOÃO DE PIRABAS':'SAO JOAO DE PIRABAS',
        'SÃO JOÃO DO ARAGUAIA':'SAO JOAO DO ARAGUAIA',
        'SÃO SEBASTIÃO DA BOA VISTA':'SAO SEBASTIAO DA BOA VISTA',
        'SAPUCAIA':'SAPUCAIA',
        'SENADOR JOSÉ PORFÍRIO':'SENADOR JOSE PORFIRIO',
        'SOURE':'SOURE',
        'TAILÂNDIA':'TAILANDIA',
        'TERRA ALTA':'TERRA ALTA',
        'TERRA SANTA':'TERRA SANTA',
        'TOMÉ-AÇU':'TOME-ACU',
        'TRACUATEUA':'TRACUATEUA',
        'TRAIRÃO':'TRAIRAO',
        'TUCUMÃ':'TUCUMA',
        'TUCURUÍ':'TUCURUI',
        'ULIANÓPOLIS':'ULIANOPOLIS',
        'URUARÁ':'URUARA',
        'VIGIA':'VIGIA',
        'VISEU':'VISEU',
        'VITÓRIA DO XINGU':'VITORIA DO XINGU',
        'XINGUARA':'XINGUARA'
    }

    WKID = sistema_de_referencia_de_coordenadas = {'GCS_SIRGAS_2000':4674,
        'GCS_SIRGAS' 							:4170,
        'GCS_WGS_1984' 							:4326,
        'GCS_South_American_1969' 				:4618,
        'GCS_SAD_1969_96' 						:5527,
        'SAD_1969_UTM_Zone_21S' 				:29191,
        'SAD_1969_UTM_Zone_22S' 				:29192,
        'SAD_1969_UTM_Zone_23S' 				:29193,
        'SAD_1969_96_UTM_Zone_21S' 				:5531,
        'SAD_1969_96_UTM_Zone_22S' 				:5858,
        'SAD_1969_96_UTM_Zone_23S' 				:5533,
        'SIRGAS_2000_UTM_Zone_21S' 				:31981,
        'SIRGAS_2000_UTM_Zone_22S' 				:31982,
        'SIRGAS_2000_UTM_Zone_23S' 				:31983,
        'South_America_Lambert_Conformal_Conic' :102015,
        }
    
    lLong = [ 'LONG' 		, 9, 0, 0 	]
    lText = [ 'TEXT' 		, 0, 0, 254 ]
    lDate = [ 'DATE' 		, 0, 0, 0 	]
    lDouble=[ 'DOUBLE' 	    , 0, 0, 0 	]

    operacoes_da_tabela_de_atributos = {0:{'OBJECTID':lLong},
        1 :{ 'id'			:lLong},
        2 :{ 'interessad'	:lText},
        3 :{ 'imovel'		:lText},
        4 :{ 'ano'			:lLong},
        5 :{ 'processo'		:lLong},
        6 :{ 'municipio'	:lText},
        7 :{ 'parcela'		:lText},
        8 :{ 'situacao'		:lText},
        9 :{ 'georref'		:lText},
        10:{ 'data'			:lDate},
        11:{ 'complement'	:lText},
        12:{ 'created_us'	:lText},
        13:{ 'created_da'	:lDate},
        14:{ 'last_edite'	:lDate},
        15:{ 'last_edi_1'	:lDate},
        16:{ 'Shape_Leng'	:lDouble},
        17:{ 'Shape_Area'	:lDouble},
        }

    unicodes_lowercase = ['\xc3\xa1',
        '\xc3\xa9','\xc3\xad',
        '\xc3\xb3','\xc3\xba',
        '\xc3\xa3','\xc3\xb5',
        '\xc3\xa2','\xc3\xaa',
        '\xc3\xae','\xc3\xb4',
        '\xc3\xbb','\xc3\xa7',
        ]

    unicodes_upercase = ['\xc3\x81',
        '\xc3\x89','\xc3\x8d',
        '\xc3\x93','\xc3\x9a',
        '\xc3\x83','\xc3\x95',
        '\xc3\x82','\xc3\x8a',
        '\xc3\x8e','\xc3\x94',
        '\xc3\x9b','\xc3\x87',
        ]

    definition_query_mapa_situacao = {1:"{}nmSede = \'{}\'",
        2:"{}\"nmMun\" <> \'{}\'",
        3:"{}\"nmMun\" = \'{}\'",
        }

    nome_das_camadas  = {'carta indice':"CARTA_INDICE_IBGE_DSG",
        'zee':"ZEE_2010",
        'mzee':"MZEE_2008",
        'author':'Djalma Filho',
        }



conts = Constantes()
nm = conts.nomes_municipios
src = conts.sistema_de_referencia_de_coordenadas
odta = conts.operacoes_da_tabela_de_atributos
uni_low = conts.unicodes_lowercase
uni_up = conts.unicodes_upercase
dqmds = conts.definition_query_mapa_situacao
nm_Camadas = conts.nome_das_camadas


# converte string em camada
def string_to_map(mxd, string_da_camada):
    """Retorna o map correspondente a string."""

    if isinstance(string_da_camada, str):
        print("convertendo str to <map>")
        for i in arcpy.mapping.ListLayers(mxd):
            if i.name == string_da_camada:
                string_da_camada = i
                return string_da_camada
    else:
        return string_da_camada

# atualiza o mapa de situação automaticamente apenas fornecendo municipio(s)
def att_situacao(mxd=False, municipios='PORTEL', *args):

    """ Atualiza o mapa de situacao, cedo, e município de interesse (1 ou mais):
        Ex.: att_situacao(mxd=False, 'BELÉM', 'ACARÁ', ... , 'BAGRE') (*em minúsculas)

    Args:
        mxd (bool, optional): Projeto que será utilizado. Defaults to False.
        
        municipios (str, optional): strings, separadas por virugla com o nome
        dos municípios desejados. Defaults to 'PORTEL'.
    """


    if not mxd:
        mxd = arcpy.mapping.MapDocument("CURRENT")

    # Gera uma Tupla com os municipios um apos o outro.
    municipio = tuple([municipios]) + args
    EXP = ["{}".format(i) for i in range(1, 4)]
    # EXP: deve constar no primeiro caractere da descrição da camadas na sequencia:
    # sedes(pontos) = 1, limites(bordas) = 2, interesse(amarelo) = 3
    fz = 1.084556648631034  # NUMERO DE OURO
    df = False

    # lista de camadas
    cmds = arcpy.mapping.ListLayers(mxd)
    # Armazena apenas as camadas que derem match na expressão, em ordem.
    cdi = [cmd for exp in EXP for cmd in cmds if cmd.description[:1] == exp]

    # Se a opção nenhum for selecionado, não aparece nenhum
    if municipio[0] == 'nenhum':
        e1 = e2 = e3 = ""
        for i, (c, exp) in enumerate(zip(cdi, [e1, e2, e3])):
            c.definitionQuery = exp
        arcpy.RefreshActiveView()
        return

    # Seleciona o ultimo DataFrame = Mapa de Situção
    if not df:
        df = arcpy.mapping.ListDataFrames(mxd)[-1]

    print("Municipios: ", municipios) # info

    # modificação de caracteres problematicos
    if municipio and isinstance(municipio, tuple):
        lm = []
        for m in municipio:
            m = m.upper()
            for u, U in zip(uni_low, uni_up):
                m = m.replace(u,U)
            lm.append(m)

        # Realiza a criação da expresão do Definition Query
        for i, v in enumerate(lm):
            if i == 0:
                e1 = dqmds[1].format("", v)
                e2 = dqmds[2].format("", v)
                e3 = dqmds[3].format("", v)
                continue
            e1 += dqmds[1].format(" OR ", v)
            e2 += dqmds[2].format(" AND ",v)
            e3 += dqmds[3].format(" OR ", v)

    if municipio and isinstance(municipio, str):
        municipio = municipio.upper()
        for u, U in zip(uni_low, uni_up):
            municipio = municipio.replace(u,U)
            m = municipio

        e1 = dqmds[1].format("", m)
        e2 = dqmds[2].format("", m)
        e3 = dqmds[3].format("", m)
    
    # Depois aplica um zoom na extensão
    for i, (c, exp) in enumerate(zip(cdi, [e1, e2, e3])):
        c.definitionQuery = exp
        if i == 2:
            z = c.getSelectedExtent()

    # Magia do zoom
    df.extent = z
    df.scale *= fz

    print("Fim da Atualização do Mapa de Situação.")

# Aplica um zoom agradável na camada
def zoom_camada(camada, mxd=False, data_frame=False):
    """Aplica um zoom numa escala media e numero inteiro."""

    if not mxd:
        mxd = arcpy.mapping.MapDocument("CURRENT")

    if not data_frame:
        data_frame = arcpy.mapping.ListDataFrames(mxd)[0]

    if isinstance(camada, str):
        camada = string_to_map(mxd, camada)

    cmds = arcpy.mapping.ListLayers(mxd)
    for i in cmds:
        if i.name == camada.name:
            camada = i

    obj_zoom = camada.getSelectedExtent()
    data_frame.extent = obj_zoom

    # Numbers Trick
    fator = len(str(data_frame.scale).split('.')[0])-1
    z = '1'+'0'*fator
    escala = data_frame.scale/int(z)

    # Exception
    if escala > 2:
        escala = (round(escala,0)*3)*int(z)
        z2 = z + '0'
        escala = round(escala/int(z2),0)*int(z2)
        data_frame.scale = escala
        arcpy.RefreshActiveView()
        return 1

    # Final 
    escala = (round(escala,0)*3)*int(z)
    data_frame.scale = escala
    arcpy.RefreshActiveView()
    return 2

# limpa a selação da camada selecionada
def limpar_selecao(camada):
    """Retira a Selecao feita sobre uma determinada camada"""

    arcpy.SelectLayerByAttribute_management(camada,"CLEAR_SELECTION")

# Aplica simbologia
def aplicar_simbologia(projeto_mxd, nome_camada_estilo_a_copiar, camada_a_aplicar):
    """ Pega a camada desejada copia sua simbologia na camada a aplicar."""

    for layer in arcpy.mapping.ListLayers(projeto_mxd):
        if layer.name == nome_camada_estilo_a_copiar:
            simb = layer

    arcpy.ApplySymbologyFromLayer_management(camada_a_aplicar, simb)

# criação do buffer
def criar_buffer(camada_a_ser_bufada, data_frame_to_add, distancia_metros=900):
    print("Executando funcao criar_buffer")
    print("Entrado na funcao, valor recebido pela camada_a_ser_bufada: ",camada_a_ser_bufada)
    pasta = 'C:\\Users\\{0}\\arcgis_temp'.format(self.model.nome_usuario)
    
    camada_saida = os.path.join(pasta, "buffer.shp")
    
    if not os.path.exists(pasta):
        os.mkdir(pasta)
        print("Pasta Criada")
    else:
        print("Pasta ja existe, removendo..")
        #print("Dormindo...")
        #time.sleep(5)
        try:
            shutil.rmtree(pasta)
            os.mkdir(pasta)
        except Exception as e:
            print("Nao foi possivel realizar remocao e criacao")
            print(str(e))
            print("\n\tContinuando Processos....\n")
            
        print("Pasta Criada")

    distancia = str(distancia_metros) + " Meters"
    print("Relizando buffer analysis")
    print("camada_a_ser_bufada")
    print(camada_a_ser_bufada)
    print("camada_saida")
    print(camada_saida)
    arcpy.Buffer_analysis(camada_a_ser_bufada, camada_saida, distancia)
    
    pasta = 'C:\\Users\\{0}\\arcgis_temp'.format(self.model.nome_usuario)
    caminho_busca = os.path.join(pasta, "buffer.shp")
    buffer = arcpy.mapping.Layer(caminho_busca)
    arcpy.mapping.AddLayer(data_frame_to_add, buffer, "TOP")
    print("Buffer Criado com sucesso!")
    return buffer

# copiar shapes
def copiar_shapes(camada_a_ser_copiada, camada_alvo):
    print("Executando funcao copiar_shapes")
    print("copiando os valores")
    camada_alvo = arcpy.da.InsertCursor(camada_alvo, ["SHAPE@"])
    with arcpy.da.SearchCursor(camada_a_ser_copiada, ["SHAPE@"]) as cursor:
        for shape in cursor:
            camada_alvo.insertRow(shape)  
            print(shape)
    print("Atualizando")
    arcpy.RefreshActiveView()

# apagar buffer
def apagar_buffer(arquivos_mxd):
    print("Executando funcao apagar_buffer")
    mxd = arquivos_mxd
    principal = arcpy.mapping.ListDataFrames(mxd)[0]
    layers = arcpy.mapping.ListLayers(mxd)
    print("Removendo: ", layers[0].name)
    arcpy.mapping.RemoveLayer(principal, layers[0])

# TODO IMPLEMENTAR, NÃO ESTÁ FUNCIONANDO
def limpa_tda(camada_area_de_limitacao):
    print("executando funcao limpa_tda")
    arcpy.DeleteRows_management(camada_area_de_limitacao)

# conjunto de funcoes para o buffer
def area_limitacao(camada_a_ser_bufada, data_frame_to_add, arquivo_mxd, distancia_metros=300):
    print("Executando funcao area_limitacao")
    print("Criando Buffer")
    buffer = criar_buffer(camada_a_ser_bufada, data_frame_to_add, distancia_metros)
    try:
        limpa_tda(camada_area_de_limitacao=r"LEGENDA\AREA DE LIMITACAO")
    except Exception as e:
        print(e.__class__.__name__)
        print(e)
        print("LimpaTDA falhou, continuando...")

    arg1 = 'C:\\Users\\{}\\arcgis_temp\\buffer.shp'.format(self.model.nome_usuario)
    arg2 = string_to_map(arquivo_mxd, "AREA DE LIMITACAO")
    
    print("Args de area de limitacao!")
    print(arg1)
    print(arg2)
    
    print("COPIANDO AS TABELAS DE TRIBUTOS!")
    copiar_shapes(arg1, arg2)
    print("APAGANDO BUFFER DO PROJETO!!!!")
    apagar_buffer(arquivos_mxd=arquivo_mxd)
    return arquivo_mxd



# Dados Gerais
class Model:
    rotulos = ["Ano","Número","Situaççao","Interessado",
        "Denominação","Município","Carta","Zoneamento",
        ]

    # Importante para configurar corretamente o Icone.
    myappid = 'Ocorrencias Maker {}-{}.{}'.format(__version__, __stage__, __subversion__)
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


    # User Related
    nome_diretorio = os.path.dirname(__file__).replace('/','\\')
    nome_usuario =getpass.getuser()
    caminho_projeto_mxd_legenda = ''

    # Tela
    largura = 1270
    altura = 823
    screen_largura = ctypes.windll.user32.GetSystemMetrics(0)
    screen_altura = ctypes.windll.user32.GetSystemMetrics(1)
    posicao_x = screen_largura//2 - largura//2
    posicao_y = screen_altura//2 - altura//2 
    
    # Informações
    comprimento_entry_informacoes = 70

    # 
    sequencia_de_linhas_entry_informacoes = range(1,10)





class TkView:

    def setup(self):

        """Setup inicial do Programa."""

        self.root = tkinter.Tk() # Raiz
        self.root.title(self.model.myappid) # Título
        self.root.geometry('{}x{}+{}+{}'.format(
            self.model.largura,
            self.model.altura,
            self.model.posicao_x,
            self.model.posicao_y,
            ))  
        
        # Carrega o Icone, que é gerado pelo instalador
        self.root.iconbitmap('{}\\{}'.format(self.model.nome_diretorio, 'automap.ico'))
        
        # Botões de ação da Janela: Minimizar, Maximizar, Fechar.
        # self.root.overrideredirect(True) # Remove
        self.root.overrideredirect(False)  # Não Remove

        # Funções de Redimensionamento
        # self.root.resizable(width=False, height=False) # Não permite
        self.root.resizable(width=True, height=True)     # Permite
        self.style = ttk.Style()
        self.style.theme_use('vista')

        # Adicionando os Widget na tela. OBS: Ordem é importante
        self.func_adicionar_frame_informacoes()
        self.func_adicionar_frame_pre_vizualizacao()
        self.func_adicionar_frame_caminhos()
        self.func_adicionar_frame_legenda()
        self.func_adicionar_frame_limites()
        self.func_adicionar_menubar()
        self.func_adicionar_hotkeys()

        # # Mudar Font
        # self.root.option_add("*Font", ('Impact', 9))
        # # Responsavel pela criação da tela com pegada em qualquer lugar
        # grip = Grip(self.root)
 
        # Inserir dados da seção anterior

        self.func_inserir_dados_salvos()
        self.disable_radio_buttons() # Desativa os Butões

        # Mostrar msg inicial

        espacos_msg_inicial = ' '*20
        titulo = "Mensagem Inicial"
        msg = 'AutoMap\n\nVersão: {}-{}.{}{}'
        messagebox.showinfo(title=titulo, message=msg.format(
            __version__, __stage__, __subversion__, espacos_msg_inicial)
            )


    def start_main_loop(self):

        """Inicia a cascata de eventos para inicializar o programa."""

        self.root.mainloop()


    def quit_main_loop(self, *args):

        """
        Salva as informações inseridas em:
        Documentos > AutoMap > Dados_de_Entrada.txt
        Então, encerra o programa.
        """

        # Salva as informações antes de sair
        self.func_salvar_informacoes(
            self.ano_, self.numero_,
            self.situacao_,
            self.interessado_, self.denominacao_,
            self.municipio_,
            self.carta_, self.zoneamento_,
            None
            )
       # Encerra o Programa     
        self.root.quit()
 

    def disable_radio_buttons(self, *args):
        """
        Logo que o programa se abre, ou apartir de um evento
        Desabilita os RadioButtons para não serem clicáveis.
        """

        self.rb_gms['state'] = 'disabled'
        self.rb_gd['state'] = 'disabled'
        self.rb_utm['state'] = 'disabled'
        self.epsg_Entry['state'] = 'disabled'


    def define(self, control, model):
        """
        Define a Estrura padrão do MVC.

        Args:
            control (Control): Classe de Controle, contendo as funções
            model (Model): Onde temos as possiveis informações
        """

        self.control = control
        self.model = model


    def func_root_quit(self, *args):

        """Encera o programa."""

        self.root.quit()


    def func_vizualizar_informacoes(self, ano, numero, situacao, interessado, denominacao, municipio, carta, zoneamento, instance):
        
        """Mostra uma caixa na tela para vizualizar as informações e ainda salva num txt."""

        self.model.rotulos = ["Ano", "Número", "Situação", "Interessado", "Denominação", "Município", "Carta", "Zoneamento"]
        texto = []
        pasta_automap = "C:\\Users\\{}\\Documents\\AutoMap".format(self.model.nome_usuario)

        if not os.path.exists(pasta_automap):
            os.mkdir(pasta_automap)

        sd = pasta_automap + "\\DADOS_DE_ENTRADA\\"

        arquivo = sd + "{}_{}_{}.txt".format(
            ano.get().encode('utf-8'),
            numero.get().encode('utf-8'),
            interessado.get().encode('utf-8')
            )

        with open(arquivo, 'w') as f:
            
            for a,b in zip([ano, numero, situacao, interessado, denominacao, municipio, carta, zoneamento], rotulos):
                a = a.get().encode('utf-8')
                # b = b.encode('utf-8') # Se ta em UTF la em cima nao precisar usar o decode!
                print("{} -> {}".format(b,a))
                f.write("{} -> {}\n".format(b,a))
                texto.append("{} -> {}\n".format(b,a))

        # TODO TODO TODO TODO
        # DO SOMETRING
        
        # with open(pasta_automap + "\\INFORMACOES_PARA_TABELA.txt", 'w') as f:
            
        #     for a,b in zip([ano, numero, situacao, interessado, denominacao, municipio, carta, zoneamento], rotulos):
        #         a = a.get().encode('utf-8')
        #         # b = b.encode('utf-8') # Se ta em UTF la em cima nao precisar usar o decode!
        #         f.write("{};".format(a))
                
        print("Informações")
        print(texto)
        novo_texto = ''.join(texto)
        messagebox.showinfo("Informações", novo_texto)


    def func_salvar_informacoes(self, ano, numero, situacao, interessado, denominacao, municipio, carta, zoneamento, instance):
        rotulos = ["Ano", "Número", "Situação", "Interessado", "Denominação", "Município", "Carta", "Zoneamento", "Projeto", "Exportar em", "Shape ou Txt em"]
        var_pro = self.caminho_projeto_mxd_Entry
        var_out = self.caminho_para_salvar_Entry
        var_shp = self.caminho_arquivo_shp_ou_txt_Entry
        texto = []
        pasta_automap = "C:\\Users\\{}\\Documents\\AutoMap".format(self.model.nome_usuario)

        if not os.path.exists(pasta_automap):
            os.mkdir(pasta_automap)

        if not os.path.exists(pasta_automap + "\\DADOS_DE_ENTRADA"):
            os.mkdir(pasta_automap + "\\DADOS_DE_ENTRADA")

        with open(pasta_automap + "\\DADOS_DE_ENTRADA\\" + "{}_{}_{}.txt".format(ano.get().encode('utf-8'),numero.get().encode('utf-8'),interessado.get().encode('utf-8')), 'w') as f:
            
            for a,b in zip([ano, numero, situacao, interessado, denominacao, municipio, carta, zoneamento, var_pro, var_out, var_shp], rotulos):
                a = a.get().encode('utf-8')
                # b = b.encode('utf-8') # Se ta em UTF la em cima nao precisar usar o decode!
                print("{} -> {}".format(b,a))
                f.write("{} -> {}\n".format(b,a))
                texto.append("{} -> {}\n".format(b,a))
        if not os.path.exists(pasta_automap + "\\INFORMACOES_PARA_TABELA"):
            os.mkdir(pasta_automap + "\\INFORMACOES_PARA_TABELA")

        with open(pasta_automap + "\\INFORMACOES_PARA_TABELA\\{}_{}_{}.txt".format(ano.get().encode('utf-8'),numero.get().encode('utf-8'),interessado.get().encode('utf-8')), 'w') as f:
            
            for a,b in zip([ano, numero, situacao, interessado, denominacao, municipio, carta, zoneamento, var_pro, var_out, var_shp], rotulos):
                a = a.get().encode('utf-8')
                # b = b.encode('utf-8') # Se ta em UTF la em cima nao precisar usar o decode!
                f.write("{};".format(a))
                
        print("Informações")
        print(texto)


    def func_variavel_dropdown(self, *args):
        condicao_opcao_do_dropdown = self.estado_do_botao_do_dropdown
        print("Args: {} A caixa de selecao mudou para: [{}]".format(args, condicao_opcao_do_dropdown))
        
        if self.rb_gms:
            self.rb_gms['state'] = 'disabled'
        if self.rb_gd:
            self.rb_gd['state'] = 'disabled'
        if self.rb_utm:
            self.rb_utm['state'] = 'disabled'
        if self.epsg_Entry:
            self.epsg_Entry['state'] = 'disabled'

        if condicao_opcao_do_dropdown.endswith("txt") or condicao_opcao_do_dropdown.endswith("csv"):
            self.rb_gms['state'] = 'normal'
            self.rb_gd['state'] = 'normal'
            self.rb_utm['state'] = 'normal'
            self.epsg_Entry['state'] = 'normal'
        else:
            self.rb_gms['state'] = 'disabled'
            self.rb_gd['state'] = 'disabled'
            self.rb_utm['state'] = 'disabled'
            self.epsg_Entry['state'] = 'disabled'


    def func_dropdown_mudou(self, estado_do_botao_do_dropdown):
        self.estado_do_botao_do_dropdown = estado_do_botao_do_dropdown
        print("func_dropdown_mudou: change function to: [{}]".format(self.estado_do_botao_do_dropdown))
        self.func_variavel_dropdown()
        

    def func_como_usar(self, *args):
        messagebox.showinfo(title="Como Usar", message="Informar as dados fundamentais do Processo em questão dentro das caixas de texto.\nUsar os botões ou atalhos do teclado para selecionar: \n\n1. O layout padrão que será usado\n2. A pasta na qual serão exportados os produtos\n3. O shapefile ou arquivo de texto com coordenadas que será usado para a plotagem do polígono ou ponto de interesse\n\nExportar o mapa para a pasta informada irá gerar:\n\n1. Projeto .mxd para analises adicionais e/ou edições.\n2. O PDF contendo a vizualização do mapa")


    def func_lista_de_epsgs(self, *args):
        caixa = """    4326...............GCS WGS 1984
    4170...............GCS SIRGAS
    4674...............GCS SIRGAS 2000
    31981..............SIRGAS 2000 UTM Zone 21S
    31982..............SIRGAS 2000 UTM Zone 22S
    31983..............SIRGAS 2000 UTM Zone 23S
    5527................GCS SAD 1969 96
    4618................GCS South American 1969
    29191..............SAD 1969 UTM Zone 21S
    29192..............SAD 1969 UTM Zone 22S
    29193..............SAD 1969 UTM Zone 23S
    5531................SAD 1969 96 UTM Zone 21S
    5858................SAD 1969 96 UTM Zone 22S
    5533................SAD 1969 96 UTM Zone 23S
    102015............South America Lambert Conformal Conic"""
        messagebox.showinfo(title="Lista com os EPSGs mais utilizados", message=caixa)


    def func_sobre(self, *args):
        messagebox.showinfo(title="Sobre", message="Programa criado por: Djalma Filho (Estagiário).\n\nVisando acelerar a criação de mapas simples de maneira automatizada.\n\nVersão: {}-{}.{}".format(__version__, __stage__, __subversion__))


    def func_seleciona_camada_legenda(self, *args):
        caminho_projeto_mxd = self.view.caminho_projeto_mxd_Entry.get().encode('utf-8')
        mxd = arcpy.mapping.MapDocument(caminho_projeto_mxd)
        df = arcpy.mapping.ListDataFrames(mxd, "*")[0]

     
    def func_adicionar_hotkeys(self):
        """ Adicionar os atalhos no teclado que serão usados. """

        # hot keys NO CAPS
        self.root.bind_all(sequence='<Control-d>', func=self.control.func_selecionar_arquivo_projeto_mxd)
        self.root.bind_all(sequence='<Control-o>', func=self.control.func_selecionar_arquivo)
        self.root.bind_all(sequence='<Control-s>', func=self.control.func_selecionar_diretorio_exportar_produtos)
        self.root.bind_all(sequence='<Control-m>', func=self.control.func_abrir_arc_map)
        self.root.bind_all(sequence='<Control-q>', func=self.quit_main_loop)
        #self.root.bind_all(sequence='<Control-v>', func=self.viz_data)
        self.root.bind_all(sequence='<Control-h>', func=self.func_como_usar)
        self.root.bind_all(sequence='<Control-l>', func=self.func_lista_de_epsgs)
        self.root.bind_all(sequence='<Control-i>', func=self.func_sobre)
        self.root.bind_all(sequence='<Control-e>', func=self.partial_exportar_mapa)

        # WITH CAPS
        self.root.bind_all(sequence='<Control-D>', func=self.control.func_selecionar_arquivo_projeto_mxd)
        self.root.bind_all(sequence='<Control-O>', func=self.control.func_selecionar_arquivo)
        self.root.bind_all(sequence='<Control-S>', func=self.control.func_selecionar_diretorio_exportar_produtos)
        self.root.bind_all(sequence='<Control-M>', func=self.control.func_abrir_arc_map)
        self.root.bind_all(sequence='<Control-Q>', func=self.quit_main_loop)
        #self.root.bind_all(sequence='<Control-V>', func=self.viz_data)
        self.root.bind_all(sequence='<Control-H>', func=self.func_como_usar)
        self.root.bind_all(sequence='<Control-L>', func=self.func_lista_de_epsgs)
        self.root.bind_all(sequence='<Control-I>', func=self.func_sobre)
        self.root.bind_all(sequence='<Control-E>', func=self.partial_exportar_mapa)


    def func_adicionar_menubar(self):
        """ Adiciona os itens e funções da Barra de Menus. """

        # MENUBAR
        self.menubar = tkinter.Menu(self.root)

        # ABA: ARQUIVO
        self.filemenu = tkinter.Menu(self.menubar, tearoff=False)
        self.filemenu.add_command(label="Selecionar Projeto", accelerator='Ctrl+D', command=self.control.func_selecionar_arquivo_projeto_mxd)
        self.filemenu.add_command(label="Selecionar Arquivo", accelerator='Ctrl+O', command=self.control.func_selecionar_arquivo)
        self.filemenu.add_command(label="Selecionar Diretório", accelerator='Ctrl+S',  command=self.control.func_selecionar_diretorio_exportar_produtos)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Sair", accelerator='Ctrl+Q', command=self.quit_main_loop)
        self.menubar.add_cascade(label="Arquivo", menu=self.filemenu)


        # ABA: OPÇÕES
        self.optionsmenu = tkinter.Menu(self.menubar, tearoff=False)
        self.optionsmenu.add_command(label="Abrir ArcMap", accelerator='Ctrl+M', command=self.control.func_abrir_arc_map)
        self.optionsmenu.add_command(label="Vizualizar Informações", command=self.viz_data2)
        self.optionsmenu.add_command(label="Exportar Mapa", accelerator='Ctrl+E', command=self.partial_exportar_mapa)
        self.menubar.add_cascade(label="Opções", menu=self.optionsmenu)

        # ABA: AJUDA
        self.helpmenu = tkinter.Menu(self.menubar, tearoff=False)
        self.helpmenu.add_command(label="Como usar", accelerator='Ctrl+H', command=self.func_como_usar)
        self.helpmenu.add_command(label="Lista: EPSG", accelerator='Ctrl+L', command=self.func_lista_de_epsgs)
        self.helpmenu.add_separator()
        self.helpmenu.add_command(label="Sobre...", accelerator='Ctrl+I',command=self.func_sobre)
        self.menubar.add_cascade(label="Ajuda", menu=self.helpmenu)
        
        # SETUP COMPLETE
        self.root.config(menu=self.menubar)


    def func_adicionar_frame_caminhos(self):
        """ Adiciona o layout de caminhos. """

        #self.gms = tkinter.IntVar()
        #self.gd = tkinter.IntVar()
        #self.utm = tkinter.IntVar()
        self.opt = tkinter.IntVar()

        self.theme_frame_caminhos = ttk.LabelFrame(self.theme_frame_informacoes, text='')

        self.theme_frame_log = ttk.LabelFrame(self.theme_frame_caminhos, text='LOG')
        self.log_text_Label = ttk.Label(self.theme_frame_log, text=self.log_text, justify='left',width=self.model.comprimento_entry_informacoes-15)
        self.log_text_Label['text'] = '\tAguardando entradas do usuário...'


        # GRUPO INFORAMÕES : LINHAS 11 ATÉ 17-18
        self.caminho_projeto_mxd_Label = ttk.Label(self.theme_frame_caminhos, text=" Projeto .mxd ")
        self.caminho_para_salvar_Label = ttk.Label(self.theme_frame_caminhos, text=" Exportar Mapa")
        self.caminho_projeto_mxd_Entry = ttk.Entry(self.theme_frame_caminhos, width=self.model.comprimento_entry_informacoes, textvariable=self.caminho_mxd_,)
        self.caminho_para_salvar_Entry = ttk.Entry(self.theme_frame_caminhos, width=self.model.comprimento_entry_informacoes, textvariable=self.caminho_para_salvar_,)
        
        self.sb1 = partial(self.control.func_selecionar_arquivo_projeto_mxd, self.caminho_projeto_mxd_Entry)
        self.caminho_projeto_mxd_Button = ttk.Button(self.theme_frame_caminhos, text='Selecionar', command=self.sb1)

        self.sb2 = partial(self.control.func_selecionar_diretorio_exportar_produtos, self.caminho_para_salvar_Entry)
        self.open_button_2 = ttk.Button(self.theme_frame_caminhos, text='Selecionar', command=self.sb2)

        # Label com ajuda
        self.texto_de_ajuda = "Selecionar tipo de arquivo\n\tArquivos Shapefile (*.shp)\n\tCoordenadas em arquivo de texto (*.txt).\n\nPara Coordenadas Especificar:\n\tEPSG\n\tE como as Coordenadas estão formatadas."
        self.ajuda_LabelFrame = ttk.LabelFrame(self.theme_frame_caminhos, text='')
        self.ajuda_Label = ttk.Label(self.ajuda_LabelFrame, text=self.texto_de_ajuda)


        #  DROP DOWN com as Opcoes .TXT ou .SHP
        self.opcoes_do_dropdown = ['*.txt', '*.shp', '*.gdb', '*.mxd', '*.csv']  
        self.variavel_das_opcoes = tkinter.StringVar(value='*.txt')
        self.variavel_das_opcoes.set('*.csv')

        #self.variable.trace('w', self.func_variavel_dropdown)

        
        self.dropdown = ttk.OptionMenu(
            self.theme_frame_caminhos,
            self.variavel_das_opcoes,
            self.opcoes_do_dropdown[1],
            *self.opcoes_do_dropdown,
            command=self.func_dropdown_mudou
            )
        #
        self.caminho_arquivo_shp_ou_txt_Entry = ttk.Entry(self.theme_frame_caminhos, width=self.model.comprimento_entry_informacoes, textvariable=self.caminho_arquivo_shp_ou_txt,)

        #### BOTÃO DE EXPORTAR MAPA #####

        # self.partial_exportar_mapa = partial(   self.control.func_exportar_mapa,
        #                                         self.ano_,self.numero_,self.situacao_,
        #                                         self.interessado_,self.denominacao_,
        #                                         self.municipio_,self.carta_,
        #                                         self.zoneamento_)

        # self.partial_exportar_mapa2 = partial(  self.control.func_exportar_mapa,
        #                                         self.ano_,self.numero_,self.situacao_,
        #                                         self.interessado_,self.denominacao_,
        #                                         self.municipio_,self.carta_,
        #                                         self.zoneamento_,None)

        # self.exportar_mapa_button = ttk.Button(self.theme_frame_caminhos, text=" Exportar Mapa ", command=self.partial_exportar_mapa2)
        #### BUTTAO DE EXPORTAR MAPA #####

        # GRIDS
        #self.theme_frame_caminhos.grid(row=1,column=1,padx=10, pady=10, ipadx=5, ipady=0, sticky='ne')
        



        self.epsg_Label = ttk.Label(self.theme_frame_caminhos, text='EPSG')
        self.epsg_Entry = ttk.Entry(self.theme_frame_caminhos, width=6, textvariable=self.epsg_,)



        self.sb3 = partial(self.control.func_selecionar_arquivo, self.caminho_arquivo_shp_ou_txt_Entry)
        self.open_button_txt_shp = ttk.Button(self.theme_frame_caminhos, text='Selecionar', command=self.sb3)




        self.f1 = tkinter.Frame(self.theme_frame_caminhos)


        self.rb_gms = ttk.Radiobutton(self.f1, text="Grau Minuto Segundo", value=1, var=self.opt)
        self.rb_gd = ttk.Radiobutton(self.f1, text="Grau Decimal", value=2, var=self.opt)
        self.rb_utm = ttk.Radiobutton(self.f1, text="UTM", value=3, var=self.opt)



        # BOTAO DE TESTES RAPIDOS
        textos_radios = ["Nenhum valor selecionado","Grau Minuto Segundo","Grau Decimal","UTM"]
        
        self.rb_gms.grid(row=0, column=2, sticky = 'e')
        self.rb_gd.grid(row=0, column=3, sticky = 'e')
        self.rb_utm.grid(row=0, column=4, sticky = 'e')
        self.theme_frame_caminhos.grid(row=0, columnspan=2)
        self.ajuda_Label.grid(                       row=1, column=1, padx=5, pady=5,  sticky='w')
        self.caminho_projeto_mxd_Label.grid(         row=10+1, column=0)  
        self.caminho_projeto_mxd_Entry.grid(         row=10+1, column=1, padx= 5, pady=5)
        self.caminho_projeto_mxd_Button.grid(        row=10+1, column=2)
        self.caminho_para_salvar_Label.grid(         row=10+2, column=0) 
        self.caminho_para_salvar_Entry.grid(         row=10+2, column=1, padx= 5, pady=5)
        self.open_button_2.grid(                     row=10+2, column=2)
        self.ajuda_LabelFrame.grid(                  row=10+3, column=1, padx=10, pady=10, ipadx=5, ipady=0, sticky='w')
        self.dropdown.grid(                          row=10+4, column=0, pady=0)
        self.caminho_arquivo_shp_ou_txt_Entry.grid(  row=10+4, column=1, pady=0)
        self.open_button_txt_shp.grid(               row=10+4, column=2)
        self.f1.grid(                                row=10+5, column=1,sticky = 'e')
        self.epsg_Label.grid(                        row=10+5, column=0)  
        self.epsg_Entry.grid(                        row=10+5, column=1, padx=5, pady=5,  sticky='w')  
        self.exportar_mapa_button.grid(              row=10+6, column=1, pady=20)
        self.theme_frame_log.grid(                   row=10+7, column=1)
        self.log_text_Label.grid(                    pady=17  )

        
        
        def mostrar_teste(*args):
            opcao_do_radio = self.opt.get()
            print(opcao_do_radio)
            messagebox.showinfo("Selecionado",textos_radios[opcao_do_radio])

        self.botao_teste = ttk.Button(self.f1, text=' ', width=1, command=mostrar_teste)
        self.botao_teste.grid(row=0, column=5, sticky = 'e')
        # PRA PEGAR O VALOR DOS RAPDOS


        self.caminho_projeto_mxd_Label = ttk.Label(self.theme_frame_caminhos, text=" Projeto .mxd ")
        self.caminho_projeto_mxd_Entry = ttk.Entry(self.theme_frame_caminhos, width=self.model.comprimento_entry_informacoes, textvariable=self.caminho_mxd_,)
        self.sb1 = partial(self.control.func_selecionar_arquivo_projeto_mxd, self.caminho_projeto_mxd_Entry)
        self.caminho_projeto_mxd_Button = ttk.Button(self.theme_frame_caminhos, text='Selecionar', command=self.sb1)
        self.caminho_para_salvar_Label = ttk.Label(self.theme_frame_caminhos, text=" Exportar Mapa")
        self.caminho_para_salvar_Entry = ttk.Entry(self.theme_frame_caminhos, width=self.model.comprimento_entry_informacoes, textvariable=self.caminho_para_salvar_,)
        self.sb2 = partial(self.control.func_selecionar_diretorio_exportar_produtos, self.caminho_para_salvar_Entry)
        self.open_button_2 = ttk.Button(self.theme_frame_caminhos, text='Selecionar', command=self.sb2)

        # Label com ajuda
        self.texto_de_ajuda = "Selecionar tipo de arquivo\n\tArquivos Shapefile (*.shp)\n\tCoordenadas em arquivo de texto (*.txt).\n\nPara Coordenadas Especificar:\n\tEPSG\n\tGrau Minuto Segundou\n\tGrau Decimal\n\tUTM."
        self.ajuda_LabelFrame = ttk.LabelFrame(self.theme_frame_caminhos, text='')
        self.ajuda_Label = ttk.Label(self.ajuda_LabelFrame, text=self.texto_de_ajuda)

        #  DROP DOWN com as Opcoes .TXT ou .SHP
        # self.list_dropdown_options = [' *.txt', ' *.shp']
        # self.variable = tkinter.StringVar(value=self.list_dropdown_options[1])
        # self.variable.trace('w',self.func_variavel_dropdown)
        # self.variable.set(self.list_dropdown_options[1])
        # self.dropdown = ttk.OptionMenu(self.theme_frame_caminhos, self.variable, self.list_dropdown_options[1],*self.list_dropdown_options, command=self.func_dropdown_mudou)
        # self.caminho_arquivo_shp_ou_txt_Entry = ttk.Entry(self.theme_frame_caminhos, width=self.model.comprimento_entry_informacoes, textvariable=self.caminho_arquivo_shp_ou_txt,)

        #### BUTTAO DE EXPORTAR MAPA #####
        self.exportar_mapa_button = ttk.Button(self.theme_frame_caminhos, text=" Exportar Mapa ", command=self.partial_exportar_mapa2)
       
        
    def func_adicionar_frame_pre_vizualizacao(self):
        """ Adiciona o layout de pré vizualização. """
        
        self.nome_da_imagem_gif = "automap.gif"
        self.texto_pre_vizualizacao = "Atualizar pré-vizualização"
        
        self.theme_frame_pre_vizualizacao = ttk.LabelFrame(self.root, text='Pré Vizualização')
     
        # A IMAGEM QUE SERA PRÉVIA DO MAPA
        # CARREGA A IMAGEM DENTRO DA PASTA DO PROJETO
        self.imagem_de_previzualizacao = tkinter.PhotoImage(file="{}\\{}".format(
                os.path.dirname(__file__).replace('/','\\').replace('c:\\','C:\\'),
                self.nome_da_imagem_gif))

        # CRIA UM OBJETO CANVAS
        self.objeto_canvas = tkinter.Canvas(self.theme_frame_pre_vizualizacao, width=610, height=420)
        self.objeto_canvas.create_image(0, 0, anchor='nw', image=self.imagem_de_previzualizacao)
        
        # BOTÃO FINAL
        self.pre_vizualizacao_botao_atualizar = ttk.Button(self.theme_frame_pre_vizualizacao, command=self.control.func_botao_atualizar_preview, text=self.texto_pre_vizualizacao, width=self.model.comprimento_entry_informacoes-5)

        # GRIDS
        self.theme_frame_pre_vizualizacao.grid(row=0,column=1, padx=5, pady=5, ipadx=0, ipady=0, sticky='nw')
        self.objeto_canvas.grid(row=0)



        self.partial_exportar_mapa = partial(   self.control.func_exportar_mapa,
                                                self.ano_,self.numero_,self.situacao_,
                                                self.interessado_,self.denominacao_,
                                                self.municipio_,self.carta_,
                                                self.zoneamento_)

        self.partial_exportar_mapa2 = partial(  self.control.func_exportar_mapa,
                                                self.ano_,self.numero_,self.situacao_,
                                                self.interessado_,self.denominacao_,
                                                self.municipio_,self.carta_,
                                                self.zoneamento_,None)

        self.exportar_mapa_button = ttk.Button(self.theme_frame_pre_vizualizacao, text=" Exportar Mapa ", command=self.partial_exportar_mapa2, width=self.model.comprimento_entry_informacoes-5)
        
        self.pre_vizualizacao_botao_atualizar.grid(row=2)
        self.exportar_mapa_button.grid(row=3)


    def func_adicionar_frame_informacoes(self):
        """ Adiciona o layout de informações. """

        self.theme_frame_informacoes = ttk.LabelFrame(self.root, text='Informações')
        self.theme_frame_informacoes.grid(row=0,column=0, padx=10, pady=10, ipadx=5, ipady=0, sticky='ne')

        self.titulo_ = tkinter.StringVar()
        self.ano_ = tkinter.StringVar()
        self.numero_ = tkinter.StringVar()
        self.situacao_ = tkinter.StringVar()
        self.interessado_ = tkinter.StringVar()
        self.denominacao_ = tkinter.StringVar()
        self.municipio_ = tkinter.StringVar()
        self.carta_ = tkinter.StringVar()
        self.zoneamento_ = tkinter.StringVar()
        self.caminho_mxd_ = tkinter.StringVar()
        self.caminho_para_salvar_ = tkinter.StringVar()
        self.caminho_arquivo_shp_ou_txt = tkinter.StringVar()
        self.log_text = tkinter.StringVar()
        self.pre_vizualizacao_text = tkinter.StringVar()
        self.epsg_ = tkinter.StringVar()

        # ANO
        self.ano_Label = ttk.Label(self.theme_frame_informacoes, text=self.model.rotulos[0], justify='left')
        self.ano_Entry = ttk.Entry(self.theme_frame_informacoes, width=self.model.comprimento_entry_informacoes, textvariable=self.ano_,  )
        # NUMERO
        self.numero_Label = ttk.Label(self.theme_frame_informacoes, text=self.model.rotulos[1], justify='left') 
        self.numero_Entry = ttk.Entry(self.theme_frame_informacoes, width=self.model.comprimento_entry_informacoes, textvariable=self.numero_,  )
        # SITUACAO
        self.situacao_Label = ttk.Label(self.theme_frame_informacoes, text=self.model.rotulos[2], justify='left')
        self.situacao_Entry = ttk.Entry(self.theme_frame_informacoes, width=self.model.comprimento_entry_informacoes, textvariable=self.situacao_,  )
        # INTERESSADO
        self.interessado_Label = ttk.Label(self.theme_frame_informacoes, text=self.model.rotulos[3], justify='left') 
        self.interessado_Entry = ttk.Entry(self.theme_frame_informacoes, width=self.model.comprimento_entry_informacoes, textvariable=self.interessado_,  )
        # DENOMINACAO
        self.denominacao_Label = ttk.Label(self.theme_frame_informacoes, text=self.model.rotulos[4], justify='left')
        self.denominacao_Entry = ttk.Entry(self.theme_frame_informacoes, width=self.model.comprimento_entry_informacoes, textvariable=self.denominacao_,  )
        # Muni_upCIPIO
        self.municipio_Label = ttk.Label(self.theme_frame_informacoes, text=self.model.rotulos[5], justify='left')
        self.municipio_Entry = ttk.Entry(self.theme_frame_informacoes, width=self.model.comprimento_entry_informacoes, textvariable=self.municipio_,  )
        # CARTA
        self.carta_Label = ttk.Label(self.theme_frame_informacoes, text=self.model.rotulos[6], justify='left')
        self.carta_Entry = ttk.Entry(self.theme_frame_informacoes, width=self.model.comprimento_entry_informacoes, textvariable=self.carta_,  )
        # ZONEAMENTO
        self.zoneamento_Label = ttk.Label(self.theme_frame_informacoes, text=self.model.rotulos[7], justify='left')
        self.zoneamento_Entry = ttk.Entry(self.theme_frame_informacoes, width=self.model.comprimento_entry_informacoes, textvariable=self.zoneamento_,  )
        
        # BUTÃO VIZUALIZAR INFORMAÇÕES
        self.viz_data = partial(self.func_vizualizar_informacoes,
                                self.ano_,self.numero_,self.situacao_,
                                self.interessado_,self.denominacao_,
                                self.municipio_,self.carta_,
                                self.zoneamento_)

        self.viz_data2 = partial(self.func_vizualizar_informacoes,
                                self.ano_,self.numero_,self.situacao_,
                                self.interessado_,self.denominacao_,
                                self.municipio_,self.carta_,
                                self.zoneamento_, None)

        self.ano_Label.grid(             row=self.model.sequencia_de_linhas_entry_informacoes[0], column=0)  
        self.ano_Entry.grid(             row=self.model.sequencia_de_linhas_entry_informacoes[0], column=1, padx=5, pady=5,  sticky='w') 
     
        self.numero_Label.grid(          row=self.model.sequencia_de_linhas_entry_informacoes[1], column=0)  
        self.numero_Entry.grid(          row=self.model.sequencia_de_linhas_entry_informacoes[1], column=1, padx=5, pady=5,  sticky='w') 
     
        self.situacao_Label.grid(        row=self.model.sequencia_de_linhas_entry_informacoes[2], column=0)  
        self.situacao_Entry.grid(        row=self.model.sequencia_de_linhas_entry_informacoes[2], column=1, padx=5, pady=5,  sticky='w')  
     
        self.interessado_Label.grid(     row=self.model.sequencia_de_linhas_entry_informacoes[3], column=0)  
        self.interessado_Entry.grid(     row=self.model.sequencia_de_linhas_entry_informacoes[3], column=1, padx=5, pady=5,  sticky='w')  
     
        self.denominacao_Label.grid(     row=self.model.sequencia_de_linhas_entry_informacoes[4], column=0)  
        self.denominacao_Entry.grid(     row=self.model.sequencia_de_linhas_entry_informacoes[4], column=1, padx=5, pady=5,  sticky='w')  
     
        self.municipio_Label.grid(       row=self.model.sequencia_de_linhas_entry_informacoes[5], column=0)  
        self.municipio_Entry.grid(       row=self.model.sequencia_de_linhas_entry_informacoes[5], column=1, padx=5, pady=5,  sticky='w')  
     
        self.carta_Label.grid(           row=self.model.sequencia_de_linhas_entry_informacoes[6], column=0)  
        self.carta_Entry.grid(           row=self.model.sequencia_de_linhas_entry_informacoes[6], column=1, padx=5, pady=5,  sticky='w')  
     
        self.zoneamento_Label.grid(      row=self.model.sequencia_de_linhas_entry_informacoes[7], column=0)  
        self.zoneamento_Entry.grid(      row=self.model.sequencia_de_linhas_entry_informacoes[7], column=1, padx=5, pady=5,  sticky='w')

        self.viz_all_info_button = ttk.Button(self.theme_frame_informacoes, text="Vizualizar e Salvar Dados", command=self.viz_data2)
        self.viz_all_info_button.grid(row=self.model.sequencia_de_linhas_entry_informacoes[8], column=0, columnspan=2,pady=5)


    def func_adicionar_frame_limites(self):
        # self.theme_frame_limites = ttk.LabelFrame(self.theme_frame_legenda, text='LIMITES')
        # self.theme_frame_limites.grid()
        # self.var_btn_limites = tkinter.StringVar()
        # self.var_btn_limites.set("LIMITES (desativado)")
        # self.btn_limites = ttk.Checkbutton(self.theme_frame_limites,onvalue ="LIMITES ( ativado  )",offvalue="LIMITES (desativado)",textvariable=self.var_btn_limites,variable=self.var_btn_limites)
        # btn_limites_args = partial(self.control.func_legenda_visibilidade_camada_imediata,'LIMITES',self.btn_limites)
        # self.btn_limites.configure(command=btn_limites_args)
        # self.btn_ai.grid()
        pass


    def func_adicionar_frame_legenda(self):
        """ Adiciona o layout de legenda. """

        self.theme_frame_legenda = ttk.LabelFrame(self.theme_frame_pre_vizualizacao, text='Legenda')
        #self.theme_frame_legenda.grid(row=0,column=1, padx=10, pady=10, ipadx=5, ipady=0, sticky='nw')
        self.theme_frame_legenda.grid(row=1)

        self.var_btn_ai = tkinter.StringVar()
        self.var_btn_ge = tkinter.StringVar()
        self.var_btn_gf = tkinter.StringVar()
        self.var_btn_ae = tkinter.StringVar()
        self.var_btn_af = tkinter.StringVar()
        self.var_btn_li = tkinter.StringVar()
        self.var_btn_te = tkinter.StringVar()
        self.var_btn_qu = tkinter.StringVar()
        self.var_btn_pe = tkinter.StringVar()
        self.var_btn_limites = tkinter.StringVar()
        self.var_btn_info_cart = tkinter.StringVar()


        self.var_btn_ai.set('ÁREA DE INTERESSE')
        self.var_btn_ge.set('GLEBAS ESTADUAIS')
        self.var_btn_gf.set('GLEBAS FEDERAIS')
        self.var_btn_ae.set('ASSENTAMENTOS ESTADUAIS')
        self.var_btn_af.set('ASSENTAMENTOS FEDERAIS')
        self.var_btn_li.set('LOTES INCIDENTES')
        self.var_btn_te.set('TÍTULOS DEFINITVOS EXPEDIDOS')
        self.var_btn_qu.set('QUILOMBO')
        self.var_btn_pe.set('PEAEX')
        self.var_btn_limites.set("LIMITES (desativado)")
        self.var_btn_info_cart.set("INFOR. CARTO. (OFF)")
        
        self.btn_ai = ttk.Checkbutton(self.theme_frame_legenda, onvalue="ÁREA DE INTERESSE*",           offvalue="ÁREA DE INTERESSE",           textvariable=self.var_btn_ai, variable=self.var_btn_ai)
        self.btn_ge = ttk.Checkbutton(self.theme_frame_legenda, onvalue='GLEBAS ESTADUAIS*',            offvalue='GLEBAS ESTADUAIS',            textvariable=self.var_btn_ge, variable=self.var_btn_ge)
        self.btn_gf = ttk.Checkbutton(self.theme_frame_legenda, onvalue='GLEBAS FEDERAIS*',             offvalue='GLEBAS FEDERAIS',             textvariable=self.var_btn_gf, variable=self.var_btn_gf)
        self.btn_ae = ttk.Checkbutton(self.theme_frame_legenda, onvalue='ASSENTAMENTOS ESTADUAIS*',     offvalue='ASSENTAMENTOS ESTADUAIS ',    textvariable=self.var_btn_ae, variable=self.var_btn_ae)
        self.btn_af = ttk.Checkbutton(self.theme_frame_legenda, onvalue='ASSENTAMENTOS FEDERAIS*',      offvalue='ASSENTAMENTOS FEDERAIS',      textvariable=self.var_btn_af, variable=self.var_btn_af)
        self.btn_li = ttk.Checkbutton(self.theme_frame_legenda, onvalue='LOTES INCIDENTES*',            offvalue='LOTES INCIDENTES',            textvariable=self.var_btn_li, variable=self.var_btn_li)
        self.btn_te = ttk.Checkbutton(self.theme_frame_legenda, onvalue='TÍTULOS DEFINITVOS EXPEDIDOS*',offvalue='TÍTULOS DEFINITVOS EXPEDIDOS',textvariable=self.var_btn_te, variable=self.var_btn_te)   
        self.btn_qu = ttk.Checkbutton(self.theme_frame_legenda, onvalue='QUILOMBO*',                    offvalue='QUILOMBO',                    textvariable=self.var_btn_qu, variable=self.var_btn_qu)
        self.btn_pe = ttk.Checkbutton(self.theme_frame_legenda, onvalue='PEAEX*',                       offvalue='PEAEX',                       textvariable=self.var_btn_pe, variable=self.var_btn_pe)
        self.btn_limites = ttk.Checkbutton(self.theme_frame_legenda, onvalue ="LIMITES ( ativado  )",   offvalue="LIMITES (desativado)",        textvariable=self.var_btn_limites,variable=self.var_btn_limites)
        self.btn_info_cart = ttk.Checkbutton(self.theme_frame_legenda, onvalue ="INFOR. CARTO. (ON)",   offvalue="INFOR. CARTO. (OFF)",         textvariable=self.var_btn_info_cart,variable=self.var_btn_info_cart)

        btn_ai_args = partial(self.control.func_legenda_visibilidade_camada, 'AREA DE INTERESSE',       self.btn_ai)
        btn_ge_args = partial(self.control.func_legenda_visibilidade_camada, 'GLEBAS ESTADUAIS',        self.btn_ge)
        btn_gf_args = partial(self.control.func_legenda_visibilidade_camada, 'GLEBAS FEDERAIS',         self.btn_gf)
        btn_ae_args = partial(self.control.func_legenda_visibilidade_camada, 'ASSENTAMENTOS ESTADUAIS', self.btn_ae)
        btn_af_args = partial(self.control.func_legenda_visibilidade_camada, 'ASSENTAMENTOS FEDERAIS',  self.btn_af)
        btn_li_args = partial(self.control.func_legenda_visibilidade_camada, 'LOTES INCIDENTES',        self.btn_li)
        btn_te_args = partial(self.control.func_legenda_visibilidade_camada, 'LOTES TITULADOS',         self.btn_te)
        btn_qu_args = partial(self.control.func_legenda_visibilidade_camada, 'QUILOMBO',               self.btn_qu)
        btn_pe_args = partial(self.control.func_legenda_visibilidade_camada, 'PEAEX',                    self.btn_pe)
        btn_limites_args = partial(self.control.func_legenda_visibilidade_camada_imediata, 'LIMITES',self.btn_limites)
        btn_info_cart_args = partial(self.control.func_legenda_visibilidade_camada_imediata, 'INFORMACOES_CARTOGRAFICAS', self.btn_info_cart)

        self.btn_ai.configure(command=btn_ai_args)
        self.btn_ge.configure(command=btn_ge_args)
        self.btn_gf.configure(command=btn_gf_args)
        self.btn_ae.configure(command=btn_ae_args)
        self.btn_af.configure(command=btn_af_args)
        self.btn_li.configure(command=btn_li_args)
        self.btn_te.configure(command=btn_te_args)
        self.btn_qu.configure(command=btn_qu_args)
        self.btn_pe.configure(command=btn_pe_args)
        self.btn_limites.configure(command=btn_limites_args)
        self.btn_info_cart.configure(command=btn_info_cart_args)


        self.btn_ai.grid(sticky='nw',padx=5,pady=5, column=0, row=0)
        self.btn_ge.grid(sticky='nw',padx=5,pady=5, column=0, row=1)
        self.btn_gf.grid(sticky='nw',padx=5,pady=5, column=1, row=1)
        self.btn_ae.grid(sticky='nw',padx=5,pady=5, column=0, row=2)
        self.btn_af.grid(sticky='nw',padx=5,pady=5, column=1, row=2)
        self.btn_li.grid(sticky='nw',padx=5,pady=5, column=0, row=3)
        self.btn_te.grid(sticky='nw',padx=5,pady=5, column=1, row=3)
        self.btn_qu.grid(sticky='nw',padx=5,pady=5, column=0, row=4)
        self.btn_pe.grid(sticky='nw',padx=5,pady=5, column=1, row=4)
        self.btn_limites.grid(sticky='nw',padx=5,pady=5,column=0, row=5)
        self.btn_info_cart.grid(sticky='nw',padx=5,pady=5,column=1, row=5)


    def func_inserir_dados_salvos(self):
        pasta_automap = "C:\\Users\\{}\\Documents\\AutoMap".format(self.model.nome_usuario)
        #dados_de_entrada = pasta_automap + "\\DADOS_DE_ENTRADA.txt"

        sd = pasta_automap + "\\DADOS_DE_ENTRADA"
        try:
            files = list(filter(os.path.isfile, glob.glob(sd +'\\' + "*.txt")))
            files.sort(key=lambda x: os.path.getmtime(x))
            self.arquivo = files[-1]

        except Exception as e:
            print("Exception: ", e.__class__.__name__)
            pass

        if self.arquivo:
            if os.path.exists(self.arquivo):
                with open(self.arquivo) as f:
                    txt = f.read()

                lista_de_dados = list(map(lambda x:x.split('->')[1].strip(), txt.split('\n')[:-1]))
                variaveis = [
                    self.ano_Entry,
                    self.numero_Entry,
                    self.situacao_Entry,
                    self.interessado_Entry,
                    self.denominacao_Entry,
                    self.municipio_Entry,
                    self.carta_Entry,
                    self.zoneamento_Entry,
                    self.caminho_projeto_mxd_Entry,
                    self.caminho_para_salvar_Entry,
                    self.caminho_arquivo_shp_ou_txt_Entry,
                ]

                for index, valor in enumerate(lista_de_dados):
                    variaveis[index].insert(0, valor)

                messagebox.showinfo(title="Dados Carregados", message="Os dados da sessão anterior foram carregados com sucesso")
        
        else:
            self.ano_Entry.insert(0, '2022')
            self.numero_Entry.insert(0, '12345')
            self.situacao_Entry.insert(0, 'REGULARIZAÇÃO NÃO ONEROSA')
            self.interessado_Entry.insert(0, 'FULANO DA SILVA')
            self.denominacao_Entry.insert(0, 'SÍTIO FAZENDA')
            self.municipio_Entry.insert(0, 'BELÉM')
            self.carta_Entry.insert(0, 'SA.22-V-D-I')
            self.zoneamento_Entry.insert(0, 'ZEE: Zona de Consolidação II')
         
            self.caminho_projeto_mxd_Entry.insert(0, 'C:\\Users\\{}\\layout_padrao.mxd'.format(self.model.nome_usuario))
            self.caminho_para_salvar_Entry.insert(0, 'C:\\Users\\{}\\pasta'.format(self.model.nome_usuario))
        

class Control:

    camadas_legenda = {}
    legendas_ativas = []
    caminho_projeto_mxd_atual = None
    camada_limite_ativada = None
    camada_informacoes_ativada = None

    def __init__(self, model, view):
        self.model = model
        self.view = view


    def criar_subpastas(self):
        """Cria as subpastas."""
        
        pastas = self.model.lista_de_pastas

        for pasta in pastas:
            caminho_da_pasta = os.path.join(self.model.nome_diretorio, pasta)

            if not os.path.exists(caminho_da_pasta):
                os.mkdir(caminho_da_pasta)
                print("Criando: {}".format(caminho_da_pasta))
            else:
                print("{} Ja existe.".format(caminho_da_pasta))


    def download_imagens_internet(self):
        """Baixa as imagens da internet."""

        # para cada imagem dentro da lista de imagens ele baixa e ja joga no diretorio
        pasta_destino = os.path.join(self.model.nome_diretorio, self.model.pasta_das_imagens)

        for img in self.model.lista_de_imgs:
            pasta_final = os.path.join(pasta_destino ,img.split('/')[-1])

            if not os.path.exists(pasta_final):
                print("Baixando {}...".format(img.split('/')[-1]))
                requisicao = requests.get(img).content
                
                with open(pasta_final, 'wb') as handler:
                    handler.write(requisicao)
            else:
                print("{} Já existe.".format(img.split('/')[-1]))



    def start(self):
        self.view.define(self, self.model)
        self.view.setup()
        self.view.start_main_loop()


    def func_botao_atualizar_preview(self, *args):

        def get_random_string(length):
            # With combination of lower and upper case
            result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
            return result_str


        print("Atualizando previzualização!")
        # import arcpy # nao precisa caso seja importando na parte de cima do codigo
        if not self.caminho_projeto_mxd_atual:
            self.caminho_projeto_mxd_atual = self.view.caminho_projeto_mxd_Entry.get().encode('utf-8')

        if not len(self.caminho_projeto_mxd_atual) > 1:
            messagebox.showinfo(title='Arquivo .mxd faltando', message='Por favor, selecione pelo menos um arquivo mxd, para poder realizar a atualização da pré-vizualização.')
        

        print("caminho_projeto_mxd: {}".format(self.caminho_projeto_mxd_atual))

        mxd = arcpy.mapping.MapDocument(self.caminho_projeto_mxd_atual)
        df = arcpy.mapping.ListDataFrames(mxd,"*")[0]
        outpath_gif = "{}\\{}".format( os.path.dirname(__file__).replace('/','\\').replace('c:\\','C:\\'), self.view.nome_da_imagem_gif )
        random_name = get_random_string(20)
        random_name_outpath_gif = "{}\\{}".format( os.path.dirname(__file__).replace('/','\\').replace('c:\\','C:\\'), random_name )
        c = "{}\\{}".format(os.path.dirname(__file__).replace('/','\\').replace('c:\\','C:\\'), "previzs")
        if not os.path.exists(c):
            os.mkdir(c)

        random_name_outpath_gif = "{}\\{}".format( os.path.dirname(__file__).replace('/','\\').replace('c:\\','C:\\'), "previzs\\" + random_name )
        
        for cmd in arcpy.mapping.ListLayers(mxd):
            if cmd.name == 'LIMITES':
                if self.camada_limite_ativada:
                    cmd.visible = True
                else:
                    cmd.visible = False

            if cmd.name == 'INFORMACOES_CARTOGRAFICAS':
                if self.camada_informacoes_ativada:
                    cmd.visible = True
                else:
                    cmd.visible = False


            

        print('Executando função de exportGIF')

        shape_ou_txt = self.view.caminho_arquivo_shp_ou_txt_Entry.get().encode('utf-8')

        # Se shape, aplicar zoom, e simbologia antes de exportar a imagem
        if len(shape_ou_txt) > 1:
            print('len > 1: aplicando zoom')
            shape = arcpy.mapping.Layer(shape_ou_txt)
            arcpy.mapping.AddLayer(df, shape, "TOP")
            cmd_1 = arcpy.mapping.ListLayers(mxd)[0]

            zoom_camada(camada=cmd_1, mxd=mxd, data_frame=df)
            print('zoom aplicado com sucesso!')


            # TODO ERRO BEM AQUI: TypeError
            # Corrigido
            aplicar_simbologia(
                projeto_mxd=mxd,
                nome_camada_estilo_a_copiar='AREA DE INTERESSE',
                camada_a_aplicar=cmd_1,
                )


        arcpy.mapping.ExportToGIF(
            map_document=mxd,
            out_gif=outpath_gif,
            data_frame=df,
            df_export_width=585,
            df_export_height=413,
            )

        
        arcpy.mapping.ExportToGIF(
            map_document=mxd,
            out_gif=random_name_outpath_gif,
            data_frame=df,
            df_export_width=585,
            df_export_height=413,
            )
            
        print("Concluido!")
        print('executando mudanca de fotos')
        self.new_imagem_de_previzualizacao = tkinter.PhotoImage(file="{}\\{}".format(os.path.dirname(__file__).replace('/','\\').replace('c:\\','C:\\'), self.view.nome_da_imagem_gif))
        self.view.objeto_canvas.create_image(0,0,anchor='nw',image=self.new_imagem_de_previzualizacao)
        print('concluido e alterado?')


    def func_selecionar_arquivo_projeto_mxd(self, *args):
        if self.view.caminho_projeto_mxd_Entry:
            self.view.caminho_projeto_mxd_Entry.delete(0, 'end')
            self.view.caminho_projeto_mxd_Entry.insert(0, '')

        filetypes = (('shape files', '*.mxd'),('All files', '*.*'))
        filename = fd.askopenfilename(title='Selecionar um arquivo .mxd - Layout ArcMAP 10.x', initialdir='C:\\Users\\{0}'.format(self.model.nome_usuario), filetypes=filetypes)
        self.view.caminho_projeto_mxd_Entry.insert(0, filename)
        
        if filename:
            if filename.endswith('.txt'):
                messagebox.showinfo(title='Arquivo de Texto', message='Arquivo de Texto selecionado:\n\n{}'.format(filename))
            if filename.endswith('.txt'):
                messagebox.showinfo(title='Arquivo Shapefile', message='Arquivo Shapefile selecionado:\n\n{}'.format(filename))
        else:
            messagebox.showinfo(title='Arquivo Ausente', message='Nenhum arquivo foi selecionado')


    def func_selecionar_diretorio_exportar_produtos(self, *args):
        if self.view.caminho_para_salvar_Entry:
            self.view.caminho_para_salvar_Entry.delete(0, 'end')
            self.view.caminho_para_salvar_Entry.insert(0, '')

        foldername = fd.askdirectory(title='Selecione um diretório')
        self.view.caminho_para_salvar_Entry.insert(0, foldername)
        if foldername:
            #messagebox.showinfo(title='Diretório Selecionado', message=foldername)
            pass
        else:
            messagebox.showinfo(title='Diretório Ausente', message='Nenhum diretório foi selecionado')


    def func_abrir_arc_map(self, *args):
        arcgis_path = ":\\Program Files (x86)\\ArcGIS\\Desktop10.8\\bin\\ArcMap.exe"

        if os.path.exists("C"+arcgis_path):
            subprocess.Popen('{}'.format("C"+arcgis_path))
        elif os.path.exists("Z"+arcgis_path):
            subprocess.Popen('{}'.format("Z"+arcgis_path))
        else:
            messagebox.showinfo(title="Executavel não encontrado",message="Não foi possível localizar o ArcMap 10.8 no seu computador!\n\nTalvez tenha sido instalado em outro diretório não padrão, ou você não possui o ArcMap em seu computador.")


    def func_selecionar_arquivo(self, *args):
        if self.view.caminho_arquivo_shp_ou_txt_Entry:
            self.view.caminho_arquivo_shp_ou_txt_Entry.delete(0, 'end')
            self.view.caminho_arquivo_shp_ou_txt_Entry.insert(0, '')

        filetypes = (("shapefiles e textos","*.shp *.txt"),('shapefiles', '*.shp'),('texto', '*.txt'),('Todos os arquivos', '*.*'))
        filename = fd.askopenfilename(title='Selecionar um arquivo .txt ou .shp', initialdir='C:\\Users\\{0}'.format(self.model.nome_usuario), filetypes=filetypes)
        self.view.caminho_arquivo_shp_ou_txt_Entry.insert(0, filename)
        
        if filename:
            if filename.endswith('.txt'):
                msg = 'Arquivo de texto selecionado:\n\n{}'.format(filename)
                messagebox.showinfo(title='Arquivo de Texto selecionado', message=msg)
                self.view.variable.set(self.view.list_dropdown_options[0])
                messagebox.showinfo(title='Informar dados adicionais necessários', message='Por favor selecionar EPSG, e formatação das coordenadas')

            if filename.endswith('.shp'):
                msg = 'Arquivo Shapefile selecionado:\n\n{}'.format(filename)
                messagebox.showinfo(title='Arquivo Shapefile selecionado', message=msg)
                self.view.variable.set(self.view.list_dropdown_options[1])
                #messagebox.showinfo(title='Informar dados adicionais necessários', message='Por favor selecionar EPSG, e formatação das coordenadas')
        else:
            messagebox.showinfo(title='Arquivo Ausente', message='Nenhum arquivo foi selecionado')


    def func_legenda_visibilidade_camada(self, btn_name, btn_estado):

        if 'selected' in btn_estado.state():
            self.legendas_ativas.append(btn_name)
            print("{} >> SELECIONADO. append".format(btn_name))
        else:
            self.legendas_ativas.remove(btn_name)
            print("{} >> DESELECIONADO. remove".format(btn_name))
        

    def func_legenda_visibilidade_camada_imediata(self, btn_name, btn_estado):

        if not self.caminho_projeto_mxd_atual:
            self.caminho_projeto_mxd_atual = self.view.caminho_projeto_mxd_Entry.get().encode('utf-8')

        if not self.camadas_legenda:
            self.camadas_legenda = { i.name:i for i in arcpy.mapping.ListLayers(
                arcpy.mapping.MapDocument(
                    self.caminho_projeto_mxd_atual))
                }
        if 'selected' in btn_estado.state():
            print("{} >> SELECIONADO".format(btn_name))
            # self.camadas_legenda[btn_name].visible = True
            if btn_name == 'LIMITES':
                self.camada_limite_ativada = True
            if btn_name == 'INFORMACOES_CARTOGRAFICAS':
                self.camada_informacoes_ativada = True

        else:
            print("{} >> DESELECIONADO".format(btn_name))
            # self.camadas_legenda[btn_name].visible = False
            if btn_name == 'LIMITES':
                self.camada_limite_ativada = False
            if btn_name == 'INFORMACOES_CARTOGRAFICAS':
                self.camada_informacoes_ativada = False


    def func_legenda_visibilidade_camada_OLD(self, btn_name, btn_estado):
        
        if not self.model.caminho_projeto_mxd_legenda:
            self.model.caminho_projeto_mxd_legenda = self.view.caminho_projeto_mxd_Entry.get().encode('utf-8')
        
        if not self.camadas_legenda:
            self.camadas_legenda = { i.name:i for i in arcpy.mapping.ListLayers(
                arcpy.mapping.MapDocument(
                    self.model.caminho_projeto_mxd_legenda))
                }
     
        if 'selected' in btn_estado.state():
            print("{} >> SELECIONADO".format(btn_name))
            self.camadas_legenda[btn_name].visible = True
            
        else:
            print("{} >> DESELECIONADO".format(btn_name))
            self.camadas_legenda[btn_name].visible = False

    # FUNCIONANDO 100%
    def func_atualiza_situacao(self, mxd, municipios='MOJU', *args):
        """Atualiza o mapa de situacao de acordo com as 
        entradas fornecidas (1 ou mais): EX.:
        att_situacao('BELÉM','ACARÁ',...)"""

        print("Carregando unicodes...")
        UNICODES_LOWERCASE = ['\xc3\xa1',
            '\xc3\xa9','\xc3\xad',
            '\xc3\xb3','\xc3\xba',
            '\xc3\xa3','\xc3\xb5',
            '\xc3\xa2','\xc3\xaa',
            '\xc3\xae','\xc3\xb4',
            '\xc3\xbb','\xc3\xa7',
            ]

        UNICODES_UPPERCASE = ['\xc3\x81',
            '\xc3\x89','\xc3\x8d',
            '\xc3\x93','\xc3\x9a',
            '\xc3\x83','\xc3\x95',
            '\xc3\x82','\xc3\x8a',
            '\xc3\x8e','\xc3\x94',
            '\xc3\x9b','\xc3\x87',
            ]

        print("Carregando Definitions Querys")
        DEFINITION_QUERY_SITUACAO = {
            1:"{}nmSede = \'{}\'",
            2:"{}\"nmMun\" <> \'{}\'",
            3:"{}\"nmMun\" = \'{}\'",
            }

        P = DEFINITION_QUERY_SITUACAO
        UNI = UNICODES_UPPERCASE
        uni = UNICODES_LOWERCASE

        
        #print("Iniciando Operacoes")
        municipio = tuple([municipios]) + args
        #print(municipio)
        EXP = ['1', '2', '3']
        fz = 1.084556648631034
        df = False
        
        
        print("Carregando Projeto Atual...")


        print("Analisando Camadas...")
        cmds = arcpy.mapping.ListLayers(mxd)
        cdi = [cmd for exp in EXP for cmd in cmds if cmd.description[:1] == exp]
        
        if municipio[0] == 'nenhum':
            e1 = e2 = e3 = ""
            for i, (c, exp) in enumerate(zip(cdi, [e1, e2, e3])):
                c.definitionQuery = exp
            arcpy.RefreshActiveView()
            return

        if not df:
            df = arcpy.mapping.ListDataFrames(mxd)[-1]

        if municipio and isinstance(municipio, tuple):
            lm = []
            for m in municipio:
                m = m.upper()
                for u, U in zip(uni, UNI):
                    m = m.replace(u,U)
                lm.append(m)
            for i, v in enumerate(lm):
                if i == 0:
                    e1 = P[1].format("", v)
                    e2 = P[2].format("", v)
                    e3 = P[3].format("", v)
                    continue
                e1 += P[1].format(" OR ", v)
                e2 += P[2].format(" AND ",v)
                e3 += P[3].format(" OR ", v)

        if municipio and isinstance(municipio, str):
            municipio = municipio.upper()
            for u, U in zip(uni, UNI):
                municipio = municipio.replace(u,U)
                m = municipio

            e1 = P[1].format("",m)
            e2 = P[2].format("",m)
            e3 = P[3].format("",m)
        
        for i, (c, exp) in enumerate(zip(cdi, [e1, e2, e3])):
            c.definitionQuery = exp
            if i == 2:
                z = c.getSelectedExtent()
        print("Aplicando Zoom..")
        df.extent = z
        df.scale *= fz
        print()



        print('municipio',municipio)
        print('EXP',EXP)
        print('fz',fz)
        print('df',df)
        print('mxd',mxd)
        print('cmds',cmds)
        print('cdi',cdi)
        print('df',df)
        print('z',z)
        
        print(df.extent)
        print(df.scale)


    def func_exportar_mapa(self, ano, numero, situacao, interessado, denominacao, municipio, carta, zoneamento, instance):
        
        if not len(self.view.caminho_arquivo_shp_ou_txt_Entry.get()) > 1:
            self.view.log_text_Label['text'] = 'Nenhum shape ou coordenadas foram imformadas'
            messagebox.messagebox.showinfo("Shapefile ou Coordenadas Ausentes", "Por favor selecione um arquivo do tipo Shapefile (.shp) ou um arquivo de Texto (.txt) contendo as coordenadas do poligono ou ponto para iniciar a produção do mapa")
            return

        self.view.log_text_Label['text'] = 'Importando bibliotecas GIS, realizando operações...'
        messagebox.messagebox.showinfo("Iniciando Processo", "Por favor aguarde enquanto os procedimentos estão sendo realizados")
        
        caminho_projeto_mxd = self.view.caminho_projeto_mxd_Entry.get().encode('utf-8')
        caminho_para_salvar = self.view.caminho_para_salvar_Entry.get().encode('utf-8')

        ano_str = ano.get().encode('utf-8')
        numero_str = numero.get().encode('utf-8')

        print(ano_str, numero_str)

        nome_mxd = '{}_{}.mxd'.format(ano_str, numero_str)
        novo_mxd = "{}\\{}".format(caminho_para_salvar, nome_mxd)
        

        mxd = arcpy.mapping.MapDocument(caminho_projeto_mxd)
        df = arcpy.mapping.ListDataFrames(mxd,"*")[0]
        shape_ou_txt = self.view.caminho_arquivo_shp_ou_txt_Entry.get().encode('utf-8')
        
        if not len(shape_ou_txt) > 1:
            print("LEN MENOR QUE 1 MENOR!")

        shape = arcpy.mapping.Layer(shape_ou_txt)
        arcpy.mapping.AddLayer(df, shape, "TOP")
        print("Inserindo na camada_a_ser_bufada o valor correspondente a: ", shape_ou_txt )
        #buffer300 = criar_buffer(camada_a_ser_bufada=shape_ou_txt, data_frame_to_add=df, distancia_metros=300)
        municipio_fornecido = self.view.municipio_Entry.get().encode('utf-8')
        municipio_fornecido.replace("'","")
        self.func_atualiza_situacao(mxd, municipio_fornecido)
        
        camadas_nome_mapa = { i.name:i for i in arcpy.mapping.ListLayers(mxd)}
        
        for i in self.legendas_ativas:
            camadas_nome_mapa[i].visible = True
            

                
        for i in arcpy.mapping.ListLayers(mxd):
            if i.name == shape.name:
                shape = i

        #area_limitacao(shape)
        print("Aplicando Zoom")
        #_, camada = zoom(mxd, shape, df)
        print("Escala aplicada com sucesso!")
        print("Aplicando Simbologia")
        #aplicar_simbologia('AREA DE INTERESSE', camada)

        print('municipio_fornecido',municipio_fornecido)
        print("Atualizando Situacao!")
        

        print("Simbologia aplicada com sucesso!")

        valores = {}
        
        pretexto_zee = "2- "
        pretexto_carta = "1- FOLHA/CIM / "
        valores["ano"] = self.view.ano_Entry.get().encode('utf-8')
        valores["numero"] = self.view.numero_Entry.get().encode('utf-8')
        valores["situacao"] = self.view.situacao_Entry.get().encode('utf-8')
        valores["interessado"] = self.view.interessado_Entry.get().encode('utf-8')
        valores["denominacao"] = self.view.denominacao_Entry.get().encode('utf-8')
        valores["municipio"] = self.view.municipio_Entry.get().encode('utf-8')
        valores["texto_carta"] = self.view.carta_Entry.get().encode('utf-8')
        valores["zoneamento"] = self.view.zoneamento_Entry.get().encode('utf-8')
        
        if valores["denominacao"].startswith("SEM DENO"):
            valores["denominacao"] = valores["interessado"];

        print("Atualizando Titulo do Projeto")
        mxd.title = "{0}/{1}".format(valores["ano"], valores["numero"])

        print("Atualizando Sumario do Projeto")
        mxd.summary = "{0} - {1}".format(valores["situacao"], valores["interessado"])

        print("Atualizando Author do Projeto")
        mxd.author = 'Djalma Filho'

        print("Atualizando Creditos do Projeto")
        mxd.credits = valores["denominacao"]

        print("Atualizando Descricao do Projeto")
        mxd.description = pretexto_carta + valores["texto_carta"] + '\n' + pretexto_zee + valores["zoneamento"]

        print("Salvando Thumbnail.")
        mxd.makeThumbnail()

        print("Layout Atualizado com Sucesso!")
        print('mxd', mxd)
        print('novo_mxd', novo_mxd)
        novo_mxd = novo_mxd.replace('/','\\')

        print('novo_mxd com replace', novo_mxd)
        # saves file into 10.1 version of arcgis
        while True:
            variar_nome = 1
            print("While Loop, var:{}".format(variar_nome))
            if not os.path.exists(novo_mxd):
                print("Nao existe@!")
                break
            else:
                print("Existe@!")
                novo_mxd = novo_mxd[:-1] + str(variar_nome)
                print('novo_mxd com variar', novo_mxd)

            variar_nome += 1
                
        
        mxd.saveACopy(file_name=novo_mxd, version=101)
        
        pdf_name = novo_mxd[:-4] + '.pdf'

        mxd_novo_mxd = arcpy.mapping.MapDocument(novo_mxd)
        df_novo_mxd = arcpy.mapping.ListDataFrames(mxd_novo_mxd,"*")[0]
        cmd_1_novo_mxd = arcpy.mapping.ListLayers(mxd_novo_mxd)[0]

        zoom_camada(
            camada=cmd_1_novo_mxd,
            mxd=mxd_novo_mxd,
            data_frame=df_novo_mxd
            )

        #area_limitacao(cmd_1_novo_mxd, df_novo_mxd, mxd_novo_mxd, 400)
        # Distancia do Buffer para o mapa
        area_limitacao(
            camada_a_ser_bufada=cmd_1_novo_mxd,
            data_frame_to_add=df_novo_mxd,
            arquivo_mxd=mxd_novo_mxd,
            distancia_metros=800
            )
        
        aplicar_simbologia(
            projeto_mxd=mxd_novo_mxd,
            nome_camada_estilo_a_copiar='AREA DE INTERESSE',
            camada_a_aplicar=cmd_1_novo_mxd
            )

        arcpy.mapping.ExportToPDF(
            map_document=mxd_novo_mxd,
            data_frame='PAGE_LAYOUT',
            out_pdf=pdf_name,
            df_export_width=1600,
            df_export_height=1200,
            )

        print("salvando novo mxd")
        mxd_novo_mxd.saveACopy(file_name=novo_mxd[:-4]+'F.mxd', version=101)

        print("Excluindo mxd place holder...")

        # Exclui PlaceHolder
        def relatar(): print("mxd placeholder não existe")
        try:
            if os.path.exists(novo_mxd):
                os.remove(novo_mxd) 
            else:
                relatar()
        except Exception as e:
            print(e)
            print('\nNome do Erro: {}'.format(e.__class__.__name__))
            print("\nArquivo mxd placeholder não Excluído!")

        # mensagem
        messagebox.messagebox.showinfo("Concluido", "Salvamento Concluído!")
        # open window on the current file
        subprocess.Popen('explorer /select, "{0}"'.format(novo_mxd.replace('/','\\').replace('c:\\','C:\\'),))




if __name__ == "__main__":
    control = Control(Model(), TkView())
    control.start()




# Para Ativar ou desativar a vizualização

# informacoes_cartograficas
	
# 	CARTA_INDICE_IBGE_DSG
# 	ZEE_2010
# 	FUSOS


# jurisdicao
	
# 	GLEBAS_ESTADUAIS
# 	ASSENTAMENTOS_ESTADUAIS
# 	GLEBAS_FEDERAIS
# 	ASSENTAMENTOS_FEDERAIS

