import cv2 as cv
import numpy as np
import os
import sys


def carregar_imagem(caminho):
    """Carrega a imagem preservando a quantidade original de canais."""
    img = cv.imread(caminho, cv.IMREAD_UNCHANGED)

    if img is None:
        print(f"Erro: Falha na leitura da imagem '{caminho}'.")
        return None

    return img


def quantidade_canais(img):
    if len(img.shape) == 2:
        return 1
    return img.shape[2]


def inspecionar_imagem(img):
    """Inspeção manual das intensidades da imagem."""
    altura = img.shape[0]
    largura = img.shape[1]
    canais = quantidade_canais(img)
    quantidade_pixels = altura * largura

    print("\n--- INSPEÇÃO DA IMAGEM ---")
    print(f"Largura: {largura}")
    print(f"Altura: {altura}")
    print(f"Número de canais: {canais}")
    print(f"Tipo: {img.dtype}")
    print(f"Quantidade de pixels: {quantidade_pixels}")

    if canais == 1:
        minimo = 255
        maximo = 0
        soma = 0

        for i in range(altura):
            for j in range(largura):
                valor = int(img[i, j])

                if valor < minimo:
                    minimo = valor

                if valor > maximo:
                    maximo = valor

                soma += valor

        media = soma / quantidade_pixels

        print(f"Valor mínimo: {minimo}")
        print(f"Valor máximo: {maximo}")
        print(f"Média das intensidades: {media:.2f}")

    elif canais == 3:
        minimos = [255, 255, 255]
        maximos = [0, 0, 0]
        somas = [0, 0, 0]

        for i in range(altura):
            for j in range(largura):
                for canal in range(3):
                    valor = int(img[i, j, canal])

                    if valor < minimos[canal]:
                        minimos[canal] = valor

                    if valor > maximos[canal]:
                        maximos[canal] = valor

                    somas[canal] += valor

        nomes = ["Azul", "Verde", "Vermelho"]

        for canal in range(3):
            media = somas[canal] / quantidade_pixels
            print(
                f"{nomes[canal]} -> mínimo: {minimos[canal]}, "
                f"máximo: {maximos[canal]}, média: {media:.2f}"
            )

        minimo_global = min(minimos)
        maximo_global = max(maximos)
        media_global = sum(somas) / (quantidade_pixels * 3)

        print(f"Valor mínimo global: {minimo_global}")
        print(f"Valor máximo global: {maximo_global}")
        print(f"Média global das intensidades: {media_global:.2f}")

    else:
        print("Aviso: inspeção detalhada implementada para imagens de 1 ou 3 canais.")


def copiar_imagem_manual(img):
    """Cria uma cópia percorrendo todos os pixels manualmente."""
    altura = img.shape[0]
    largura = img.shape[1]
    canais = quantidade_canais(img)

    if canais == 1:
        copia = np.zeros((altura, largura), dtype=img.dtype)

        for i in range(altura):
            for j in range(largura):
                copia[i, j] = img[i, j]

    elif canais == 3:
        copia = np.zeros((altura, largura, 3), dtype=img.dtype)

        for i in range(altura):
            for j in range(largura):
                for canal in range(3):
                    copia[i, j, canal] = img[i, j, canal]

    else:
        raise ValueError("A cópia manual está preparada para imagens de 1 ou 3 canais.")

    return copia


def separar_canais_manual(img):
    """Separa B, G e R manualmente, preservando somente um canal por saída."""
    if quantidade_canais(img) != 3:
        raise ValueError("A separação de canais exige uma imagem colorida com 3 canais.")

    altura, largura, _ = img.shape

    canal_b = np.zeros((altura, largura, 3), dtype=np.uint8)
    canal_g = np.zeros((altura, largura, 3), dtype=np.uint8)
    canal_r = np.zeros((altura, largura, 3), dtype=np.uint8)

    for i in range(altura):
        for j in range(largura):
            b = int(img[i, j, 0])
            g = int(img[i, j, 1])
            r = int(img[i, j, 2])

            canal_b[i, j, 0] = b
            canal_g[i, j, 1] = g
            canal_r[i, j, 2] = r

    return canal_b, canal_g, canal_r


def cinza_media_simples(img):
    """Conversão manual para cinza usando (R + G + B) / 3."""
    if quantidade_canais(img) != 3:
        raise ValueError("A conversão para cinza exige uma imagem colorida com 3 canais.")

    altura, largura, _ = img.shape
    resultado = np.zeros((altura, largura), dtype=np.uint8)

    for i in range(altura):
        for j in range(largura):
            b = int(img[i, j, 0])
            g = int(img[i, j, 1])
            r = int(img[i, j, 2])

            valor = round((r + g + b) / 3)
            resultado[i, j] = valor

    return resultado


def cinza_media_ponderada(img):
    """Conversão manual usando 0,299R + 0,587G + 0,114B."""
    if quantidade_canais(img) != 3:
        raise ValueError("A conversão para cinza exige uma imagem colorida com 3 canais.")

    altura, largura, _ = img.shape
    resultado = np.zeros((altura, largura), dtype=np.uint8)

    for i in range(altura):
        for j in range(largura):
            b = int(img[i, j, 0])
            g = int(img[i, j, 1])
            r = int(img[i, j, 2])

            valor = round(0.299 * r + 0.587 * g + 0.114 * b)

            if valor < 0:
                valor = 0
            elif valor > 255:
                valor = 255

            resultado[i, j] = valor

    return resultado


