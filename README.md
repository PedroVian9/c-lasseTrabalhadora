# Compilador C-lasse Trabalhadora 🐜

Este projeto é um compilador que traduz uma linguagem de programação temática, a **C-lasse Trabalhadora**, para a linguagem C padrão. A C-lasse Trabalhadora foi criada com o objetivo de ser didática e divertida, utilizando uma analogia com o universo das formigas para representar conceitos de programação.

Todas as palavras-chave, tipos de dados e estruturas de controle são em português e seguem a temática, facilitando a compreensão para programadores iniciantes.

## A Filosofia da Linguagem

A C-lasse Trabalhadora enxerga o código como uma colônia de formigas. Cada variável é uma formiga com uma função específica, as funções são túneis que levam a outras partes do formigueiro, e as estruturas de controle são as ordens e decisões tomadas durante a marcha diária em busca de comida (dados).

O objetivo é organizar o "formigueiro" (o código) de maneira clara e eficiente, onde cada "formiga" (variável) executa sua tarefa de forma disciplinada.

## Sintaxe e Palavras-Chave

A linguagem busca manter uma sintaxe familiar à da linguagem C, substituindo as palavras-chave em inglês por termos temáticos em português.

### 1\. Tipos de Dados (Tipos de Formigas)

Cada variável precisa ser declarada com um tipo, que define o tipo de "carga" que ela pode carregar.

| C-lasse Trabalhadora | Equivalente em C | Descrição |
| :--- | :--- | :--- |
| `formigaInteira` | `int` | Para armazenar números inteiros. |
| `formigaFlutuante` | `float` | Para números de ponto flutuante de precisão simples. |
| `formigaFlutuante^2` | `double` | Para números de ponto flutuante de precisão dupla. |
| `formigaLetra` | `char` | Para armazenar um único caractere. |
| `formigaSentinela` | `bool` | Para valores lógicos (verdadeiro ou falso). |
| `formigaAncia` | `long` | Para números inteiros longos. |
| `formigaLarva` | `short` | Para números inteiros curtos. |
| `operario` | `unsigned` | Modificador para tipos inteiros, indicando ausência de sinal. |
| `tunelVazio` | `void` | Usado para indicar que uma função não retorna valor. |

**Exemplo de Declaração de Variáveis:**

```ant
// Declaração de formigas trabalhadoras (variáveis)
formigaInteira numero_de_operarias = 150;
formigaFlutuante tamanho_da_folha = 5.7;
formigaSentinela rainha_presente = vigia;
```

### 2\. Valores Booleanos (Estado da Sentinela)

A formiga `formigaSentinela` utiliza valores especiais para representar seus estados de vigília.

| C-lasse Trabalhadora | Equivalente em C |
| :--- | :--- |
| `vigia` | `true` |
| `descansa` | `false` |

**Exemplo:**

```ant
formigaSentinela inimigo_a_vista = descansa;
```

### 3\. Estruturas de Controle (Ordens da Colônia)

As estruturas de controle guiam o fluxo de execução do programa, como se fossem ordens para a colônia.

| C-lasse Trabalhadora | Equivalente em C | Descrição |
| :--- | :--- | :--- |
| `seObstaculo` | `if` | Executa um bloco de código se uma condição for verdadeira. |
| `senaoCavar` | `else` | Executa um bloco alternativo se a condição do `if` for falsa. |
| `senaoSeOutroObstaculo` | `else if` | Testa uma nova condição se a anterior for falsa. |
| `enquantoHouverComida` | `while` | Repete um bloco de código enquanto uma condição for verdadeira. |
| `marchar` | `for` | Repete um bloco de código um número definido de vezes. |
| `cavarAteEnquanto` | `do-while` | Executa um bloco de código uma vez e o repete enquanto a condição for verdadeira. |
| `inspecionarTunel` | `switch` | Seleciona um de vários blocos de código para ser executado. |
| `caminho` | `case` | Define um dos blocos de código para a estrutura `switch`. |
| `retornarAoNinho` | `break` | Interrompe a execução de um loop ou `switch`. |
| `ignorarFolha` | `continue` | Pula a iteração atual de um loop e vai para a próxima. |

**Exemplo de `if/else`:**

```ant
seObstaculo (tem_pedra_no_caminho == vigia) {
    // Tenta um caminho alternativo
    desviar_da_pedra();
} senaoCavar {
    // Segue em frente
    continuar_marcha();
}
```

**Exemplo de `while`:**

```ant
enquantoHouverComida (estoque_de_comida > 0) {
    trabalhar();
    estoque_de_comida = estoque_de_comida - 1;
}
```

**Exemplo de `for`:**

```ant
marchar (formigaInteira i = 0; i < 10; i = i + 1) {
    coletar_comida();
}
```

### 4\. Funções (Túneis do Formigueiro)

Funções são blocos de código reutilizáveis que realizam uma tarefa específica, como túneis que levam a diferentes câmaras do formigueiro.

A declaração de uma função segue o formato:
`tipo_retorno nome_funcao(parametros) { ... }`

**Exemplo de Função:**

```ant
// Função que calcula a carga total que um grupo de formigas pode carregar
formigaFlutuante calcular_carga_total(formigaInteira num_formigas, formigaFlutuante carga_individual) {
    formigaFlutuante carga_total = num_formigas * carga_individual;

    // A palavra 'retornar' ainda não foi implementada no compilador fornecido,
    // mas seria o equivalente a 'return'.
    // Ex: retornar carga_total;
}

// Função principal, o coração da colônia
formigaInteira principal() {
    formigaFlutuante resultado = calcular_carga_total(50, 2.5);
    // ... resto do código
}
```

## Exemplo Completo

Aqui está o código de demonstração que usa vários recursos da linguagem C-lasse Trabalhadora.

**Código em C-lasse Trabalhadora:**

```ant
// Função principal da colônia
formigaInteira principal() {
    // Declaração de variáveis das formigas
    formigaInteira numero_formigas = 42;
    formigaFlutuante peso_carga = 3.14;
    formigaSentinela tem_comida = vigia;
    
    // Estrutura condicional - se encontrar obstáculo
    seObstaculo (numero_formigas > 0) {
        numero_formigas = numero_formigas + 1;
    } senaoCavar {
        tem_comida = descansa;
    }
    
    // Loop enquanto houver comida
    enquantoHouverComida (numero_formigas < 100) {
        numero_formigas = numero_formigas * 2;
    }
    
    // Loop organizado (for)
    marchar (formigaInteira i = 0; i < numero_formigas; i = i + 1) {
        peso_carga = peso_carga - 0.1;
    }
}
```

**Código C Gerado:**

```c
// Código C gerado pelo compilador C-lasse Trabalhadora
#include <stdio.h>
#include <stdbool.h>

int main() {
    int numero_formigas = 42;
    float peso_carga = 3.14;
    bool tem_comida = true;
    
    if ((numero_formigas > 0)) {
        numero_formigas = (numero_formigas + 1);
    }
    else {
        tem_comida = false;
    }
    
    while ((numero_formigas < 100)) {
        numero_formigas = (numero_formigas * 2);
    }
    
    for (int i = 0; (i < numero_formigas); i = (i + 1)) {
        peso_carga = (peso_carga - 0.1);
    }
}
```

-----
