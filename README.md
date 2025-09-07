# Compilador C-lasse Trabalhadora 🐜

Este projeto é um compilador que traduz uma linguagem de programação temática, a **C-lasse Trabalhadora**, para a linguagem C padrão. A C-lasse Trabalhadora foi criada com o objetivo de ser didática e divertida, utilizando uma analogia com o universo das formigas para representar conceitos de programação.

Todas as palavras-chave, tipos de dados e estruturas de controle são em português e seguem a temática, facilitando a compreensão para programadores iniciantes.

## A Filosofia da Linguagem

A C-lasse Trabalhadora enxerga o código como uma colônia de formigas. Cada variável é uma formiga com uma função específica, as funções são túneis que levam a outras partes do formigueiro, e as estruturas de controle são as ordens e decisões tomadas durante a marcha diária em busca de comida (dados).

O objetivo é organizar o "formigueiro" (o código) de maneira clara e eficiente, onde cada "formiga" (variável) executa sua tarefa de forma disciplinada.

## Como Usar o Compilador

### Instalação e Execução

1. Certifique-se de ter Python 3 instalado em seu sistema
2. Faça o download do script `c-lasseT.py`
3. Torne o script executável (no Linux/Mac):
   ```bash
   chmod +x c-lasseT.py
   ```

### Estrutura de Arquivos

O compilador trabalha com arquivos que tenham a extensão `.formiga`. Por exemplo:
- `exemplo.formiga` (seu código em C-lasse Trabalhadora)
- `exemplo.c` (arquivo C gerado automaticamente)

### Executando o Compilador

```bash
python c-lasseT.py arquivo.formiga
```

ou, se o script estiver marcado como executável:

```bash
./c-lasseT.py arquivo.formiga
```

### Comportamento do Compilador

O compilador realiza as seguintes operações automaticamente:

1. **Leitura**: Lê o arquivo `.formiga` especificado
2. **Tradução**: Converte todas as palavras-chave da C-lasse Trabalhadora para C padrão
3. **Geração**: Cria um arquivo `.c` com o mesmo nome do arquivo original
4. **Headers**: Adiciona automaticamente os includes necessários (`#include <stdio.h>` e `#include <stdbool.h>`)
5. **Estrutura**: Envolve todo o código em uma função `main()` padrão de C
6. **Indentação**: Aplica indentação automática de 4 espaços para todo o código

### Exemplo Prático

**1. Crie um arquivo `colonia.formiga`:**
```formiga
formigaInteira natureza(){
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

**2. Execute o compilador:**
```bash
python c-lasseT.py colonia.formiga
```

**3. O compilador gerará automaticamente `colonia.c`:**
```c
#include <stdio.h>
#include <stdbool.h>

int main() {
    // Declaração de variáveis das formigas
    int numero_formigas = 42;
    float peso_carga = 3.14;
    bool tem_comida = true;
    
    // Estrutura condicional - se encontrar obstáculo
    if (numero_formigas > 0) {
        numero_formigas = numero_formigas + 1;
    } else {
        tem_comida = false;
    }
    
    // Loop enquanto houver comida
    while (numero_formigas < 100) {
        numero_formigas = numero_formigas * 2;
    }
    
    // Loop organizado (for)
    for (int i = 0; i < numero_formigas; i = i + 1) {
        peso_carga = peso_carga - 0.1;
    }
    return 0;
}
```

**4. Compile e execute o código C gerado:**
```bash
gcc colonia.c -o colonia
./colonia
```

## Mensagens do Compilador

- **Sucesso**: `Compilação concluída! Arquivo gerado: <nome>.c`
- **Erro de arquivo não encontrado**: `Arquivo não encontrado: <nome>`
- **Uso incorreto**: `Uso: python c-lasseT <arquivo.formiga>`

## Sintaxe e Palavras-Chave

### 1. Tipos de Dados (Tipos de Formigas)

Cada variável precisa ser declarada com um tipo, que define o tipo de "carga" que ela pode carregar.

| C-lasse Trabalhadora | Equivalente em C | Descrição |
|:---------------------|:-----------------|:----------|
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
```formiga
formigaInteira natureza() {
    // Declaração de formigas trabalhadoras (variáveis)
    formigaInteira numero_de_operarias = 150;
    formigaFlutuante tamanho_da_folha = 5.7;
    formigaSentinela rainha_presente = vigia;
}
```

### 2. Valores Booleanos (Estado da Sentinela)

A formiga `formigaSentinela` utiliza valores especiais para representar seus estados de vigília.

| C-lasse Trabalhadora | Equivalente em C |
|:---------------------|:-----------------|
| `vigia` | `true` |
| `descansa` | `false` |

**Exemplo:**
```formiga
formigaSentinela inimigo_a_vista = descansa;
```

### 3. Estruturas de Controle (Ordens da Colônia)

As estruturas de controle guiam o fluxo de execução do programa, como se fossem ordens para a colônia.

| C-lasse Trabalhadora | Equivalente em C | Descrição |
|:---------------------|:-----------------|:----------|
| `natureza` | `main` | Função principal do programa - onde toda a colônia opera. |
| `seObstaculo` | `if` | Executa um bloco de código se uma condição for verdadeira. |
| `senaoCavar` | `else` | Executa um bloco alternativo se a condição do `if` for falsa. |
| `senaoSeOutroObstaculo` | `else if` | Testa uma nova condição se a anterior for falsa. |
| `enquantoHouverComida` | `while` | Repete um bloco de código enquanto uma condição for verdadeira. |
| `marchar` | `for` | Repete um bloco de código um número definido de vezes. |
| `cavarAteEnquanto` | `do` | Executa um bloco de código uma vez e o repete enquanto a condição for verdadeira. |
| `inspecionarTunel` | `switch` | Seleciona um de vários blocos de código para ser executado. |
| `caminho` | `case` | Define um dos blocos de código para a estrutura `switch`. |
| `retornarAoNinho` | `break` | Interrompe a execução de um loop ou `switch`. |
| `ignorarFolha` | `continue` | Pula a iteração atual de um loop e vai para a próxima. |

## Limitações Atuais

- O compilador não realiza análise sintática avançada
- Não há verificação de tipos
- Não suporta funções customizadas (apenas tradução simples de palavras-chave)
- Não detecta erros de sintaxe no código original

## Estrutura do Projeto

```
projeto/
├── c-lasseT.py          # Compilador principal
├── exemplo.formiga      # Arquivo de exemplo
├── exemplo.c           # Arquivo C gerado (após compilação)
└── README.md           # Este arquivo
```

## Requisitos

- **Python 3.x** - Para executar o compilador
- **GCC** - Para compilar o código C gerado
  - Windows: MinGW-w64, MSYS2, ou Visual Studio Build Tools
  - Linux: Geralmente já instalado ou via package manager
  - Mac: Xcode Command Line Tools

## Compatibilidade

- ✅ Windows (com MinGW/MSYS2)
- ✅ Linux 
- ✅ macOS
- ✅ Qualquer sistema com Python 3 e GCC

## Contribuindo

Este projeto é educacional e está aberto a contribuições! Algumas ideias para melhorias:

- Implementar análise sintática completa
- Adicionar verificação de tipos
- Suporte a funções customizadas
- Melhor tratamento de erros
- Otimizações no código gerado

---

Feito com 🐜 para tornar a programação mais divertida e acessível!