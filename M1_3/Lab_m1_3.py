import cv2 as cv
import numpy as np
import os
import csv
import math
import sys


def clipe_valor(valor):
    """Garante que o valor fique no intervalo [0, 255]."""
    if valor < 0:
        return 0
    elif valor > 255:
        return 255
    return int(round(valor))


def carregar_imagem_cinza(caminho):
    """Carrega a imagem e converte para cinza somente como preparação."""
    img = cv.imread(caminho)

    if img is None:
        print(f"Erro: Falha na leitura da imagem '{caminho}'.")
        return None

    if len(img.shape) == 3:
        print("Imagem colorida detectada. Convertendo para níveis de cinza...")
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    return img


def validar_kernel(kernel, img):
    """Verifica se o kernel é quadrado, ímpar e compatível com a imagem."""
    if kernel is None or kernel.ndim != 2:
        raise ValueError("Kernel inválido.")

    linhas, colunas = kernel.shape

    if linhas == 0 or colunas == 0:
        raise ValueError("Kernel vazio.")

    if linhas != colunas:
        raise ValueError("O kernel deve ser quadrado.")

    if linhas % 2 == 0:
        raise ValueError("O kernel deve possuir dimensão ímpar.")

    if linhas > img.shape[0] or colunas > img.shape[1]:
        raise ValueError("O kernel não pode ser maior que a imagem.")


def convolucao(img, kernel, estrategia_borda="replicar", normalizar=False):
    """
    Convolução/correlação espacial manual.
    O kernel é aplicado na ordem em que foi informado, sem rotação.
    Estratégias de borda: 'copiar' e 'replicar'.
    """
    validar_kernel(kernel, img)

    if estrategia_borda not in ("copiar", "replicar"):
        raise ValueError("Estratégia de borda deve ser 'copiar' ou 'replicar'.")

    altura, largura = img.shape
    tamanho = kernel.shape[0]
    raio = tamanho // 2

    divisor = 1.0
    if normalizar:
        divisor = 0.0
        for ki in range(tamanho):
            for kj in range(tamanho):
                divisor += float(kernel[ki, kj])

        if abs(divisor) < 1e-12:
            raise ValueError("Não é possível normalizar um kernel cuja soma é zero.")

    resultado = np.zeros((altura, largura), dtype=np.float64)

    for i in range(altura):
        for j in range(largura):

            if estrategia_borda == "copiar":
                if i - raio < 0 or i + raio >= altura or j - raio < 0 or j + raio >= largura:
                    resultado[i, j] = float(img[i, j])
                    continue

            acumulador = 0.0

            for ki in range(tamanho):
                for kj in range(tamanho):
                    linha_img = i + ki - raio
                    coluna_img = j + kj - raio

                    if estrategia_borda == "replicar":
                        if linha_img < 0:
                            linha_img = 0
                        elif linha_img >= altura:
                            linha_img = altura - 1

                        if coluna_img < 0:
                            coluna_img = 0
                        elif coluna_img >= largura:
                            coluna_img = largura - 1

                    acumulador += float(img[linha_img, coluna_img]) * float(kernel[ki, kj])

            resultado[i, j] = acumulador / divisor

    return resultado


def converter_para_uint8(matriz, usar_modulo=False):
    """Converte uma matriz numérica para imagem uint8 somente no final."""
    altura, largura = matriz.shape
    resultado = np.zeros((altura, largura), dtype=np.uint8)

    for i in range(altura):
        for j in range(largura):
            valor = float(matriz[i, j])

            if usar_modulo:
                valor = abs(valor)

            resultado[i, j] = clipe_valor(valor)

    return resultado


def normalizar_visualizacao(matriz):
    """Mapeia uma resposta assinada para [0,255] apenas para visualização."""
    minimo = float(np.min(matriz))
    maximo = float(np.max(matriz))

    altura, largura = matriz.shape
    resultado = np.zeros((altura, largura), dtype=np.uint8)

    if maximo == minimo:
        return resultado

    for i in range(altura):
        for j in range(largura):
            valor = (float(matriz[i, j]) - minimo) * 255.0 / (maximo - minimo)
            resultado[i, j] = clipe_valor(valor)

    return resultado


