from INP import *
from PDB import *

## VARIAVEL GLOBAL PARA ARMAZENAR O NOME DOS ARQUIVOS ##
caminho = ""
## GLOBAL PARA DEFINIR O METODO E USAR NA EDIÇÃO E CÓPIA ##
Novo_Metodo = ""

Metodo_1 = '''! SP wB97X-d3 RIJCOSX def2-tzvp def2/J def2-tzvp/C TightSCF
%pal nprocs 22 end 
%maxcore 3000
%scf Guess Pmodel end'''
Metodo_2 = '''! SP wB97X-d3 RIJCOSX def2-tzvp def2/J def2-tzvp/C TightSCF
%pal nprocs 19 end 
%maxcore 3000
%scf Guess Pmodel end'''
Metodo_3 = '''! SP wB97X-d3 RIJCOSX def2-tzvp def2/J def2-tzvp/C TightSCF
%pal nprocs 22 end 
%maxcore 3000
%scf Guess Hueckel end'''
Metodo_4 = '''! SP wB97X-d3 RIJCOSX def2-tzvp def2/J def2-tzvp/C TightSCF
%pal nprocs 19 end 
%maxcore 3000
%scf Guess Hueckel end'''

def tipo(tipo_arquivo,Moleculas,nome_original,Numero_Atm,Metodo_escolhido,Alterar_Nucleos,Nucleos,Alterar_Ram,Ram):
    global caminho
    caminho = ""
    ## DEFINE O METODO ##
    if Metodo_escolhido == 1:
        Metodo = Metodo_1
    elif Metodo_escolhido == 2:
        Metodo = Metodo_2
    elif Metodo_escolhido == 3:
        Metodo = Metodo_3
    elif Metodo_escolhido == 4:
        Metodo = Metodo_4
    
        ## DEFINE O NOME DO ARQUIVO ##
    
    if tipo_arquivo == "pdb":
        nome = nome_original.removesuffix(".pdb")
    else:
        nome = nome_original.removesuffix(".inp")
    res = nome.split("/", -1)
    nome_certo = res[-1] if len(res) > 1 else ""

    ## DEFINE O CAMINHO PARA O ARQUIVO ##
    res.remove(nome_certo)
    for i in res:
        caminho += i + '/'
    print(nome_certo)
    if tipo_arquivo == "pdb":
        Pdb_String_Manipulation(caminho,nome_certo,Moleculas,Numero_Atm,Metodo,Alterar_Nucleos,Nucleos,Alterar_Ram,Ram)
    ## VERIFICA SE O ARQUIVO ESCOLHIDO É VALIDO (RECEM SAÍDO DO AVOGRADO) ##
    elif tipo_arquivo == "inp" and Moleculas[:73] == Metodo_original:
        Inp_String_Manipulation(caminho,nome_certo,Moleculas,Numero_Atm,Metodo,Alterar_Nucleos,Nucleos,Alterar_Ram,Ram)        
        return 0
    else:
        ## RETORNA 1 NA FUNÇÃO CASO O ARQUIVO SEJA INVALIDO PARA LEVANTARMOS UM ERRO NO INTERFACE.PY ##
        return 1
    