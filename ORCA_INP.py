from tkinter.filedialog import askopenfilenames
from io import StringIO
from string import ascii_uppercase as alc
import os
import errno

## VARIAVEL GLOBAL PARA ARMAZENAR O NOME DOS ARQUIVOS ##
Arquivos_gerados = []
caminho = ""

## ABRE O ARQUIVO ##
def abrir():
    filename = askopenfilenames()
    return filename


def String_Manipulation(Moleculas,nome,Numero_Atm,Metodo,Alterar_Nucleos,Nucleos,Alterar_Ram,Ram):
    global Molecula, Molecula_Alvo
    ## VERIFICA SE O ARQUIVO ESCOLHIDO É VALIDO (RECEM SAÍDO DO AVOGRADO) ##
    if Moleculas[:73] == '''# avogadro generated ORCA input file 
# Basic Mode
# 
! RHF SP def2-SVP 
''':
        ## REMOVE O METODO INICIAL E O SEPARA O * QUE MARCA O INICIO DOS ATOMOS PARA DICIONARMOS DEPOIS ##
        inicio = Moleculas[73:84]
        Mol_Limpas = Moleculas[84:]

        ## DEFINE O METODO ##
        
        if Metodo == 1:
            Metodo_escolhido = '''! SP wB97X-d3 RIJCOSX def2-tzvp def2/J def2-tzvp/C TightSCF
%pal nprocs 22 end 
%maxcore 3000
%scf Guess Pmodel end'''
        elif Metodo == 2:
            Metodo_escolhido ='''! SP wB97X-d3 RIJCOSX def2-tzvp def2/J def2-tzvp/C TightSCF
%pal nprocs 19 end 
%maxcore 3000
%scf Guess Pmodel end'''
        elif Metodo == 3:
            Metodo_escolhido ='''! SP wB97X-d3 RIJCOSX def2-tzvp def2/J def2-tzvp/C TightSCF
%pal nprocs 22 end 
%maxcore 3000
%scf Guess Hueckel end'''
        elif Metodo == 4:
            Metodo_escolhido ='''! SP wB97X-d3 RIJCOSX def2-tzvp def2/J def2-tzvp/C TightSCF
%pal nprocs 19 end 
%maxcore 3000
%scf Guess Hueckel end'''

        ## DEFINE O NUMERO DE MOLECULAS A VERIFICAR ##
        Numero_Mol = (Mol_Limpas.count("\n")-2)/Numero_Atm

        ## CONTADORES ##
        Atm = 0
        i = 0
        Molecula_Alvo = 0
        Molecula = 1

        ## CHAMA O METODO PARA EDITARMOS OS ARQUIVOS ##
        for i in range(int(Numero_Mol)):
            Molecula_Alvo += 1
            sla = StringIO(Mol_Limpas)
            Manipulation(Numero_Atm,Atm,sla,Metodo_escolhido,inicio,nome,alc[i],Alterar_Nucleos,Nucleos,Alterar_Ram,Ram)
            i+=1
        ## CRIA UMA CÓPIA DO ARQUIVO ORIGINAL NA PASTA DE RESULTADOS ##
        sla = StringIO(Mol_Limpas)
        Copia(inicio,sla,Metodo_escolhido,Alterar_Nucleos,Nucleos,nome,Alterar_Ram,Ram)
        return 0
    else:
        return 1

