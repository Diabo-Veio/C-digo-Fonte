from io import StringIO
from string import ascii_uppercase as alc
from pathlib import Path
import os
import errno
#-----------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------#

## VARIAVEL GLOBAL PARA ARMAZENAR O NOME DOS ARQUIVOS ##
Arquivos_gerados = []


#-----------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------#


def Pdb_String_Manipulation(caminho,nome_certo,Moleculas,nome,Numero_Atm,Metodo,Alterar_Nucleos,Nucleos,Alterar_Ram,Ram):
    global Molecula, Molecula_Alvo, Arquivos_gerados
    Texto = StringIO(Moleculas)
    Linhas = []
    n_linha = 0
    while True:
        n_linha += 1
        linha = Texto.readline()
        if linha[0:3] == "HET":
            Linhas.append(linha)
            print(Linhas)
        if linha[0:3] == "CON":
            break

    nome_completo = nome_certo + ".inp"
    print(nome_completo)

    with open(caminho + "Resultados/" + nome_completo,"w") as outfile:
        outfile.writelines([str(i) for i in Linhas])