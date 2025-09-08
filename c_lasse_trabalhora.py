#!/usr/bin/env python3
import sys
import os
from sly import Lexer, Parser

# =====================================================================
#  ANALISADOR LÉXICO (LEXER)
# =====================================================================
class AnalisadorLexico(Lexer):
    tokens = {
        TIPO_INT, TIPO_FLOAT, TIPO_DOUBLE, TIPO_CHAR, TIPO_BOOL, TIPO_LONG,
        TIPO_SHORT, TIPO_UNSIGNED, TIPO_VOID, BOOL_TRUE, BOOL_FALSE,
        IF, ELSE, ELSEIF, WHILE, FOR, DO, SWITCH, CASE, BREAK, CONTINUE,
        PRINT,
        ID, NUMERO, STRING,
        IGUAL, MAIS, MENOS, VEZES, DIVIDE,
        IGUAL_COMP, DIFERENTE, MENOR_Q, MAIOR_Q, MENOR_IGUAL, MAIOR_IGUAL,
    }

    ignore = ' \t'
    ignore_comment = r'//.*'

    IGUAL_COMP = r'=='
    DIFERENTE = r'!='
    MENOR_IGUAL = r'<='
    MAIOR_IGUAL = r'>='
    IGUAL = r'='
    MENOR_Q = r'<'
    MAIOR_Q = r'>'
    
    MAIS = r'\+'
    MENOS = r'-'
    VEZES = r'\*'
    DIVIDE = r'/'
    
    literals = { '(', ')', '{', '}', ';', ':', ',' }

    STRING = r'\"[^"]*\"'

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
    ID['sinalizar'] = PRINT

    @_(r'\d+(\.\d+)?')
    def NUMERO(self, t):
        if '.' in t.value:
            t.value = float(t.value)
        else:
            t.value = int(t.value)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print(f"Erro Léxico: Caractere ilegal '{t.value[0]}' na linha {self.lineno}")
        self.index += 1

