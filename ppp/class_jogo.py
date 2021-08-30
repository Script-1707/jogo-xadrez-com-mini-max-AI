import abc

class jogo():
    def __init__(self):
        self.lista_tabuleiro=[

             ["PT","PB","PC","PQ","PK"],
             ["PP","PP","PP","PP","PP"],
             ["__","__","__","__","__"],
             ["BP","BP","BP","BP","BP"],
             ["BT","BB","BC","BQ","BK"]
        ]


        self.funcoes_movimento={'P':self.getM_Piao,'T':self.getM_Torre,'B':self.getM_Bispo,
                                'C':self.getM_Cavalo,'Q':self.getM_Queen,'K':self.getM_King}

        self.brancoMovimento =True
        self.movP=[]
        self.rei_BrancoLoc= (4,4)
        self.rei_PretoLoc = (0,4)
        self.checkMate=False
        self.impasse=False#impasse
        self.pr=1
        self.turno=[]
        self.jogada=None
        self.jogada2=None


    def fazerMovimento(self,movimento,jogada_AI=False,final=False,inicio=False):


        self.lista_tabuleiro[movimento.iniciaLinha][movimento.iniciaColuna]="__"
        self.lista_tabuleiro[movimento.fimLinha][movimento.fimColuna]=movimento.pecaMovida
        self.movP.append(movimento)
        self.brancoMovimento = not self.brancoMovimento


        if movimento.pecaMovida =='BK':
           self.rei_BrancoLoc=(movimento.fimLinha,movimento.fimColuna)
        elif movimento.pecaMovida=='PK':
           self.rei_PretoLoc=(movimento.fimLinha,movimento.fimColuna)

        p=movimento.pecaMovida[0]

        if final==True:
            if inicio==True:
                print("Start Game")

            if len(self.turno)==0:
                self.turno.append(movimento.getNotacao())
            else:
                passado=self.turno.pop()

                self.jogada=(passado+" Black Played "+movimento.getNotacao())
                self.jogada2=("White Played "+passado+" "+movimento.getNotacao())
                self.turno=[]

                #passado=1
        if self.pr==1 and jogada_AI==True:
            if movimento.promocao :
                 promocaoPeca= input("promover para  Q , T , C , B :")
                 self.lista_tabuleiro[movimento.fimLinha][movimento.fimColuna]=movimento.pecaMovida[0]+promocaoPeca



    def desfazer_movimento(self):
        if len(self.movP)!=0:
            movimento=self.movP.pop()
            self.lista_tabuleiro[movimento.iniciaLinha][movimento.iniciaColuna]=movimento.pecaMovida
            self.lista_tabuleiro[movimento.fimLinha][movimento.fimColuna]=movimento.pecaJogada
            self.brancoMovimento = not self.brancoMovimento

            if movimento.pecaMovida=='BK':
               self.rei_BrancoLoc=(movimento.iniciaLinha,movimento.iniciaColuna)
            elif movimento.pecaMovida=='PK':
               self.rei_PretoLoc=(movimento.iniciaLinha,movimento.iniciaColuna)

#todos movimentos do xadrez

    def getMovimentosValidos(self):
        #1-gerar todos movimentos possiveis

        movimentos=self.getMovimentosPossiveis()
        #2-para cada movimeto ,fazer movimento
        self.pr=0
        for i in range(len(movimentos)-1,-1,-1):

            self.fazerMovimento(movimentos[i])

              #3-gerar movimentos do inimigo e verificar se ele esta ou vai atacar o rei


            self.brancoMovimento = not self.brancoMovimento
            estado=self.emChek()


            if estado==True:
                movimentos.remove(movimentos[i]) #se atacar o rei nao é um mov valido
            self.brancoMovimento= not self.brancoMovimento
            self.desfazer_movimento()
        self.pr=1
        if len(movimentos)==0:
            if self.emChek:
                self.checkMate=True
            else:
                self.impasse=True
        else:
            self.checkMate=False
            self.impasse=False

        return movimentos



