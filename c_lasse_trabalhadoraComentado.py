#!/usr/bin/env python3
import sys
import os
from sly import Lexer, Parser

# =====================================================================
#  ANALISADOR LÉXICO (LEXER)
# =====================================================================
# O Analisador Léxico é responsável por pegar o código fonte (texto puro)
# e dividi-lo em pequenas partes chamadas "tokens". Cada token representa
# um elemento da linguagem, como uma palavra-chave, um número, um
# identificador (nome de variável) ou um operador.
# =====================================================================
class AnalisadorLexico(Lexer):
    # Nomes dos tokens que serão gerados. O Parser usará esses nomes.
    tokens = {
        # Palavras Reservadas (Keywords)
        TIPO_INT, TIPO_FLOAT, TIPO_DOUBLE, TIPO_CHAR, TIPO_BOOL, TIPO_LONG,
        TIPO_SHORT, TIPO_UNSIGNED, TIPO_VOID, BOOL_TRUE, BOOL_FALSE,
        IF, ELSE, ELSEIF, WHILE, FOR, DO, SWITCH, CASE, BREAK, CONTINUE,
        PRINT, # Novo token para o comando de escrita
        
        # Identificadores e Literais
        ID, NUMERO, STRING, # Novo token para literais de texto
        
        # Operadores
        IGUAL, MAIS, MENOS, VEZES, DIVIDE,
        IGUAL_COMP, DIFERENTE, MENOR_Q, MAIOR_Q, MENOR_IGUAL, MAIOR_IGUAL,
    }

    # Caracteres que serão ignorados entre os tokens (espaço e tabulação)
    ignore = ' \t'
    
    # Ignora comentários no estilo C++
    ignore_comment = r'//.*'

    # Expressões regulares para tokens simples
    # Operadores de atribuição e comparação
    IGUAL_COMP = r'=='
    DIFERENTE = r'!='
    MENOR_IGUAL = r'<='
    MAIOR_IGUAL = r'>='
    IGUAL = r'='
    MENOR_Q = r'<'
    MAIOR_Q = r'>'
    
    # Operadores aritméticos e delimitadores
    MAIS = r'\+'
    MENOS = r'-'
    VEZES = r'\*'
    DIVIDE = r'/'
    
    # Delimitadores são tratados como literais de um caractere só
    literals = { '(', ')', '{', '}', ';', ':', ',' }

    # Regra para reconhecer literais de texto (strings)
    STRING = r'\"[^"]*\"'

    # Regra para identificar nomes de variáveis, funções, etc. (Identificadores)
    ID = r'[a-zA-Z_][a-zA-Z0-9_^]*'
    ID['formigaInteira'] = TIPO_INT
    ID['formigaFlutuante'] = TIPO_FLOAT
    ID['formigaFlutuante^2'] = TIPO_DOUBLE
    ID['formigaLetra'] = TIPO_CHAR
    ID['formigaSentinela'] = TIPO_BOOL
    ID['formigaAncia'] = TIPO_LONG
    ID['formigaLarva'] = TIPO_SHORT
    ID['operario'] = TIPO_UNSIGNED
    ID['tunelVazio'] = TIPO_VOID
    ID['vigia'] = BOOL_TRUE
    ID['descansa'] = BOOL_FALSE
    ID['seObstaculo'] = IF
    ID['senaoCavar'] = ELSE
    ID['senaoSeOutroObstaculo'] = ELSEIF
    ID['enquantoHouverComida'] = WHILE
    ID['marchar'] = FOR
    ID['cavarAteEnquanto'] = DO
    ID['inspecionarTunel'] = SWITCH
    ID['caminho'] = CASE
    ID['retornarAoNinho'] = BREAK
    ID['ignorarFolha'] = CONTINUE
    ID['sinalizar'] = PRINT # Nova palavra-chave

    # Regra para reconhecer números (inteiros ou de ponto flutuante)
    @_(r'\d+(\.\d+)?')
    def NUMERO(self, t):
        # Converte o valor do token para um número (float ou int)
        if '.' in t.value:
            t.value = float(t.value)
        else:
            t.value = int(t.value)
        return t

    # Regra para contar as linhas, útil para reportar erros
    @_(r'\n+')
    def newline(self, t):
        self.lineno += len(t.value)

    # Função para tratar erros léxicos (caracteres inesperados)
    def error(self, t):
        print(f"Erro Léxico: Caractere ilegal '{t.value[0]}' na linha {self.lineno}")
        self.index += 1

