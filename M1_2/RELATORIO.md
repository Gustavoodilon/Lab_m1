
---

# M1.2 — `RELATORIO.md`

```md
# Mini Relatório — Laboratório M1.2

## Identificação

**Aluno:** Gustavo Odilon da Costa  
**Matrícula:** PREENCHER  
**Laboratório:** M1.2 — Transformações de intensidade

## 1. Objetivo

O objetivo foi implementar transformações pontuais em imagens em níveis de cinza e observar as alterações produzidas nos valores dos pixels e nos histogramas.

## 2. Operações implementadas

Foram implementados:

- brilho com b negativo;
- brilho com b positivo;
- contraste com α = 0,5;
- contraste com α = 1,0;
- contraste com α = 1,5;
- negativo;
- limiarização com dois valores diferentes;
- cálculo manual do histograma.

## 3. Decisões de implementação

Cada transformação percorre individualmente os pixels da imagem.

Quando uma operação produz valores inferiores a 0 ou superiores a 255, é realizada saturação para manter o valor no intervalo válido.

O histograma utiliza uma estrutura com 256 posições, uma para cada intensidade possível.

## 4. Testes realizados

Foram testados valores positivos e negativos de brilho.

O contraste foi testado com os valores 0,5, 1,0 e 1,5.

Também foram utilizados dois valores distintos de limiar.

Foram gerados histogramas da imagem original e de imagens transformadas.

## 5. Resultados

O aumento do brilho deslocou as intensidades para valores maiores, enquanto a redução do brilho deslocou os valores para intensidades menores.

O contraste com α menor que 1 aproximou os valores da região central das intensidades.

O contraste com α maior que 1 aumentou a diferença entre regiões claras e escuras.

O negativo inverteu as intensidades.

A limiarização produziu uma imagem contendo apenas dois níveis.

## 6. Análise técnica

### Qual é a diferença entre alteração de brilho e alteração de contraste?

A alteração de brilho adiciona ou remove uma quantidade de intensidade de todos os pixels.

O contraste modifica a distância dos valores de intensidade em relação a um valor de referência.

### Em quais testes ocorreu saturação e qual foi seu efeito?

A saturação pode ocorrer nos ajustes de brilho e contraste quando o resultado ultrapassa 255 ou fica abaixo de 0.

Nesses casos, os valores são limitados para 255 ou 0.

### Como o histograma se deslocou após alterar o brilho?

Com brilho positivo, o histograma tende a deslocar-se para intensidades maiores.

Com brilho negativo, tende a deslocar-se para intensidades menores.

### Como a distribuição mudou ao alterar o contraste?

Com contraste reduzido, os valores ficam mais concentrados.

Com contraste ampliado, os valores ficam mais espalhados e podem atingir os extremos do intervalo.

### Que informação é perdida após a limiarização?

A limiarização elimina os níveis intermediários de intensidade.

Os pixels passam a representar apenas duas classes, normalmente preto e branco.

## 7. Limitações

As transformações foram implementadas para imagens em níveis de cinza com intensidades entre 0 e 255.

## 8. Uso de Inteligência Artificial

Foi utilizada a ferramenta ChatGPT como apoio durante o desenvolvimento do laboratório.

A ferramenta foi utilizada para:

- auxiliar na criação dos testes;
- revisar a documentação.

## 9. Referências

- Material e enunciado do Laboratório M1.2.
- OpenCV.
- NumPy.