#em chek
    def emChek(self):
        if self.brancoMovimento:

            return self.quadro_em_ataque(self.rei_BrancoLoc[0],self.rei_BrancoLoc[1])
        else:
            #print("vi que o rei preto esta em chek")
            return self.quadro_em_ataque(self.rei_PretoLoc[0],self.rei_PretoLoc[1])


#verifica se o inimigo pode atacar uma posicao (l,c)
    def quadro_em_ataque(self,l,c):
        self.brancoMovimento=not self.brancoMovimento
        inimigo_mov=self.getMovimentosPossiveis()
        self.brancoMovimento=not self.brancoMovimento

        for mov in inimigo_mov:
            if(mov.fimLinha==l and mov.fimColuna==c):
               return True

        return False

#todos movimentos possiveis

    def getMovimentosPossiveis(self):
        movimentos=[]
        #movimentos=[movimentacao((3,0),(2,0),self.lista_tabuleiro)]

        for l in range (len(self.lista_tabuleiro)): #num linhas
            for c in range(len(self.lista_tabuleiro[l])):#num colunas
                turn=self.lista_tabuleiro[l][c][0]
                if (turn=='B' and self.brancoMovimento) or (turn=='P' and not self.brancoMovimento):
                    peca=self.lista_tabuleiro[l][c][1]
                    '''
                    if peca=='P':
                        self.getM_Piao(l,c,movimentos)
                    '''
                    #print(funcoes_movimento[peca])
                    self.funcoes_movimento[peca](l,c,movimentos)
        return movimentos
# ____________________movimentos____________________________________
#gerar todos os movimentos das pecas em funcao da linha e coluna e add na lista


#_Piao  - uma ou duas casas para cima e diginal para atacar o inimigo
    def getM_Piao(self,l,c,movimentos):
        p=False

        if self.brancoMovimento:
            if self.lista_tabuleiro[l-1][c]=="__":

                movimentos.append(movimentacao((l,c),(l-1,c),self.lista_tabuleiro))

            if c-1>=0:
                if self.lista_tabuleiro[l-1][c-1][0]=='P':
                    if l-1==0:
                       p=True
                    movimentos.append(movimentacao((l,c),(l-1,c-1),self.lista_tabuleiro))
            if c+1<=4:
                if self.lista_tabuleiro[l-1][c+1][0]=='P':
                    if l-1==0:
                       p=True
                    movimentos.append(movimentacao((l,c),(l-1,c+1),self.lista_tabuleiro))
        else:
            #print("sou preto")
            #print("aqui o l",l+1)
            if(l+1==5):
                l=3
            if self.lista_tabuleiro[l+1][c]=="__" and 0<=l+1<=4:
                movimentos.append(movimentacao((l,c),(l+1,c),self.lista_tabuleiro))

            if c-1>=0:
               if self.lista_tabuleiro[l+1][c-1][0]=='B':
                   movimentos.append(movimentacao((l,c),(l+1,c-1),self.lista_tabuleiro))
            if c+1<=4:
               if self.lista_tabuleiro[l+1][c+1][0]=='B':
                   movimentos.append(movimentacao((l,c),(l+1,c+1),self.lista_tabuleiro))


#_Torre - todos  lados menos digonais
    def getM_Torre(self,l,c,movimentos):
        direcoes=((-1,0),(0,-1),(1,0),(0,1))
        inimigo="P" if self.brancoMovimento else "B"

        for d in direcoes:
            for i in range(1, 5):
                fimLinha=l+d[0]*i
                fimColuna=c+d[1]*i
                if 0<=fimLinha<5 and 0<=fimColuna<5:
                    peca=self.lista_tabuleiro[fimLinha][fimColuna]
                    if peca=="__":
                        movimentos.append(movimentacao((l,c),(fimLinha,fimColuna),self.lista_tabuleiro))
                    elif peca[0]==inimigo:
                        movimentos.append(movimentacao((l,c),(fimLinha,fimColuna),self.lista_tabuleiro))
                        break
                    else:
                        break
                else:
                    break
