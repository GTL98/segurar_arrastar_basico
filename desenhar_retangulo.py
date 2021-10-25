class DesenharRetangulos:
    def __init__(self, posicao_centro, tamanho=[200, 200]):
        self.posicao_centro = posicao_centro
        self.tamanho = tamanho
        
    def atualizar(self, cursor, x1, x2, y1, y2):
        cx, cy = self.posicao_centro
        largura, altura = self.tamanho
        
        # Se a ponta do dedo indicador está dentro do retângulo
        if x1 < cursor[8][0] < x2 and y1 < cursor[8][1] < y2:
            self.posicao_centro = cursor[8][0], cursor[8][1]