def filtro_media_3x3(img, estrategia_borda="replicar"):
    kernel = np.array([
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ], dtype=np.float64)

    bruto = convolucao(img, kernel, estrategia_borda, normalizar=True)
    return converter_para_uint8(bruto)


def filtro_media_ponderada_3x3(img, estrategia_borda="replicar"):
    kernel = np.array([
        [1, 2, 1],
        [2, 4, 2],
        [1, 2, 1]
    ], dtype=np.float64)

    bruto = convolucao(img, kernel, estrategia_borda, normalizar=True)
    return converter_para_uint8(bruto)


def filtro_media_5x5(img, estrategia_borda="replicar"):
    kernel = np.ones((5, 5), dtype=np.float64)

    bruto = convolucao(img, kernel, estrategia_borda, normalizar=True)
    return converter_para_uint8(bruto)


def aplicar_laplaciano(img, estrategia_borda="replicar"):
    kernel = np.array([
        [0, -1, 0],
        [-1, 4, -1],
        [0, -1, 0]
    ], dtype=np.float64)

    resposta_bruta = convolucao(img, kernel, estrategia_borda, normalizar=False)

    # Imagem apenas para visualizar a resposta assinada.
    visualizacao = normalizar_visualizacao(resposta_bruta)

    # Realce: imagem original + resposta Laplaciana.
    altura, largura = img.shape
    realce = np.zeros((altura, largura), dtype=np.uint8)

    for i in range(altura):
        for j in range(largura):
            valor = float(img[i, j]) + float(resposta_bruta[i, j])
            realce[i, j] = clipe_valor(valor)

    return resposta_bruta, visualizacao, realce


def aplicar_sobel(img, estrategia_borda="replicar"):
    kernel_gx = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ], dtype=np.float64)

    kernel_gy = np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1]
    ], dtype=np.float64)

    gx = convolucao(img, kernel_gx, estrategia_borda, normalizar=False)
    gy = convolucao(img, kernel_gy, estrategia_borda, normalizar=False)

    altura, largura = img.shape
    magnitude_aproximada = np.zeros((altura, largura), dtype=np.float64)
    magnitude_euclidiana = np.zeros((altura, largura), dtype=np.float64)

    for i in range(altura):
        for j in range(largura):
            valor_gx = float(gx[i, j])
            valor_gy = float(gy[i, j])

            magnitude_aproximada[i, j] = abs(valor_gx) + abs(valor_gy)
            magnitude_euclidiana[i, j] = math.sqrt(valor_gx ** 2 + valor_gy ** 2)

    gx_visual = normalizar_visualizacao(gx)
    gy_visual = normalizar_visualizacao(gy)
    aproximada_visual = converter_para_uint8(magnitude_aproximada)
    euclidiana_visual = converter_para_uint8(magnitude_euclidiana)

    return gx_visual, gy_visual, aproximada_visual, euclidiana_visual


def salvar_csv(matriz, caminho):
    """Salva a resposta numérica bruta, incluindo valores negativos."""
    with open(caminho, mode="w", newline="") as arquivo:
        escritor = csv.writer(arquivo)

        for linha in matriz:
            escritor.writerow([f"{float(valor):.6f}" for valor in linha])