def quantizar_manual(img_cinza, niveis):
    """Quantização uniforme manual para 16, 8, 4 ou 2 níveis."""
    if len(img_cinza.shape) != 2:
        raise ValueError("A quantização exige uma imagem em níveis de cinza.")

    if niveis not in (16, 8, 4, 2):
        raise ValueError("Quantidade de níveis inválida. Use 16, 8, 4 ou 2.")

    altura, largura = img_cinza.shape
    resultado = np.zeros((altura, largura), dtype=np.uint8)

    tamanho_faixa = 256.0 / niveis

    for i in range(altura):
        for j in range(largura):
            valor = int(img_cinza[i, j])

            indice = int(valor / tamanho_faixa)

            if indice >= niveis:
                indice = niveis - 1

            if niveis == 1:
                novo_valor = 0
            else:
                novo_valor = round(indice * 255 / (niveis - 1))

            if novo_valor < 0:
                novo_valor = 0
            elif novo_valor > 255:
                novo_valor = 255

            resultado[i, j] = novo_valor

    return resultado


def contar_niveis(img):
    """Conta manualmente quantos valores diferentes aparecem em uma imagem cinza."""
    presentes = [False] * 256
    altura, largura = img.shape

    for i in range(altura):
        for j in range(largura):
            presentes[int(img[i, j])] = True

    quantidade = 0

    for valor in presentes:
        if valor:
            quantidade += 1

    return quantidade


def executar_testes_minimos():
    """Executa os testes obrigatórios com casos pequenos e previsíveis."""
    pasta = os.path.join("saidas", "testes")
    os.makedirs(pasta, exist_ok=True)

    imagem_teste = carregar_imagem("Imagem3.png")

    if imagem_teste is None:
        print("Aviso: Imagem3.png não encontrada; testes com imagem 2x2 não foram executados.")
        return

    if quantidade_canais(imagem_teste) != 3:
        print("Aviso: Imagem3.png precisa possuir 3 canais para os testes.")
        return

    # 1. Cópia exata dos pixels.
    copia = copiar_imagem_manual(imagem_teste)

    if np.array_equal(imagem_teste, copia):
        print("Teste cópia manual: OK")
    else:
        print("Teste cópia manual: FALHOU")

    cv.imwrite(os.path.join(pasta, "teste_copia.png"), copia)

    # 2. Ordem dos canais.
    b, g, r = separar_canais_manual(imagem_teste)
    cv.imwrite(os.path.join(pasta, "teste_canal_b.png"), b)
    cv.imwrite(os.path.join(pasta, "teste_canal_g.png"), g)
    cv.imwrite(os.path.join(pasta, "teste_canal_r.png"), r)
    print("Teste separação de canais: saídas geradas")

    # 3. Duas versões em níveis de cinza.
    simples = cinza_media_simples(imagem_teste)
    ponderada = cinza_media_ponderada(imagem_teste)

    cv.imwrite(os.path.join(pasta, "teste_gray_average.png"), simples)
    cv.imwrite(os.path.join(pasta, "teste_gray_weighted.png"), ponderada)
    print("Teste conversões para cinza: saídas geradas")

    # 4 e 5. Quantidade de níveis e valores próximos aos limites.
    rampa = np.array([
        [0, 1, 15, 16, 31, 32, 63, 64],
        [95, 96, 127, 128, 191, 192, 254, 255]
    ], dtype=np.uint8)

    for niveis in (16, 8, 4, 2):
        quantizada = quantizar_manual(rampa, niveis)
        quantidade = contar_niveis(quantizada)

        cv.imwrite(
            os.path.join(pasta, f"teste_quant_{niveis}.png"),
            quantizada
        )

        if quantidade <= niveis:
            print(f"Teste quantização {niveis} níveis: OK ({quantidade} níveis presentes)")
        else:
            print(f"Teste quantização {niveis} níveis: FALHOU")


def main():
    pasta_saida = "saidas"
    os.makedirs(pasta_saida, exist_ok=True)

    # Permite trocar a imagem sem alterar o código:
    # python Lab_m1_1.py Imagem2.png
    nome_imagem = sys.argv[1] if len(sys.argv) > 1 else "Imagem1.png"

    img = carregar_imagem(nome_imagem)

    if img is None:
        return

    inspecionar_imagem(img)

    if quantidade_canais(img) != 3:
        print("\nErro: As operações principais do M1.1 exigem uma imagem colorida de 3 canais.")
        return

    print("\n1. Gerando cópia manual...")
    copia = copiar_imagem_manual(img)
    cv.imwrite(f"{pasta_saida}/copy.png", copia)

    print("2. Separando canais manualmente...")
    canal_b, canal_g, canal_r = separar_canais_manual(img)
    cv.imwrite(f"{pasta_saida}/channel_b.png", canal_b)
    cv.imwrite(f"{pasta_saida}/channel_g.png", canal_g)
    cv.imwrite(f"{pasta_saida}/channel_r.png", canal_r)

    print("3. Convertendo para níveis de cinza...")
    gray_average = cinza_media_simples(img)
    gray_weighted = cinza_media_ponderada(img)

    cv.imwrite(f"{pasta_saida}/gray_average.png", gray_average)
    cv.imwrite(f"{pasta_saida}/gray_weighted.png", gray_weighted)

    print("4. Quantizando a imagem em cinza ponderado...")

    for niveis in (16, 8, 4, 2):
        quantizada = quantizar_manual(gray_weighted, niveis)
        cv.imwrite(f"{pasta_saida}/quant_{niveis}.png", quantizada)

    print("5. Executando os testes mínimos...")
    executar_testes_minimos()

    print("\nTodas as operações obrigatórias do Laboratório M1.1 foram concluídas com sucesso!")


if __name__ == "__main__":
    main()
