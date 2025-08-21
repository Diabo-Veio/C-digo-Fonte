import tkinter as tk
from tkinter import PhotoImage
from ORCA_INP import *
from tkinter.ttk import *
from tkinter import messagebox
import sys
import os

#-----------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------#

## GAMBIARRA PARA PEGAR O CAMINHO ABSOLUTO DA IMAGEM E ADICIONAR O .EXE (funciona no pyinstaller)##
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

#-----------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------#

## CRIA INSTANCIA DO TKINTER ##
root = tk.Tk()
root.title("Pontuador")

## VARIAVEL PARA DEFINIR O METODO E NUMERO DE NUCLEOS##
Metodo = tk.IntVar(value=0)
Alterar_Nucleos = tk.BooleanVar(value=False)
Alterar_Ram = tk.BooleanVar(value=False)

## VARIÁVEIS GLOBAIS ##
Numero_Atm = ""
arquivos = []

#-----------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------#

## ETIQUETA PARA IDENTIFICAR O CAMPO DE DIGITAÇÃO ##
label1 = tk.Label(root,text="Número de átomos").grid(column=0,row=0)

## CAMPO PARA DIGITAR O NUMERO DE ATOMOS ##
entrada1 = tk.Entry(root)
entrada1.grid(column=0,row=1)

## BOTÕES PARA ESCOLHA DO METODO ##
tk.Radiobutton(root, text="Dimero Sem Iodo", variable= Metodo,value=1).grid(column=0,row=2)
tk.Radiobutton(root, text="Cluster Sem Iodo", variable= Metodo,value=2).grid(column=0,row=3)
tk.Radiobutton(root, text="Dimero com Iodo", variable= Metodo,value=3).grid(column=0,row=4)
tk.Radiobutton(root, text="Cluster com Iodo", variable= Metodo,value=4).grid(column=0,row=5)

## BOTÃO PARA ESCOLHER O ARQUIVO ##
button1 = tk.Button(root,text="selecionar arquivos", command= lambda:Escolher_Arquivo()).grid(column=0,row=6)

## BOTÃO PARA ALTERAR O NUMERO DE NÚCLEOS ##
tk.Checkbutton(root,text="Alterar número de nucleos", variable = Alterar_Nucleos,command=lambda:Alt_Nucleos()).grid(column=0,row=7)
entrada2 = tk.Entry(root)

## BOTÃO PARA ALTERAR A RAM ##
tk.Checkbutton(root,text="Alterar memória ram", variable = Alterar_Ram,command=lambda:Alt_Ram()).grid(column=0,row=9)
entrada3 = tk.Entry(root)

## BOTÃO GERAR OS OUTPUTS ##
button2 = tk.Button(root,text="Gerar arquivos", command= lambda:Gerar()).grid(column=0,row=11)

#-----------------------------------------------------------------------------------#
#-----------------------------------------------------------------------------------#

## MOSTRA/ESCONDE CAMPO PARA MUDANÇA DE NÚCLEOS ##
def Alt_Nucleos():
    if(Alterar_Nucleos.get()):
        entrada2.grid(column=0,row=8)
    else:
        entrada2.grid_forget()

## MOSTRA/ESCONDE CAMPO PARA MUDANÇA DE RAM ##
def Alt_Ram():
    if(Alterar_Ram.get()):
        entrada3.grid(column=0,row=10)
    else:
        entrada3.grid_forget()

## METODO PARA CHAMAR A EDIÇÃO DE STRINGS ##
def Escolher_Arquivo():
    global arquivos, Numero_Atm
    ## LÊ O NUMERO DE ATOMOS
    Numero_Atm = entrada1.get()
    ## VERIFICA SE O NUMERO DE ATOMOS NÃO É NULO E CHAMA UM ERRO SE FOR ##
    if Numero_Atm != "":
        ## ABRE OS ARQUIVOS ##
        arquivos = abrir()
    else:
       Nova_Aba()

## METODO PARA CHAMAR A EDIÇÃO DE STRINGS ##
def Gerar():
    if arquivos != []:
        ## ZERA AS VARIAVEIS PARA ATRIBUIR NOVOS VALORES ##
        Nucleos = 0
        Ram = 0
        ## DEFINE O NUMERO DE NÚCLEOS E MEMÓRIA RAM ##
        if(Alterar_Nucleos):
            Nucleos = entrada2.get()
        if(Alterar_Ram):
            Ram = entrada3.get()
        ## CHAMA O METODO UM VEZ POR ARQUIVO ##
        for arquivo in arquivos:
            ## LÊ O CAMINHO PARA O ARQUIVOS ##
            f = open(arquivo)
            ## LÊ O CONTEUDO DO ARQUIVO EM QUESTÃO ##
            Molecula = f.read()
            ## CHAMA O METODO PARA EDIÇÃO DAS LINHAS ##
            a = String_Manipulation(Molecula,arquivo,int(Numero_Atm),Metodo.get(),Alterar_Nucleos.get(),Nucleos,Alterar_Ram.get(),Ram)
            ## CHAMA O ERRO SE O ARQUIVO SELECIONADO NÃO FOR VALIDO ##
            if a == 1:
                messagebox.showerror(title="Erro",message="Selecione o arquivo correto")
        ## CRIA O EXECUTÁVEL PARA CHAMAR O ORCA ##
        print(Arquivos_gerados)
        Executavel()
        zerar()
    else: Nova_Aba()

## ERRO DO FAUSTÃO ##
class Nova_Aba():
    def __init__(self):
        self.abrir()
    def abrir(self):
        ## ABRE NOVA ABA ##
        self.new_window = tk.Toplevel()
        self.new_window.title("INFORMAÇÕES INCOMPLETAS")
        self.new_window.geometry("253x275") 
        ## ABRE A IMAGEM E MUDA O TAMANHO ##
        self.image_orig = PhotoImage(file=resource_path("erro.png"))
        self.image = self.image_orig.subsample(2, 2)
        ## COLOCA A IMAGEM NA TELA ##
        self.image_label = tk.Label(self.new_window, image=self.image)
        self.image_label.grid(column=0,row=0,sticky="W")
        self.image_label.image = self.image
        self.label = tk.Label(self.new_window,text="Arquivos ou Nº de Átomos Faltando")
        self.label.grid(column=0,row=1)

## ABRE O AVISO PARA LEMBRAR SOBRE O ARQUIVO DO AVOGRADO ##
def aviso():
    messagebox.showerror(title="LEMBRE-SE",message="ESSE PROGRAMA DEVE SER USADO DIRETAMENTE EM ARQUIVOS GERADOS PELO AVOGRADO")

## CHAMA O AVISO ##
aviso()

## INICIA O LOOP DA INSTANCIA DO TKINTER ##
root.mainloop()