#_Bispo -todas diagonais
    def getM_Bispo(self,l,c,movimentos):
        direcoes=((-1,-1),(-1,1),(1,-1),(1,1))
        inimigo="P" if self.brancoMovimento else "B"
        for d in direcoes:
            for i in range(1, 5):
                fimLinha=l+d[0]*i
                fimColuna=c+d[1]*i
                if 0<=fimLinha<5 and 0<=fimColuna<5:
                    peca=self.lista_tabuleiro[fimLinha][fimColuna]
                    if peca=="__":
                        movimentos.append(movimentacao((l,c),(fimLinha,fimColuna),self.lista_tabuleiro))
                    elif peca[0]==inimigo:
                        movimentos.append(movimentacao((l,c),(fimLinha,fimColuna),self.lista_tabuleiro))
                        break
                    else:
                        break
                else:
                    break


#_Cavalo
    def getM_Cavalo(self,l,c,movimentos):
        cavalo=((-2,-1),(-2,1),(-1,2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        cor="B" if self.brancoMovimento else "P"
        for i in cavalo:
            fimLinha=l+i[0]
            fimColuna=c+i[1]
            if 0<=fimLinha<5 and 0<=fimColuna<5:
                peca=self.lista_tabuleiro[fimLinha][fimColuna]
                if peca[0] != cor:
                    movimentos.append(movimentacao((l,c),(fimLinha,fimColuna),self.lista_tabuleiro))


#_Rainha
    def getM_Queen(self,l,c,movimentos):
        self.getM_Torre(l,c,movimentos)
        self.getM_Bispo(l,c,movimentos)

#_Rei -uma casa em todos sentidos
    def getM_King(self,l,c,movimentos):
        rei=((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        cor="B" if self.brancoMovimento else "P"

        #print("a cor e ",cor,rei[1][0])
        for i in range(7):
            fimLinha  =l+rei[i][0]
            fimColuna =c+rei[i][1]
            if 0<=fimLinha< 5 and 0<=fimColuna <5:
                fimPeca=self.lista_tabuleiro[fimLinha][fimColuna]
                if fimPeca[0]!= cor:
                    movimentos.append(movimentacao((l,c),(fimLinha,fimColuna),self.lista_tabuleiro))
                    #print("posso mver para", fimLinha , fimColuna)

#______________________________________________________________________

class movimentacao():
      indo_linha={"1":4,"2":3,"3":2,"4":1,"5":0}
      linhas ={v:k for k,v in indo_linha.items()}
      indo_colunas={"a":0,"b":1,"c":2,"d":3,"e":4}
      colunas ={v:k for k,v in indo_colunas.items()}

      def __init__(self,iniM,fimM,tabuleiro):#parametro passant é opcional
        self.iniciaLinha=iniM[0]
        self.iniciaColuna=iniM[1]

        self.fimLinha=fimM[0]
        self.fimColuna=fimM[1]
        self.pecaMovida=tabuleiro[self.iniciaLinha][self.iniciaColuna]
        self.pecaJogada=tabuleiro[self.fimLinha][self.fimColuna]

        #Promocao
        self.promocao= ((self.pecaMovida=='BP' and self.fimLinha==0 ) or (self.pecaMovida=='PP' and self.fimLinha==4))
         #       self.promocao=True

        #passant
        #self.emPassant=False

        self.movimentacaoId=self.iniciaLinha*1000+self.iniciaColuna*100+self.fimLinha*10+self.fimColuna
        #print("id")
        #print(self.movimentacaoId)



      def __eq__(self,aux):
        if isinstance(aux,movimentacao):
            return self.movimentacaoId==aux.movimentacaoId
        return False

      def getNotacao(self):
             return self.getJogadaArquivo(self.iniciaLinha,self.iniciaColuna)+self.getJogadaArquivo(self.fimLinha,self.fimColuna)
      def getJogadaArquivo(self,l,c):
            return self.colunas[c]+self.linhas[l]