# =====================================================================
#  ANALISADOR SINTÁTICO (PARSER)
# =====================================================================
class GeradorCodigo(Parser):
    tokens = AnalisadorLexico.tokens

    def __init__(self):
        self.funcao_natureza_encontrada = False
        self.mapeamento = {
            'formigaInteira': 'int',
            'formigaFlutuante': 'float', 
            'formigaFlutuante^2': 'double',
            'formigaLetra': 'char', 
            'formigaSentinela': 'bool', 
            'formigaAncia': 'long',
            'formigaLarva': 'short', 
            'operario': 'unsigned', 
            'tunelVazio': 'void',
            'vigia': 'true', 
            'descansa': 'false', 
            'seObstaculo': 'if',
            'senaoCavar': 'else', 
            'senaoSeOutroObstaculo': 'else if',
            'enquantoHouverComida': 'while', 
            'marchar': 'for', 
            'cavarAteEnquanto': 'do',
            'inspecionarTunel': 'switch', 
            'caminho': 'case', 
            'retornarAoNinho': 'break',
            'ignorarFolha': 'continue',
        }

    @_('declaracoes')
    def programa(self, p):
        if not self.funcao_natureza_encontrada:
            raise ValueError("ERRO: Função 'natureza()' não encontrada! Todo programa C-lasse Trabalhadora deve ter uma função 'natureza()'.")
        return p.declaracoes

    @_('declaracao declaracoes')
    def declaracoes(self, p):
        return p.declaracao + p.declaracoes

    @_('')
    def declaracoes(self, p):
        return ''

    @_('declaracao_funcao')
    def declaracao(self, p):
        return p.declaracao_funcao

    @_('tipo ID "(" ")" "{" corpo "}"')
    def declaracao_funcao(self, p):
        nome_funcao = p.ID
        nome_traduzido = nome_funcao
        
        if nome_funcao == 'natureza':
            self.funcao_natureza_encontrada = True
            nome_traduzido = 'main'
            
        return f'{p.tipo} {nome_traduzido}() {{\n{p.corpo}}}\n'

    @_('instrucoes')
    def corpo(self, p):
        return p.instrucoes

    @_('instrucao instrucoes')
    def instrucoes(self, p):
        return p.instrucao + p.instrucoes

    @_('')
    def instrucoes(self, p):
        return ''

    @_('declaracao_variavel', 'atribuicao', 'estrutura_controle', 'break_stmt', 'continue_stmt', 'print_stmt')
    def instrucao(self, p):
        return p[0]

    @_('tipo ID IGUAL expressao ";"',
       'tipo ID ";"')
    def declaracao_variavel(self, p):
        if len(p) == 5:
            return f'\t{p.tipo} {p.ID} = {p.expressao};\n'
        else:
            return f'\t{p.tipo} {p.ID};\n'

    @_('ID IGUAL expressao ";"')
    def atribuicao(self, p):
        return f'\t{p.ID} = {p.expressao};\n'

    @_('PRINT "(" print_arg ")" ";"')
    def print_stmt(self, p):
        argumento = p.print_arg
        if argumento.startswith('"'):
            texto_formatado = argumento[:-1] + '\\n"'
            return f'\tprintf({texto_formatado});\n'
        else:
            return f'\tprintf("%d\\n", {argumento});\n'

    @_('STRING', 'ID')
    def print_arg(self, p):
        return p[0]

    @_('BREAK ";"')
    def break_stmt(self, p):
        return '\tbreak;\n'

    @_('CONTINUE ";"')
    def continue_stmt(self, p):
        return '\tcontinue;\n'

    @_('if_stmt', 'while_stmt', 'for_stmt', 'do_while_stmt', 'switch_stmt')
    def estrutura_controle(self, p):
        return p[0]
        
    @_('IF "(" expressao ")" "{" corpo "}" else_parte')
    def if_stmt(self, p):
        return f'\tif ({p.expressao}) {{\n{p.corpo}\t}}{p.else_parte}\n'

    @_('ELSE "{" corpo "}"')
    def else_parte(self, p):
        return f' else {{\n{p.corpo}\t}}'

    @_('ELSEIF "(" expressao ")" "{" corpo "}" else_parte')
    def else_parte(self, p):
        return f' else if ({p.expressao}) {{\n{p.corpo}\t}}{p.else_parte}'

    @_('')
    def else_parte(self, p):
        return ''

    @_('WHILE "(" expressao ")" "{" corpo "}"')
    def while_stmt(self, p):
        return f'\twhile ({p.expressao}) {{\n{p.corpo}\t}}\n'
        
    @_('FOR "(" for_inicializacao ";" expressao ";" atribuicao_sem_ponto_virgula ")" "{" corpo "}"')
    def for_stmt(self, p):
        return f'\tfor ({p.for_inicializacao}; {p.expressao}; {p.atribuicao_sem_ponto_virgula}) {{\n{p.corpo}\t}}\n'

    @_('declaracao_variavel_for', 'atribuicao_sem_ponto_virgula')
    def for_inicializacao(self, p):
        return p[0]

    @_('tipo ID IGUAL expressao')
    def declaracao_variavel_for(self, p):
        return f'{p.tipo} {p.ID} = {p.expressao}'

    @_('DO "{" corpo "}" WHILE "(" expressao ")" ";"')
    def do_while_stmt(self, p):
        return f'\tdo {{\n{p.corpo}\t}} while ({p.expressao});\n'

    @_('SWITCH "(" expressao ")" "{" case_bloco "}"')
    def switch_stmt(self, p):
        return f'\tswitch ({p.expressao}) {{\n{p.case_bloco}\t}}\n'

    @_('case_declaracao case_bloco')
    def case_bloco(self, p):
        return p.case_declaracao + p.case_bloco

    @_('')
    def case_bloco(self, p):
        return ''

    @_('CASE expressao ":" instrucoes')
    def case_declaracao(self, p):
        return f'\t\tcase {p.expressao}:\n{p.instrucoes}'

    @_('ID IGUAL expressao')
    def atribuicao_sem_ponto_virgula(self, p):
        return f'{p.ID} = {p.expressao}'

    @_('NUMERO', 'ID', 'BOOL_TRUE', 'BOOL_FALSE')
    def expressao(self, p):
        return self.mapeamento.get(p[0], str(p[0]))

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

    @_('"(" expressao ")"')
    def expressao(self, p):
        return f'({p.expressao})'

    @_('TIPO_INT', 'TIPO_FLOAT', 'TIPO_DOUBLE', 'TIPO_CHAR', 'TIPO_BOOL',
       'TIPO_LONG', 'TIPO_SHORT', 'TIPO_UNSIGNED', 'TIPO_VOID')
    def tipo(self, p):
        return self.mapeamento[p[0]]
        
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

    with open(arquivo_entrada, "r", encoding="utf-8") as f:
        codigo_formiga = f.read()

    analisador_lexico = AnalisadorLexico()
    gerador_codigo = GeradorCodigo()

    try:
        tokens = analisador_lexico.tokenize(codigo_formiga)
        codigo_c = gerador_codigo.parse(tokens)

        arquivo_saida = arquivo_entrada.replace(".formiga", ".c")
        with open(arquivo_saida, "w", encoding="utf-8") as f:
            f.write("#include <stdio.h>\n")
            f.write("#include <stdbool.h>\n\n")
            f.write(codigo_c)

        print(f"Compilação concluída! Arquivo C gerado: {arquivo_saida}")

    except (ValueError, TypeError) as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()