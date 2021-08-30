import class_jogo,random
jogos=class_jogo.jogo()
pecasPontos={"K":0,"Q":10,"T":5,"C":3,"B":3,"P":1}
checkmate =100
impasse=0


def movimentosAleatorios(movValidos):
 return movValidos[random.randint(0,len(movValidos)-1)]

#minimax
def melhorMovimento(jogo,movValidos):

    trocar_jogador= 1 if jogo.brancoMovimento else -1

    inimigoMinimaxPonto= checkmate #ai tem de reduzir

    melhor_mov_Jogador=None
    #random.shuffle(movValidos)
    jogos.pr=0
    mv=movValidos
    i=len(movValidos)
    for jogador_mov in mv:
       print("este preto ",i)
       jogo.fazerMovimento(jogador_mov)

       inimigo_Mov=jogo.getMovimentosValidos()

       if jogo.impasse:
           inimigo_ponto_max=impasse
       elif jogo.checkMate:
           inimigo_ponto_max=-checkmate
       else:
           inimigo_ponto_max=-checkmate
           for inimigo_Mov in inimigo_Mov:

                 print("estou no branco COM I",i)

                 jogo.fazerMovimento(inimigo_Mov,jogada_AI=False)
                 jogo.getMovimentosValidos()

                 if jogo.checkMate:
                       ponto=checkmate
                 elif jogo.impasse:
                        ponto=impasse
                 else:
                    ponto=-trocar_jogador*pontuar(jogo.lista_tabuleiro)

                 if ponto>inimigo_ponto_max:
                    print("a minha melhor jogada banco e esta",ponto)
                    inimigo_ponto_max=ponto
                 jogo.desfazer_movimento()
           print("----------------------------------------------")

       if inimigo_ponto_max<inimigoMinimaxPonto:
            print("a melhor jogada no branco ",inimigo_ponto_max,"jogada no preto e",inimigoMinimaxPonto)
            inimigoMinimaxPonto=inimigo_ponto_max
            melhor_mov_Jogador=jogador_mov
       jogo.desfazer_movimento()
       i=i-1
    jogos.pr=1
    return melhor_mov_Jogador

#pontuar o tabuleiro
def pontuar(tabuleiro):
    ponto=0
    for linha in tabuleiro:
        for quadro in linha:
            if quadro[0]=='B':
                ponto+=pecasPontos[quadro[1]]
            elif quadro[0]=='P':
                ponto-=pecasPontos[quadro[1]]
        print("o ponto que dei  ",ponto," ",quadro[1],linha)
    print("o ponto que retonei e ",ponto)
    return ponto