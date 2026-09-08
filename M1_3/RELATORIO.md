
---

# M1.3 — `RELATORIO.md`

```md
# Mini Relatório — Laboratório M1.3

## Identificação

**Aluno:** Gustavo Odilon da Costa  
**Matrícula:** PREENCHER  
**Laboratório:** M1.3 — Convolução e filtragem espacial

## 1. Objetivo

O objetivo foi implementar operações de vizinhança e convolução espacial manualmente, analisando o efeito de kernels, tratamento de bordas, suavização e detecção de bordas.

## 2. Operações implementadas

Foram implementadas:

- convolução genérica;
- estratégia de borda copiar;
- estratégia de borda replicar;
- filtro de média 3x3;
- filtro de média ponderada 3x3;
- filtro de média 5x5;
- Laplaciano;
- realce utilizando a resposta Laplaciana;
- Sobel Gx;
- Sobel Gy;
- magnitude aproximada |Gx| + |Gy|;
- magnitude euclidiana.

## 3. Kernels utilizados

### Média 3x3

```text
1 1 1
1 1 1
1 1 1