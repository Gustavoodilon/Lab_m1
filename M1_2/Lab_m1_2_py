import cv2 as cv
import numpy as np
import os
import csv

def clipe_valor(valor):
    """Garante que o valor fique no intervalo [0, 255]."""
    if valor < 0:
        return 0
    elif valor > 255:
        return 255
    else:
        return int(valor)

def carregar_imagem_cinza(caminho):
    """Carrega a imagem e converte para tons de cinza se for colorida, como preparação."""
    img = cv.imread(caminho)
    if img is None:
        print(f"Erro: Falha na leitura da imagem '{caminho}'.")
        return None
    
    if len(img.shape) == 3:
        print("Imagem colorida detectada. Extraindo o canal V (brilho) ou convertendo para cinza...")
        #Uma conversão rápida para cinza 
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        
    return img

def ajuste_brilho(img, b):
    print(f"1. Ajustando brilho (b = {b})...")
    altura, largura = img.shape
    resultado = np.zeros((altura, largura), dtype=np.uint8)

    for i in range(altura):
        for j in range(largura):
            #Soma com casting para int
            novo_valor = int(img[i, j]) + b
            resultado[i, j] = clipe_valor(novo_valor)
            
    return resultado

def ajuste_contraste(img, alpha):
    print(f"2. Ajustando contraste (alpha = {alpha})...")
    altura, largura = img.shape
    resultado = np.zeros((altura, largura), dtype=np.uint8)

    for i in range(altura):
        for j in range(largura):
            #g(x,y) = alpha * (f(x,y) - 128) + 128
            novo_valor = round(alpha * (int(img[i, j]) - 128) + 128)
            resultado[i, j] = clipe_valor(novo_valor)
            
    return resultado

def negativo(img):
    print("3. Gerando negativo...")
    altura, largura = img.shape
    resultado = np.zeros((altura, largura), dtype=np.uint8)

    for i in range(altura):
        for j in range(largura):
            resultado[i, j] = 255 - int(img[i, j])
            
    return resultado

def limiarizacao(img, T):
    print(f"4. Aplicando limiarização (T = {T})...")
    #Guarda de limiar válido
    if T < 0 or T > 255:
        print("Aviso: Limiar T fora do intervalo [0, 255]. Resultados podem ser todos pretos ou brancos.")
        
    altura, largura = img.shape
    resultado = np.zeros((altura, largura), dtype=np.uint8)

    for i in range(altura):
        for j in range(largura):
            if int(img[i, j]) < T:
                resultado[i, j] = 0
            else:
                resultado[i, j] = 255
                
    return resultado

def calcular_histograma(img, nome_arquivo):
    print(f"5. Calculando histograma: {nome_arquivo}...")
    altura, largura = img.shape
    
    #Estrutura com 256 posições zeradas
    histograma = [0] * 256

    #Contabiliza as intensidades
    for i in range(altura):
        for j in range(largura):
            intensidade = int(img[i, j])
            histograma[intensidade] += 1

    #Registra em CSV
    caminho_csv = os.path.join("saidas", nome_arquivo)
    with open(caminho_csv, mode='w', newline='') as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        escritor.writerow(['intensidade', 'quantidade'])
        for intensidade, quantidade in enumerate(histograma):
            escritor.writerow([intensidade, quantidade])

def main():
    pasta_saida = "saidas"
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    nome_imagem = "Imagem3.png"
    img = carregar_imagem_cinza(nome_imagem)
    if img is None: return

    #5. Histograma da Original
    calcular_histograma(img, "hist_original.csv")

    #1. Ajuste de Brilho
    img_brilho_neg = ajuste_brilho(img, -50)
    img_brilho_pos = ajuste_brilho(img, 50)
    cv.imwrite(f"{pasta_saida}/brilho_negativo.png", img_brilho_neg)
    cv.imwrite(f"{pasta_saida}/brilho_positivo.png", img_brilho_pos)
    calcular_histograma(img_brilho_pos, "hist_brilho_positivo.csv")

    #2. Ajuste de Contraste
    img_contraste_reduzido = ajuste_contraste(img, 0.5)
    img_contraste_identidade = ajuste_contraste(img, 1.0)
    img_contraste_ampliado = ajuste_contraste(img, 1.5)
    cv.imwrite(f"{pasta_saida}/contraste_reduzido.png", img_contraste_reduzido)
    cv.imwrite(f"{pasta_saida}/contraste_identidade.png", img_contraste_identidade)
    cv.imwrite(f"{pasta_saida}/contraste_ampliado.png", img_contraste_ampliado)
    calcular_histograma(img_contraste_ampliado, "hist_contraste_ampliado.csv")

    #3. Negativo
    img_negativo = negativo(img)
    cv.imwrite(f"{pasta_saida}/negativo.png", img_negativo)

    #4. Limiarização
    img_limiar_100 = limiarizacao(img, 100)
    img_limiar_200 = limiarizacao(img, 200)
    cv.imwrite(f"{pasta_saida}/limiar_100.png", img_limiar_100)
    cv.imwrite(f"{pasta_saida}/limiar_200.png", img_limiar_200)

    print("Todas as operações do Laboratório M1.2 foram concluídas com sucesso!")

if __name__ == "__main__":
    main()