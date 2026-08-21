import cv2 as cv
import numpy as np
import os

def inspecao_imagem(img):
    altura, largura = img.shape[0], img.shape[1]
    canais = img.shape[2] if len(img.shape) == 3 else 1
    
    print("--- 1. Inspeção da Imagem ---")
    print(f"Largura: {largura} px")
    print(f"Altura: {altura} px")
    print(f"Número de canais: {canais}")
    print(f"Tipo da imagem (dtype): {img.dtype}")
    print(f"Total de pixels: {largura * altura}")

    if canais == 3:
        print("Tipo: Imagem colorida (BGR)")
        # Separa os canais apenas para o cálculo de estatísticas
        b, g, r = img[:,:,0], img[:,:,1], img[:,:,2]
        print(f"Canal B - Min: {b.min()}, Máx: {b.max()}, Média: {b.mean():.2f}")
        print(f"Canal G - Min: {g.min()}, Máx: {g.max()}, Média: {g.mean():.2f}")
        print(f"Canal R - Min: {r.min()}, Máx: {r.max()}, Média: {r.mean():.2f}")
        print(f"Geral   - Min: {img.min()}, Máx: {img.max()}, Média: {img.mean():.2f}")
    else:
        print("Tipo: Imagem em escala de cinza")
        print(f"Geral   - Min: {img.min()}, Máx: {img.max()}, Média: {img.mean():.2f}")
    print("-" * 30)

def criar_copia(img):
    print("2. Criando cópia exata...")
    altura, largura = img.shape[0], img.shape[1]
    canais = img.shape[2] if len(img.shape) == 3 else 1
    
    # É fundamental definir dtype=np.uint8
    if canais == 3:
        copia = np.zeros((altura, largura, canais), dtype=np.uint8)
    else:
        copia = np.zeros((altura, largura), dtype=np.uint8)

    for i in range(altura):
        for j in range(largura):
            if canais == 3:
                copia[i, j, 0] = img[i, j, 0]
                copia[i, j, 1] = img[i, j, 1]
                copia[i, j, 2] = img[i, j, 2]
            else:
                copia[i, j] = img[i, j]
                
    cv.imwrite("saidas/copy.png", copia)

def separar_canais(img):
    if len(img.shape) != 3:
        print("Erro: A imagem não é colorida, impossível separar canais.")
        return

    print("3. Separando canais B, G e R...")
    altura, largura = img.shape[:2]
    
    # Criamos três imagens 3D, pois precisamos zerar os outros canais da mesma estrutura BGR
    b_img = np.zeros((altura, largura, 3), dtype=np.uint8)
    g_img = np.zeros((altura, largura, 3), dtype=np.uint8)
    r_img = np.zeros((altura, largura, 3), dtype=np.uint8)

    for i in range(altura):
        for j in range(largura):
            b_img[i, j, 0] = img[i, j, 0] # Apenas Azul
            g_img[i, j, 1] = img[i, j, 1] # Apenas Verde
            r_img[i, j, 2] = img[i, j, 2] # Apenas Vermelho

    cv.imwrite("saidas/channel_b.png", b_img)
    cv.imwrite("saidas/channel_g.png", g_img)
    cv.imwrite("saidas/channel_r.png", r_img)

def niveis_cinza(img):
    if len(img.shape) != 3:
        print("Erro: Imagem já está em escala de cinza.")
        return img
        
    print("4. Convertendo para níveis de cinza (Média Simples e Ponderada)...")
    altura, largura = img.shape[:2]
    
    # Imagens cinza têm apenas 1 dimensão além de X e Y
    simples = np.zeros((altura, largura), dtype=np.uint8)
    ponderada = np.zeros((altura, largura), dtype=np.uint8)

    for i in range(altura):
        for j in range(largura):
            # Casting para int para evitar estouro (overflow) do uint8 na hora de somar
            b = int(img[i, j, 0])
            g = int(img[i, j, 1])
            r = int(img[i, j, 2])
            
            # Média Simples
            val_simples = (r + g + b) // 3
            
            # Média Ponderada
            val_ponderada = int(0.299 * r + 0.587 * g + 0.114 * b)
            
            # Atribuição
            simples[i, j] = val_simples
            ponderada[i, j] = val_ponderada

    cv.imwrite("saidas/gray_average.png", simples)
    cv.imwrite("saidas/gray_weighted.png", ponderada)
    
    # Retornamos a imagem ponderada para ser usada na quantização
    return ponderada

def quantizacao(img_gray):
    print("5. Realizando a quantização (16, 8, 4 e 2 níveis)...")
    altura, largura = img_gray.shape
    niveis = [16, 8, 4, 2]
    
    for n in niveis:
        quantizada = np.zeros((altura, largura), dtype=np.uint8)
        
        # Tamanho de cada "balde" de pixels
        tamanho_intervalo = 256 / n
        
        # Fator para expandir o nível de volta ao intervalo 0-255 visualmente
        fator_expansao = 255 / (n - 1)
        
        for i in range(altura):
            for j in range(largura):
                pixel = img_gray[i, j]
                
                # Descobre em qual nível/degrau o pixel atual se encaixa
                nivel = int(pixel / tamanho_intervalo)
                
                # Mapeia o nível de volta para o intervalo (0-255)
                novo_valor = int(nivel * fator_expansao)
                
                # Guarda para garantir que não passe de 255
                if novo_valor > 255: novo_valor = 255
                if novo_valor < 0: novo_valor = 0
                    
                quantizada[i, j] = novo_valor
                
        cv.imwrite(f"saidas/quant_{n}.png", quantizada)

def main():
    # Guarda: cria o diretório de saídas se não existir
    if not os.path.exists("saidas"):
        os.makedirs("saidas")

    # Atualize para o nome correto da imagem colorida que você está usando
    nome_imagem = "Imagem3.png"
    img = cv.imread(nome_imagem)
    
    # Guarda de falha de leitura
    if img is None:
        print(f"Erro: Não foi possível ler a imagem '{nome_imagem}'. Verifique o caminho.")
        return

    inspecao_imagem(img)
    criar_copia(img)
    separar_canais(img)
    
    # Recebemos a imagem em cinza da função para ser quantizada
    img_gray = niveis_cinza(img) 
    quantizacao(img_gray)
    
    print("Processamento concluído com sucesso! Verifique a pasta 'saidas/'.")

if __name__ == "__main__":
    main()