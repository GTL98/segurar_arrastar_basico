# 1. Importar as bibliotecas
import cv2
import cvzone
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from desenhar_retangulo import DesenharRetangulos
            
# 2. Carregar o módulo de desenhar o retângulo
retangulo = DesenharRetangulos([150, 150])

# 3. Carregar o módulo de detecção
detector = HandDetector(maxHands=1, detectionCon=0.8, minTrackCon=0.8)

# 4. Definir o tamanho da tela
largura_tela = 1280
altura_tela = 720

# 5. Definir a cor inicial do retângulo
cor = (255, 0, 255)

# 6. Definir os parâmetros iniciais do retângulo
cx, cy, largura_ret, altura_ret = 100, 100, 200, 200

# 7. Definir transparência
transparencia = 0

# 8. Captura de vídeo
cap = cv2.VideoCapture(0)
cap.set(3, largura_tela)
cap.set(4, altura_tela)

while True:
    # Detectar as mãos
    sucesso, imagem = cap.read()
    imagem = cv2.flip(imagem, 1)
    maos, imagem = detector.findHands(imagem, flipType=False)
    
    # Extrair as informações das mãos
    if maos:
        # Descobrir a distância entre a ponta do indicador e a ponta do médio
        mao = maos[0]
        cursor = mao['lmList']
        comprimento, _, _ = detector.findDistance(cursor[8], cursor[12], imagem)
        if comprimento < 20:
            # Chamar a função de atualização aqui para criar vários retângulos
            retangulo.atualizar(cursor, x1, x2, y1, y2)
    
    if transparencia == 0:
        # Atualizar a posição dos retângulos
        cx, cy = retangulo.posicao_centro
        largura_ret, altura_ret = retangulo.tamanho

        # Variáveis dos retângulos
        x1 = cx-largura_ret//2
        x2 = cx+largura_ret//2
        y1 = cy-altura_ret//2
        y2 = cy+altura_ret//2

        # Desenhar os retângulos que iremos interagir
        cv2.rectangle(imagem, (x1, y1), (x2, y2), cor, cv2.FILLED)

        # Desenhar as quinas do retângulo
        cvzone.cornerRect(imagem, (x1, y1, largura_ret, altura_ret), 20, rt=0)
        
        # Mostrar a imagem na tela (sem transparência)
        cv2.imshow('Segurar e Arrastar', imagem)
    
    if transparencia == 1:
        imagem_nova = np.zeros_like(imagem, np.uint8)
        # Atualizar a posição dos retângulos
        cx, cy = retangulo.posicao_centro
        largura_ret, altura_ret = retangulo.tamanho

        # Variáveis dos retângulos
        x1 = cx-largura_ret//2
        x2 = cx+largura_ret//2
        y1 = cy-altura_ret//2
        y2 = cy+altura_ret//2

        # Desenhar os retângulos que iremos interagir
        cv2.rectangle(imagem_nova, (x1, y1), (x2, y2), cor, cv2.FILLED)

        # Desenhar as quinas do retângulo
        cvzone.cornerRect(imagem_nova, (x1, y1, largura_ret, altura_ret), 20, rt=0)
        
        saida = imagem.copy()
        alfa = 0.5
        mascara = imagem_nova.astype(bool)
        saida[mascara] = cv2.addWeighted(imagem, alfa, imagem_nova, 1-alfa, 0)[mascara]
        
        # Mostrar a imagem na tela (com transparência)
        cv2.imshow('Segurar e Arrastar', saida)
  
    # Terminar o loop
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break
        
# 9. Fechar a tela de captura
cap.release()
cv2.destroyAllWindows()