from io import StringIO
from string import ascii_uppercase as alc
from pathlib import Path
from Complementar import *
import os
import errno

#-----------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------#

## VARIAVEL GLOBAL PARA ARMAZENAR O NOME DOS ARQUIVOS ##
Arquivos_gerados = []
caminho = ""
## GLOBAL PARA DEFINIR O METODO E USAR NA EDIÇÃO E CÓPIA ##
Novo_Metodo = ""

#-----------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------#

## MÉTODOS ##
Metodo_original = '''# avogadro generated ORCA input file 
# Basic Mode
# 
! RHF SP def2-SVP 
'''

#-----------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------#

## ZERA A LISTA DE  ARQUIVOS GERADOS CASO O PROGRAMA SEJA EXECUTADO MAIS DE UMA VEZ ##
def zerar():
    global Arquivos_gerados
    Arquivos_gerados = []

## METODO INICIAL PARA DEFINIR OS PÂMETROS PARA A MANIPULAÇÃO DAS STRINGS ##
def Inp_String_Manipulation(caminho,nome,Moleculas,Numero_Atm,Metodo,Alterar_Nucleos,Nucleos,Alterar_Ram,Ram):
    global Molecula, Molecula_Alvo, Arquivos_gerados

    ## CONTADORES ##
    Atm = 0
    Molecula_Alvo = 0
    Molecula = 1

    ## REMOVE O METODO INICIAL E O SEPARA O * QUE MARCA O INICIO DOS ATOMOS PARA DICIONARMOS DEPOIS ##
    inicio = Moleculas[73:84]
    Mol_Limpas = Moleculas[84:]

    ## DEFINE O NUMERO DE MOLECULAS A VERIFICAR ##
    Numero_Mol = (Mol_Limpas.count("\n")-2)/Numero_Atm

    ## CHAMA O METODO PARA EDITARMOS OS ARQUIVOS ##
    for i in range(int(Numero_Mol)):
        Molecula_Alvo += 1
        Texto = StringIO(Mol_Limpas)
        Manipulation(caminho,nome,Numero_Atm,Atm,Texto,Metodo,inicio,alc[i],Alterar_Nucleos,Nucleos,Alterar_Ram,Ram)
        
    ## CRIA UMA CÓPIA DO ARQUIVO ORIGINAL NA PASTA DE RESULTADOS ##
    Texto = StringIO(Mol_Limpas)
    Copia(caminho,Novo_Metodo,inicio,Texto,nome)

## METODO PARA EDIÇÃO DE STRINGS ##
def Manipulation(caminho,nome_certo,Numero_Atm,Atm,Texto,Metodo,inicio,letra,Alterar_Nucleos,Nucleos,Alterar_Ram,Ram):
    global Molecula, Arquivos_gerados,Novo_Metodo

    ## LISTAS PARA INSERIRMOS AS LINHAS ##
    lista = []
    lista2 = []
    lista3 = []
    Molecula = 1

    ## DEFINE O NOME DO ARQUIVO ##
    nome_completo = nome_certo + letra + ".inp"

    ## LOOP PARA EDIÇÃO DAS LINHAS ##
    while True:
        ## LÊ AS LINHAS ##
        linha = Texto.readline()
        
        ## VERIFICA SE CHEGAMOS AO FINAL NO ARQUIVO PARA PARAR A ITERAÇÃO ##
        if linha == "*\n":
            break

        ## IDENTIFICA QUE CHEGAMOS NA PRÓXIMA MOLECULA ##
        if Atm == Numero_Atm :
            Molecula += 1
            Atm = 0

        ## ADICIONA A LINHA NA LISTA SE CHEGAMOS NA MOLECULA ALVO ##
        if Molecula == Molecula_Alvo:
            while True:
                ## ADICIONA LINHA NA LISTA ##
                lista.append(linha)
                ## PASSA PARA O PRÓXIMO ÁTOMO ##
                Atm += 1
                ## VERIFICA SE ACABOU A MOLECULA, PASSA PARA A PROXIMA MOLECULA E ENCERRA O LOOP ##
                if Atm == Numero_Atm:
                    Atm = 0
                    Molecula += 1
                    break
                ## LÊ A PROXIMA LINHA ##
                linha = Texto.readline()
                
        ## INICIA A EDIÇÃO SE NÃO ESTAMOS NA MOLECULA ALVO ##
        elif Molecula < Molecula_Alvo or Molecula > Molecula_Alvo:
            ## EDITA A LINHA DA MOLECULA##
            linha_rep = linha.replace(linha[3:5],linha[3]+":")
            ## ADICIONA A LINHA DA MOLECULA NA LISTA CORRETA ##
            if  Molecula < Molecula_Alvo:
                lista2.append(linha_rep)
            elif  Molecula > Molecula_Alvo:
                lista3.append(linha_rep)
            ## PASSA PARA O PRÓXIMO ÁTOMO ##
            Atm += 1
    
    ##VERIFICA SE JA EXISTE UMA PASTA DE RESULTADOS ##
    if not os.path.exists(os.path.dirname(caminho + "Resultados")):
        try:
            ## CRIA A PASTA DE RESULTADOS SE NÃO EXISTIR ##
            os.mkdir(os.path.dirname(caminho + "Resultados/"))
        except OSError as exc:
            ## CASO DE ALGUM ERRO ##
            if exc.errno != errno.EEXIST:
                raise
    
    ##EDITA O METODO
    if(Alterar_Nucleos):
        a = Metodo.replace(Metodo[72:74], Nucleos)
        Novo_Metodo = a
        if(Alterar_Ram):
            b = a.replace(Metodo[89:93], Ram)
            Novo_Metodo = b
    elif(Alterar_Ram):
        a = Metodo.replace(Metodo[89:93], Ram)
        Novo_Metodo = a
    else: Novo_Metodo = Metodo

    ## ESCREVE O ARQUIVO ##
    with open(caminho + "Resultados/" + nome_completo,"w") as outfile:
        outfile.write(Novo_Metodo)
        outfile.writelines("\n")
        outfile.write(inicio)
        outfile.writelines([str(i) for i in lista2])
        outfile.writelines([str(i) for i in lista])
        outfile.writelines([str(i) for i in lista3])
        outfile.writelines("*\n")

    ## ADICIONA O ARQUIVO NA LISTA PARA GERAR O EXECUTÁVEL ##
    Arquivos_gerados.append(nome_completo)

