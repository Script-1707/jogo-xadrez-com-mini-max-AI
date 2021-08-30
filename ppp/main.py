import class_jogo,jogador_AI
import pygame as p


altura=largura=400
dimencao=5
tamanho=altura // dimencao
num_fps=15
img={}
#funcao para carregar as imagens no tabuleiro
def carregar_img():
   pecas=['BB','BC','BK','BP','BQ','BT','PB','PC','PK','PQ','PT','PP']
   for peca in pecas:
        img[peca]=p.transform.scale(p.image.load("img/"+peca+".png"),(tamanho,tamanho))

def main():

    movimentacaoB=0
    movimentacaoP=0

    p.init()
    tela=p.display.set_mode((altura, largura)) #
    clock=p.time.Clock()
    tela.fill(p.Color("white"))
    jogos=class_jogo.jogo()
    movimentos_validos=jogos.getMovimentosValidos()
    m=jogador_AI
    moveMade=False #ver min 00:25:16



    carregar_img()
    carregar=True
    boxSelecionada=()
    jogada=[]

    gameOver=False
    jogador=True #humano=true,|, IA=FALSE
    jogador2=False

    while carregar:
       turnoHumano=(jogos.brancoMovimento and jogador) or (not jogos.brancoMovimento and jogador2)
       for e in p.event.get():
            if e.type==p.QUIT:
                carregar=False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and turnoHumano:
                    localizacao = p.mouse.get_pos()
                    coluna=localizacao[0]//tamanho
                    linha=localizacao[1]//tamanho
                    if boxSelecionada==(linha,coluna):
                        boxSelecionada=()#apagar
                        jogada=[]
                    else:
                        boxSelecionada=(linha,coluna)
                        jogada.append(boxSelecionada)
                    if len(jogada)==2:
                         mov=class_jogo.movimentacao(jogada[0],jogada[1],jogos.lista_tabuleiro)

                         for i in range(len(movimentos_validos)):
                            if mov == movimentos_validos[i]:

                                inicio=False
                                if movimentacaoB==0:
                                    inicio=True
                                    movimentacaoB=1
                                jogos.fazerMovimento(movimentos_validos[i],jogada_AI=True,final=True,inicio=inicio)
                                moveMade=True
                                boxSelecionada=()
                                jogada=[]
                         else:
                            jogada=[]
                            boxSelecionada=()
            elif e.type == p.KEYDOWN:
                if e.key ==p.K_z:
                    jogos.desfazer_movimento()#undoMove
                    boxSelecionada=()
                    jogada=[]
                    moveMade=True
       # AI
       if not gameOver and not turnoHumano:
            ai=jogador_AI.melhorMovimento(jogos,movimentos_validos)
            if ai is None:
                ai=jogador_AI.movimentosAleatorios(movimentos_validos)

            jogos.fazerMovimento(ai,final=True)

            if inicio==True:
                 with open('jogador1.txt','w') as carregar:
                      carregar.write("Start Game"+'\n')

                 with open('jogador1.txt','a') as carregar:
                      carregar.write("White"+'\n')

                 with open('jogador2.txt','w') as carregar:
                      carregar.write("Start Game"+'\n')

                 with open('jogador2.txt','a') as carregar:
                      carregar.write("Black"+'\n')

            with open('jogador1.txt','a') as carregar:
                  carregar.write(str(jogos.jogada)+'\n')

            with open('jogador2.txt','a') as carregar:
                  carregar.write(str(jogos.jogada2)+'\n')



            moveMade=True


       if moveMade:
             movimentos_validos=jogos.getMovimentosValidos()


             moveMade=False

       desenhar_jogo(tela,jogos)

       if jogos.checkMate:
            gameOver=True
            if jogos.brancoMovimento:
                escrever(tela,"Vitoria do preto Checkmate")
            else:
                escrever(tela,"Vitoria do Branco Checkmate")
       elif jogos.impasse:
            gameOver=True
            escrever(tela,"Empate")

       clock.tick(num_fps)
       p.display.flip()
       p.display.update()


def desenhar_jogo(tela,jogo):
    desenharTabuleiro(tela)
    desenharPecas(tela,jogo.lista_tabuleiro)

def desenharTabuleiro(tela):
    cores=[p.Color("white"),p.Color("gray")]
    for r in range(dimencao):
        for c in range(dimencao):
            cor=cores[((r+c)%2)]
            p.draw.rect(tela,cor,p.Rect(c*tamanho,r*tamanho,tamanho,tamanho))

def desenharPecas(tela,tabuleiro):
    for r in range(dimencao):
        for c in range(dimencao):
            peca=tabuleiro[r][c]
            if peca !="__":
                tela.blit(img[peca],p.Rect(c*tamanho,r*tamanho,tamanho,tamanho))

def escrever(tela,texto):
    font=p.font.SysFont("helvitca",32,True,False)
    textObject=font.render(texto,0,p.Color('Black'))
    localizacao_texto=p.Rect(20,150,50,50)
    tela.blit(textObject,localizacao_texto)
#if __name__ =="__main":
main()