def executar_testes_minimos():
    """
    Testes mínimos pedidos no M1.3:
    identidade, constante, impulso, degrau vertical, degrau horizontal,
    formas tocando bordas, kernel 3x3 e kernel 5x5.
    """
    pasta = os.path.join("saidas", "testes")
    os.makedirs(pasta, exist_ok=True)

    kernel_identidade = np.array([
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ], dtype=np.float64)

    # Kernel identidade.
    imagem_identidade = np.array([
        [10, 20, 30, 40, 50],
        [60, 70, 80, 90, 100],
        [110, 120, 130, 140, 150],
        [160, 170, 180, 190, 200],
        [210, 220, 230, 240, 250]
    ], dtype=np.uint8)

    resultado_identidade = convolucao(
        imagem_identidade, kernel_identidade, "replicar", normalizar=False
    )
    cv.imwrite(
        os.path.join(pasta, "teste_identidade.png"),
        converter_para_uint8(resultado_identidade)
    )

    # Imagem constante.
    imagem_constante = np.full((33, 33), 128, dtype=np.uint8)
    cv.imwrite(
        os.path.join(pasta, "teste_constante_media3.png"),
        filtro_media_3x3(imagem_constante, "replicar")
    )

    # Imagem impulso.
    imagem_impulso = np.zeros((33, 33), dtype=np.uint8)
    imagem_impulso[16, 16] = 255
    cv.imwrite(
        os.path.join(pasta, "teste_impulso_media3.png"),
        filtro_media_3x3(imagem_impulso, "replicar")
    )

    # Degrau vertical.
    degrau_vertical = np.zeros((64, 64), dtype=np.uint8)
    degrau_vertical[:, 32:] = 255
    gx, _, _, _ = aplicar_sobel(degrau_vertical, "replicar")
    cv.imwrite(os.path.join(pasta, "teste_degrau_vertical_gx.png"), gx)

    # Degrau horizontal.
    degrau_horizontal = np.zeros((64, 64), dtype=np.uint8)
    degrau_horizontal[32:, :] = 255
    _, gy, _, _ = aplicar_sobel(degrau_horizontal, "replicar")
    cv.imwrite(os.path.join(pasta, "teste_degrau_horizontal_gy.png"), gy)

    # Formas simples tocando as bordas.
    formas_borda = np.zeros((64, 64), dtype=np.uint8)
    formas_borda[0:20, 0:20] = 255
    formas_borda[20:50, 50:64] = 180

    cv.imwrite(
        os.path.join(pasta, "teste_borda_copiar.png"),
        filtro_media_3x3(formas_borda, "copiar")
    )
    cv.imwrite(
        os.path.join(pasta, "teste_borda_replicar.png"),
        filtro_media_3x3(formas_borda, "replicar")
    )

    # Teste explícito com kernel 5x5.
    cv.imwrite(
        os.path.join(pasta, "teste_media5.png"),
        filtro_media_5x5(formas_borda, "replicar")
    )


def main():
    pasta_saida = "saidas"

    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    # Permite passar outra imagem sem alterar o código.
    # Ex.: python Lab_m1_3.py Imagem1.png
    nome_imagem = sys.argv[1] if len(sys.argv) > 1 else "Imagem3.png"

    img = carregar_imagem_cinza(nome_imagem)

    if img is None:
        return

    print("1. Aplicando filtros de suavização...")

    media3_copiar = filtro_media_3x3(img, "copiar")
    media3_replicar = filtro_media_3x3(img, "replicar")
    media_ponderada = filtro_media_ponderada_3x3(img, "replicar")
    media5 = filtro_media_5x5(img, "replicar")

    cv.imwrite(f"{pasta_saida}/media_3x3_copiar.png", media3_copiar)
    cv.imwrite(f"{pasta_saida}/media_3x3_replicar.png", media3_replicar)
    cv.imwrite(f"{pasta_saida}/media_ponderada_3x3.png", media_ponderada)
    cv.imwrite(f"{pasta_saida}/media_5x5.png", media5)

    print("2. Aplicando Laplaciano e realce...")

    laplaciano_bruto, laplaciano_visual, realce = aplicar_laplaciano(img, "replicar")

    cv.imwrite(f"{pasta_saida}/laplaciano.png", laplaciano_visual)
    cv.imwrite(f"{pasta_saida}/realce_laplaciano.png", realce)
    salvar_csv(laplaciano_bruto, f"{pasta_saida}/laplaciano_bruto.csv")

    print("3. Aplicando Sobel...")

    gx, gy, aproximada, euclidiana = aplicar_sobel(img, "replicar")

    cv.imwrite(f"{pasta_saida}/sobel_gx.png", gx)
    cv.imwrite(f"{pasta_saida}/sobel_gy.png", gy)
    cv.imwrite(f"{pasta_saida}/sobel_aproximado.png", aproximada)
    cv.imwrite(f"{pasta_saida}/sobel_euclidiano.png", euclidiana)

    print("4. Executando os testes mínimos...")
    executar_testes_minimos()

    print("Todas as operações obrigatórias do Laboratório M1.3 foram concluídas com sucesso!")


if __name__ == "__main__":
    main()