# =====================================================================
#  ANALISADOR SINTÁTICO (PARSER)
# =====================================================================
# O Analisador Sintático (ou Parser) recebe a lista de tokens do Lexer
# e verifica se eles formam uma estrutura válida de acordo com a "gramática"
# da linguagem. Ao mesmo tempo que verifica a sintaxe, ele também realiza
# a "tradução" para a linguagem C, construindo o código C parte por parte.
# =====================================================================
class GeradorCodigo(Parser):
    # Vincula o parser aos tokens definidos no lexer
    tokens = AnalisadorLexico.tokens

    def __init__(self):
        # Flag para garantir que a função 'natureza' existe no programa
        self.funcao_natureza_encontrada = False
        
        # Mapeamento de tokens para suas strings correspondentes em C
        self.mapeamento = {
            'formigaInteira': 'int', 'formigaFlutuante': 'float', 'formigaFlutuante^2': 'double',
            'formigaLetra': 'char', 'formigaSentinela': 'bool', 'formigaAncia': 'long',
            'formigaLarva': 'short', 'operario': 'unsigned', 'tunelVazio': 'void',
            'vigia': 'true', 'descansa': 'false', 'seObstaculo': 'if',
            'senaoCavar': 'else', 'senaoSeOutroObstaculo': 'else if',
            'enquantoHouverComida': 'while', 'marchar': 'for', 'cavarAteEnquanto': 'do',
            'inspecionarTunel': 'switch', 'caminho': 'case', 'retornarAoNinho': 'break',
            'ignorarFolha': 'continue',
        }

    # A partir daqui, definimos as regras da gramática.
    
    # Regra inicial: um programa é uma sequência de declarações.
    @_('declaracoes')
    def programa(self, p):
        # Ao final, verifica se a função 'natureza' foi definida
        if not self.funcao_natureza_encontrada:
            raise ValueError("ERRO: Função 'natureza()' não encontrada! Todo programa C-lasse Trabalhadora deve ter uma função 'natureza()'.")
        return p.declaracoes

    @_('declaracao declaracoes')
    def declaracoes(self, p):
        # Concatena a declaração atual com as próximas
        return p.declaracao + p.declaracoes

    @_('')
    def declaracoes(self, p):
        # Caso base: fim das declarações
        return ''

    # Uma declaração pode ser uma função ou uma variável global
    @_('declaracao_funcao')
    def declaracao(self, p):
        return p.declaracao_funcao

    # Regra para declarações de função
    @_('tipo ID "(" ")" "{" corpo "}"')
    def declaracao_funcao(self, p):
        nome_funcao = p.ID
        nome_traduzido = nome_funcao
        
        # Verifica se a função é 'natureza' e a traduz para 'main'
        if nome_funcao == 'natureza':
            self.funcao_natureza_encontrada = True
            nome_traduzido = 'main'
            
        return f'{p.tipo} {nome_traduzido}() {{\n{p.corpo}}}\n'

    # O corpo de uma função é uma sequência de instruções
    @_('instrucoes')
    def corpo(self, p):
        return p.instrucoes

    @_('instrucao instrucoes')
    def instrucoes(self, p):
        return p.instrucao + p.instrucoes

    @_('')
    def instrucoes(self, p):
        return ''

    # Uma instrução pode ser várias coisas
    @_('declaracao_variavel', 'atribuicao', 'estrutura_controle', 'break_stmt', 'continue_stmt', 'print_stmt')
    def instrucao(self, p):
        return p[0]

    # Regra para declaração de variável, com ou sem inicialização
    @_('tipo ID IGUAL expressao ";"',
       'tipo ID ";"')
    def declaracao_variavel(self, p):
        if len(p) == 5:
            return f'\t{p.tipo} {p.ID} = {p.expressao};\n'
        else:
            return f'\t{p.tipo} {p.ID};\n'

    # Regra para atribuição
    @_('ID IGUAL expressao ";"')
    def atribuicao(self, p):
        return f'\t{p.ID} = {p.expressao};\n'

    # Nova regra para o comando 'sinalizar' (print)
    @_('PRINT "(" print_arg ")" ";"')
    def print_stmt(self, p):
        argumento = p.print_arg
        # Se o argumento começar com aspas, é um texto literal
        if argumento.startswith('"'):
            # Adiciona um \n para quebrar a linha no console
            texto_formatado = argumento[:-1] + '\\n"'
            return f'\tprintf({texto_formatado});\n'
        # Caso contrário, é uma variável
        else:
            # Simplificação: assume que a variável é inteira (%d) ao imprimir
            return f'\tprintf("%d\\n", {argumento});\n'

    # Regra auxiliar para o argumento do 'sinalizar'
    @_('STRING', 'ID')
    def print_arg(self, p):
        return p[0]

    # Regra para 'retornarAoNinho' (break)
    @_('BREAK ";"')
    def break_stmt(self, p):
        return '\tbreak;\n'

    # Regra para 'ignorarFolha' (continue)
    @_('CONTINUE ";"')
    def continue_stmt(self, p):
        return '\tcontinue;\n'

    # Regra genérica para qualquer estrutura de controle
    @_('if_stmt', 'while_stmt', 'for_stmt', 'do_while_stmt', 'switch_stmt')
    def estrutura_controle(self, p):
        return p[0]
        
    # Regra para a estrutura 'seObstaculo' (if)
    @_('IF "(" expressao ")" "{" corpo "}" else_parte')
    def if_stmt(self, p):
        return f'\tif ({p.expressao}) {{\n{p.corpo}\t}}{p.else_parte}\n'

    # Regra para a parte 'senaoCavar' (else) ou 'senaoSeOutroObstaculo' (else if)
    @_('ELSE "{" corpo "}"')
    def else_parte(self, p):
        return f' else {{\n{p.corpo}\t}}'

    @_('ELSEIF "(" expressao ")" "{" corpo "}" else_parte')
    def else_parte(self, p):
        return f' else if ({p.expressao}) {{\n{p.corpo}\t}}{p.else_parte}'

    @_('')
    def else_parte(self, p):
        return ''

    # Regra para a estrutura 'enquantoHouverComida' (while)
    @_('WHILE "(" expressao ")" "{" corpo "}"')
    def while_stmt(self, p):
        return f'\twhile ({p.expressao}) {{\n{p.corpo}\t}}\n'
        
    # Regra para a estrutura 'marchar' (for)
    @_('FOR "(" for_inicializacao ";" expressao ";" atribuicao_sem_ponto_virgula ")" "{" corpo "}"')
    def for_stmt(self, p):
        return f'\tfor ({p.for_inicializacao}; {p.expressao}; {p.atribuicao_sem_ponto_virgula}) {{\n{p.corpo}\t}}\n'

    # Regra para a parte de inicialização de um loop for
    @_('declaracao_variavel_for', 'atribuicao_sem_ponto_virgula')
    def for_inicializacao(self, p):
        return p[0]

    # Regra para declaração de variável com atribuição (usada no for)
    @_('tipo ID IGUAL expressao')
    def declaracao_variavel_for(self, p):
        return f'{p.tipo} {p.ID} = {p.expressao}'

    # Regra para a estrutura 'cavarAteEnquanto' (do-while)
    @_('DO "{" corpo "}" WHILE "(" expressao ")" ";"')
    def do_while_stmt(self, p):
        return f'\tdo {{\n{p.corpo}\t}} while ({p.expressao});\n'

    # Regra para a estrutura 'inspecionarTunel' (switch)
    @_('SWITCH "(" expressao ")" "{" case_bloco "}"')
    def switch_stmt(self, p):
        return f'\tswitch ({p.expressao}) {{\n{p.case_bloco}\t}}\n'

    # Regra para o bloco de casos dentro de um switch
    @_('case_declaracao case_bloco')
    def case_bloco(self, p):
        return p.case_declaracao + p.case_bloco

    @_('')
    def case_bloco(self, p):
        return ''

    # Regra para uma declaração 'caminho' (case) individual
    @_('CASE expressao ":" instrucoes')
    def case_declaracao(self, p):
        return f'\t\tcase {p.expressao}:\n{p.instrucoes}'

    # Regra auxiliar para atribuições dentro de um for, que não levam ponto-e-vírgula
    @_('ID IGUAL expressao')
    def atribuicao_sem_ponto_virgula(self, p):
        return f'{p.ID} = {p.expressao}'

    # Regra para expressões (números, IDs, operações)
    @_('NUMERO', 'ID', 'BOOL_TRUE', 'BOOL_FALSE')
    def expressao(self, p):
        # Se for um token de palavra-chave (como 'vigia'), traduz.
        # Caso contrário, usa o valor direto (número ou nome de variável).
        return self.mapeamento.get(p[0], str(p[0]))

    # Regra para expressões com operadores binários
    @_('expressao MAIS expressao',
       'expressao MENOS expressao',
       'expressao VEZES expressao',
       'expressao DIVIDE expressao',
       'expressao IGUAL_COMP expressao',
       'expressao DIFERENTE expressao',
       'expressao MENOR_Q expressao',
       'expressao MAIOR_Q expressao',
       'expressao MENOR_IGUAL expressao',
       'expressao MAIOR_IGUAL expressao')
    def expressao(self, p):
        return f'{p.expressao0} {p[1]} {p.expressao1}'

    # Regra para expressão entre parênteses
    @_('"(" expressao ")"')
    def expressao(self, p):
        return f'({p.expressao})'

    # Regra para identificar os tipos da linguagem
    @_('TIPO_INT', 'TIPO_FLOAT', 'TIPO_DOUBLE', 'TIPO_CHAR', 'TIPO_BOOL',
       'TIPO_LONG', 'TIPO_SHORT', 'TIPO_UNSIGNED', 'TIPO_VOID')
    def tipo(self, p):
        return self.mapeamento[p[0]]
        
    # Função para tratar erros de sintaxe
    def error(self, p):
        if p:
            print(f"Erro de Sintaxe: Token inesperado '{p.value}' na linha {p.lineno}")
        else:
            print("Erro de Sintaxe: Fim inesperado do arquivo.")

