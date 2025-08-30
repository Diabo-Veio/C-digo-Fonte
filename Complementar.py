from pathlib import Path
from tkinter.filedialog import askopenfilenames

## ABRE O ARQUIVO ##
def abrir():
    filename = askopenfilenames()
    return filename

## COPIA O ARQUIVO QUE ESTÁ SENDO EDITADO PARA A PASTA DE RESULTADOS ##
def Copia(caminho,Novo_Metodo,inicio,Moleculas,nome):
    global Arquivos_gerados

    ## DEFINE O NOME DO ARQUIVO ##
    res = nome.split("/", -1)
    nome_certo = res[-1] if len(res) > 1 else ""

    ## ESCREVE O ARQUIVO DE SAIDA ##
    with open(caminho + "Resultados/" + nome_certo,"w") as outfile:
        outfile.write(Novo_Metodo)
        outfile.writelines("\n")
        outfile.write(inicio)
        outfile.writelines(Moleculas)
    ## ADICIONA O ARQUIVO NA LISTA PARA GERAR O EXECUTÁVEL ##
    Arquivos_gerados.append(nome_certo)

## GERA O EXECUTAVEL PARA O ORCA ##
def Executavel():
    ## CAMINHO PARA O EXECUTAVEL QUE CHAMA O ORCA ##
    Executavel_Orca = Path(caminho + "Resultados/" + "Energias" + ".ps1")
    ## ESCREVE O ARQUIVO EXECUTÁVEL DO ORCA ##
    with open(Executavel_Orca,"w") as outfile:
        for i in Arquivos_gerados:
            out = i.removesuffix(".inp")
            outfile.write("C:\orca503\orca.exe " + i + " > " + out + ".out \n")
