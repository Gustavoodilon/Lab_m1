
---

# M1.1 — `RELATORIO.md`

```md
# Mini Relatório — Laboratório M1.1

## Identificação

**Aluno:** Gustavo Odilon da Costa  
**Laboratório:** M1.1 — Representação, canais e níveis de cinza

## 1. Objetivo

O objetivo do laboratório foi implementar operações fundamentais de representação de imagens digitais utilizando acesso direto aos pixels.

Foram trabalhados dimensões da imagem, canais de cor, níveis de cinza e resolução radiométrica.

## 2. Operações implementadas

Foram implementadas:

- inspeção da imagem;
- cópia manual dos pixels;
- separação dos canais B, G e R;
- conversão para cinza por média simples;
- conversão para cinza por média ponderada;
- quantização para 16, 8, 4 e 2 níveis.

Todas as operações principais foram realizadas através do percurso explícito dos pixels.

## 3. Decisões de implementação

As imagens são carregadas utilizando OpenCV.

As operações avaliadas foram implementadas manualmente, utilizando estruturas de repetição para percorrer cada pixel.

A ordem dos canais utilizada pelo OpenCV é BGR.

Na conversão ponderada foi utilizada a expressão:

g = 0,299R + 0,587G + 0,114B

## 4. Testes realizados

Foi utilizada uma imagem colorida principal e uma imagem pequena 2x2 para conferência manual.

Foram verificados:

- cópia exata dos pixels;
- separação dos canais;
- conversões para níveis de cinza;
- quantização em diferentes quantidades de níveis;
- comportamento em intensidades próximas de 0 e 255.

A execução apresentou sucesso nos testes realizados.

## 5. Resultados

A cópia manual produziu uma imagem idêntica à entrada.

A separação dos canais permitiu observar individualmente a contribuição dos canais azul, verde e vermelho.

As duas conversões para níveis de cinza produziram resultados diferentes.

Com a redução da quantidade de níveis na quantização, tornou-se progressivamente mais visível a perda de informação.

## 6. Análise técnica

### Qual é a diferença entre resolução espacial e resolução radiométrica?

A resolução espacial está relacionada à quantidade de pixels utilizados para representar uma imagem.

A resolução radiométrica representa a quantidade de níveis de intensidade que cada pixel pode assumir.

### Por que a média ponderada produz resultado diferente da média simples?

Na média simples, os canais vermelho, verde e azul possuem o mesmo peso.

Na média ponderada, cada canal possui uma contribuição diferente, considerando a sensibilidade visual humana. O canal verde possui maior influência no resultado.

### O que ocorre visualmente quando a quantidade de níveis é reduzida?

As transições de intensidade ficam menos suaves e aparecem regiões com tons mais uniformes.

Quanto menor a quantidade de níveis, maior a perda de detalhes.

### Em quais regiões a perda de informação fica mais evidente?

A perda é mais perceptível em regiões com transições suaves de intensidade, como sombras e gradientes.

### Como o tipo e o número de canais interferem no acesso a um pixel?

Em uma imagem em níveis de cinza, normalmente existe apenas um valor de intensidade por pixel.

Em uma imagem colorida existem vários valores por pixel, sendo necessário acessar individualmente os canais.

## 7. Limitações

A implementação foi desenvolvida considerando principalmente imagens de 8 bits e imagens com um ou três canais.

## 8. Uso de Inteligência Artificial

Foi utilizada a ferramenta ChatGPT como apoio durante o desenvolvimento do laboratório.

A ferramenta foi utilizada para:

- auxiliar na criação dos testes;
- revisar a documentação.

Foram realizadas modificações e testes durante o desenvolvimento para verificar os resultados obtidos.

## 9. Referências

- Material e enunciado do Laboratório M1.1 da disciplina de Processamento de Imagens.
- OpenCV.
- NumPy.