## METODO PARA EDIÇÃO DE STRINGS ##
def Manipulation(Numero_Atm,Atm,sla,Metodo,inicio,nome1,letra,Alterar_Nucleos,Nucleos,Alterar_Ram,Ram):
    global Molecula, Arquivos_gerados,caminho
    ## LISTAS PARA INSERIRMOS AS LINHAS ##
    lista = []
    lista2 = []
    lista3 = []
    Molecula = 1
    ## DEFINE O NOME DO ARQUIVO ##
    nome = nome1.removesuffix(".inp")
    res = nome.split("/", -1)
    nome_certo = res[-1] if len(res) > 1 else ""
    ## DEFINE O CAMINHO PARA O ARQUIVO ##
    caminho = ''
    res.remove(nome_certo)
    for i in res:
        caminho += i + '/'
    nome_completo = nome_certo + letra + ".inp"

    ## LOOP PARA EDIÇÃO DAS LINHAS ##
    while True:
        ## LÊ AS LINHAS ##
        linha = sla.readline()
        
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
                ## PASSA PARA O PRÓXIMO ÁTOMO ##
                Atm += 1
                ## ADICIONA LINHA NA LISTA ##
                lista.append(linha)
                ## VERIFICA SE ACABOU A MOLECULA, PASSA PARA A PROXIMA MOLECULA E ENCERRA O LOOP ##
                if Atm == Numero_Atm:
                    Atm = 0
                    Molecula += 1
                    break
                ## LÊ A PROXIMA LINHA ##
                linha = sla.readline()
                
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
    if not os.path.exists(os.path.dirname(caminho + "Resultados/")):
        try:
            ## CRIA A PASTA DE RESULTADOS SE NÃO EXISTIR ##
            os.mkdir(os.path.dirname(caminho + "Resultados/"))
        except OSError as exc:
            ## CASO DE ALGUM ERRO ##
            if exc.errno != errno.EEXIST:
                raise
    
    ##EDITA O METODO
    if(Alterar_Nucleos):
        Novo_Metodo = Metodo.replace(Metodo[72:74], Nucleos)
    if(Alterar_Ram and Alterar_Nucleos):
        Novo_Metodo_2 = Novo_Metodo.replace(Metodo[89:93], Ram)
    else:
        Novo_Metodo = Metodo.replace(Metodo[89:93], Ram)

    ## ESCREVE O ARQUIVO ##
    with open(caminho + "Resultados/" + nome_completo,"w") as outfile:
        Arquivos_gerados.append(nome_completo)
        if(Alterar_Ram and Alterar_Nucleos):
            outfile.write(Novo_Metodo_2)
        elif (Alterar_Nucleos or Alterar_Ram):
            outfile.write(Novo_Metodo)
        else:
            outfile.write(Metodo)
        outfile.writelines("\n")
        outfile.write(inicio)
        outfile.writelines([str(i) for i in lista2])
        outfile.writelines([str(i) for i in lista])
        outfile.writelines([str(i) for i in lista3])
        outfile.writelines("*\n")

## COPIA O ARQUIVO QUE ESTÁ SENDO EDITADO PARA A PASTA DE RESULTADOS ##
def Copia(inicio,Moleculas,Metodo,Alterar_Nucleos,Nucleos,nome,Alterar_Ram,Ram):
    global Arquivos_gerados
    ## DEFINE O NOME DO ARQUIVO ##
    res = nome.split("/", -1)
    nome_certo = res[-1] if len(res) > 1 else ""

    ##EDITA O METODO
    if(Alterar_Nucleos):
        Novo_Metodo = Metodo.replace(Metodo[72:74], Nucleos)
    if(Alterar_Ram and Alterar_Nucleos):
        Novo_Metodo_2 = Novo_Metodo.replace(Metodo[89:93], Ram)
    else:
        Novo_Metodo = Metodo.replace(Metodo[89:93], Ram)

    ## ESCREVE O ARQUIVO DE SAIDA ##
    with open(caminho + "Resultados/" + nome_certo,"w") as outfile:
        Arquivos_gerados.append(nome_certo)
        if(Alterar_Ram and Alterar_Nucleos):
            outfile.write(Novo_Metodo_2)
        elif (Alterar_Nucleos or Alterar_Ram):
            outfile.write(Novo_Metodo)
        else:
            outfile.write(Metodo)
        outfile.writelines("\n")
        outfile.write(inicio)
        outfile.writelines(Moleculas)

## GERA O EXECUTAVEL PARA O ORCA ##
def Executavel():
    with open(caminho + "Resultados/" + "Energias" + ".ps1","w") as outfile:
        for i in Arquivos_gerados:
            out = i.removesuffix(".inp")
            outfile.writelines("C:\orca503\orca.exe " + i + " > " + out + ".out \n")