# =====================================================
#  FUNÇÃO PRINCIPAL
# =====================================================
def main():
    if len(sys.argv) < 2:
        print("Uso: python c_lasse_trabalhadora.py <arquivo.formiga>")
        sys.exit(1)

    arquivo_entrada = sys.argv[1]
    if not os.path.exists(arquivo_entrada):
        print(f"Erro: Arquivo não encontrado: {arquivo_entrada}")
        sys.exit(1)

    # Lê o código fonte do arquivo de entrada
    with open(arquivo_entrada, "r", encoding="utf-8") as f:
        codigo_formiga = f.read()

    # Instancia as classes do compilador
    analisador_lexico = AnalisadorLexico()
    gerador_codigo = GeradorCodigo()

    try:
        # 1. Executa a análise léxica
        tokens = analisador_lexico.tokenize(codigo_formiga)
        
        # 2. Executa a análise sintática e geração de código
        codigo_c = gerador_codigo.parse(tokens)

        # 3. Gera o arquivo de saída .c
        arquivo_saida = arquivo_entrada.replace(".formiga", ".c")
        with open(arquivo_saida, "w", encoding="utf-8") as f:
            # Adiciona os includes necessários para o código C
            f.write("#include <stdio.h>\n")
            f.write("#include <stdbool.h>\n\n")
            f.write(codigo_c)

        print(f"Compilação concluída! Arquivo C gerado: {arquivo_saida}")

    except (ValueError, TypeError) as e:
        # Captura erros de sintaxe ou de natureza não encontrada
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()