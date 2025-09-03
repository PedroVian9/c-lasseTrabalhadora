# Compilador para a linguagem C-lasse Trabalhadora
# Traduz código da linguagem das formigas para C
# Todas as funções e variáveis em português para facilitar compreensão

import re
import sys
from dataclasses import dataclass
from typing import List, Dict, Optional, Union

class Token:
    """Classe que representa um token (unidade léxica) do código fonte"""
    def __init__(self, tipo: str, valor: str, linha: int, coluna: int):
        self.tipo = tipo
        self.valor = valor
        self.linha = linha
        self.coluna = coluna
    
    def __repr__(self):
        return f"Token({self.tipo}, {self.valor}, {self.linha}:{self.coluna})"

class AnalisadorLexico:
    """Analisador léxico - quebra o código fonte em tokens"""
    
    def __init__(self, texto: str):
        self.texto = texto
        self.posicao = 0
        self.linha = 1
        self.coluna = 1
        
        # Mapeamento dos tipos da C-lasse Trabalhadora para C
        self.mapeamento_tipos = {
            'formigaInteira': 'int',
            'formigaFlutuante': 'float', 
            'formigaFlutuante^2': 'double',
            'formigaLetra': 'char',
            'formigaSentinela': 'bool',
            'tunelVazio': 'void',
            'formigaAncia': 'long',
            'formigaLarva': 'short',
            'operario': 'unsigned'
        }
        
        # Mapeamento das estruturas de controle
        self.mapeamento_controle = {
            'seObstaculo': 'if',
            'senaoCavar': 'else',
            'senaoSeOutroObstaculo': 'else if',
            'marchar': 'for',
            'enquantoHouverComida': 'while',
            'cavarAteEnquanto': 'do',
            'inspecionarTunel': 'switch',
            'caminho': 'case',
            'retornarAoNinho': 'break',
            'ignorarFolha': 'continue'
        }
        
        # Valores booleanos especiais das formigas
        self.mapeamento_booleanos = {
            'vigia': 'true',
            'descansa': 'false'
        }
        
        # Padrões de tokens usando expressões regulares
        self.padroes_tokens = [
            ('COMENTARIO', r'//.*'),                          # Comentário de linha
            ('COMENTARIO_MULTIPLO', r'/\*.*?\*/'),           # Comentário de bloco
            ('NUMERO', r'\d+\.?\d*'),                        # Números inteiros e decimais
            ('STRING', r'"[^"]*"'),                          # Strings entre aspas
            ('CHAR', r"'[^']'"),                            # Caracteres entre aspas simples
            ('IDENTIFICADOR', r'[a-zA-Z_][a-zA-Z0-9_]*'),   # Nomes de variáveis e funções
            ('ATRIBUICAO', r'='),                           # Operador de atribuição
            ('SOMA', r'\+'),                                # Operador de soma
            ('SUBTRACAO', r'-'),                            # Operador de subtração
            ('MULTIPLICACAO', r'\*'),                       # Operador de multiplicação
            ('DIVISAO', r'/'),                              # Operador de divisão
            ('MODULO', r'%'),                               # Operador módulo
            ('IGUAL', r'=='),                               # Comparação de igualdade
            ('DIFERENTE', r'!='),                           # Comparação de diferença
            ('MENOR_IGUAL', r'<='),                         # Menor ou igual
            ('MAIOR_IGUAL', r'>='),                         # Maior ou igual
            ('MENOR', r'<'),                                # Menor que
            ('MAIOR', r'>'),                                # Maior que
            ('E_LOGICO', r'&&'),                           # E lógico
            ('OU_LOGICO', r'\|\|'),                        # Ou lógico
            ('NEGACAO', r'!'),                             # Negação lógica
            ('PONTO_VIRGULA', r';'),                       # Fim de declaração
            ('VIRGULA', r','),                             # Separador de parâmetros
            ('PAREN_ESQ', r'\('),                          # Parêntese esquerdo
            ('PAREN_DIR', r'\)'),                          # Parêntese direito
            ('CHAVE_ESQ', r'\{'),                          # Chave esquerda (início de bloco)
            ('CHAVE_DIR', r'\}'),                          # Chave direita (fim de bloco)
            ('COLCHETE_ESQ', r'\['),                       # Colchete esquerdo
            ('COLCHETE_DIR', r'\]'),                       # Colchete direito
            ('ESPACO_BRANCO', r'\s+'),                     # Espaços, tabs, quebras de linha
        ]
        
    def tokenizar(self) -> List[Token]:
        """Converte o texto fonte em uma lista de tokens"""
        tokens = []
        
        # Percorre todo o texto caractere por caractere
        while self.posicao < len(self.texto):
            encontrou_padrao = False
            
            # Testa cada padrão de token
            for tipo_token, padrao in self.padroes_tokens:
                regex = re.compile(padrao)
                correspondencia = regex.match(self.texto, self.posicao)
                
                if correspondencia:
                    valor = correspondencia.group(0)
                    
                    # Ignora espaços em branco e comentários (não gera tokens para eles)
                    if tipo_token in ['ESPACO_BRANCO', 'COMENTARIO', 'COMENTARIO_MULTIPLO']:
                        if tipo_token == 'ESPACO_BRANCO':
                            # Conta linhas e colunas para posicionamento correto dos erros
                            for char in valor:
                                if char == '\n':
                                    self.linha += 1
                                    self.coluna = 1
                                else:
                                    self.coluna += 1
                    else:
                        # Classifica o tipo do token baseado no seu valor
                        if tipo_token == 'IDENTIFICADOR':
                            if valor in self.mapeamento_tipos:
                                tipo_token = 'TIPO'
                            elif valor in self.mapeamento_controle:
                                tipo_token = 'CONTROLE'
                            elif valor in self.mapeamento_booleanos:
                                tipo_token = 'BOOLEANO'
                        
                        # Adiciona o token à lista
                        tokens.append(Token(tipo_token, valor, self.linha, self.coluna))
                        self.coluna += len(valor)
                    
                    # Avança a posição no texto
                    self.posicao = correspondencia.end()
                    encontrou_padrao = True
                    break
            
            # Se nenhum padrão corresponder, temos um caractere inválido
            if not encontrou_padrao:
                raise SyntaxError(f"Caractere inesperado '{self.texto[self.posicao]}' na linha {self.linha}, coluna {self.coluna}")
        
        return tokens

# Classes que representam os nós da Árvore Sintática Abstrata (AST)
class NoAST:
    """Classe base para todos os nós da árvore sintática"""
    pass

@dataclass
class Programa(NoAST):
    """Representa um programa completo"""
    declaracoes: List[NoAST]

@dataclass
class DeclaracaoVariavel(NoAST):
    """Representa a declaração de uma variável"""
    tipo: str
    nome: str
    valor_inicial: Optional[NoAST] = None

@dataclass
class DeclaracaoFuncao(NoAST):
    """Representa a declaração de uma função"""
    tipo_retorno: str
    nome: str
    parametros: List[DeclaracaoVariavel]
    corpo: List[NoAST]

@dataclass
class ComandoSe(NoAST):
    """Representa um comando condicional if"""
    condicao: NoAST
    bloco_se: List[NoAST]
    bloco_senao: Optional[List[NoAST]] = None

@dataclass
class ComandoEnquanto(NoAST):
    """Representa um loop while"""
    condicao: NoAST
    corpo: List[NoAST]

@dataclass
class ComandoPara(NoAST):
    """Representa um loop for"""
    inicializacao: Optional[NoAST]
    condicao: Optional[NoAST] 
    atualizacao: Optional[NoAST]
    corpo: List[NoAST]

@dataclass
class Atribuicao(NoAST):
    """Representa uma atribuição de valor a variável"""
    nome: str
    valor: NoAST

@dataclass
class OperacaoBinaria(NoAST):
    """Representa uma operação com dois operandos (ex: a + b)"""
    esquerda: NoAST
    operador: str
    direita: NoAST

@dataclass
class OperacaoUnaria(NoAST):
    """Representa uma operação com um operando (ex: -a, !b)"""
    operador: str
    operando: NoAST

@dataclass
class Identificador(NoAST):
    """Representa um identificador (nome de variável ou função)"""
    nome: str

@dataclass
class Literal(NoAST):
    """Representa um valor literal (número, string, booleano)"""
    valor: Union[int, float, str, bool]
    tipo: str

class AnalisadorSintatico:
    """Analisador sintático - constrói a árvore sintática abstrata"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.posicao = 0
        
    def token_atual(self) -> Optional[Token]:
        """Retorna o token na posição atual, ou None se chegou ao fim"""
        if self.posicao < len(self.tokens):
            return self.tokens[self.posicao]
        return None
    
    def consumir_token(self, tipo_esperado: str = None) -> Token:
        """Consome o token atual e avança para o próximo"""
        token = self.token_atual()
        if token is None:
            raise SyntaxError("Fim inesperado do arquivo")
        
        if tipo_esperado and token.tipo != tipo_esperado:
            raise SyntaxError(f"Esperado {tipo_esperado}, encontrado {token.tipo} na linha {token.linha}")
        
        self.posicao += 1
        return token
    
    def analisar(self) -> Programa:
        """Analisa todos os tokens e constrói a AST do programa"""
        declaracoes = []
        
        # Processa todas as declarações até o fim do arquivo
        while self.token_atual():
            declaracao = self.analisar_declaracao()
            if declaracao:
                declaracoes.append(declaracao)
        
        return Programa(declaracoes)
    
    def analisar_declaracao(self) -> Optional[NoAST]:
        """Analisa uma declaração (variável, função, comando)"""
        token = self.token_atual()
        
        if not token:
            return None
            
        # Se começar com um tipo, pode ser variável ou função
        if token.tipo == 'TIPO':
            return self.analisar_variavel_ou_funcao()
        # Se começar com estrutura de controle
        elif token.tipo == 'CONTROLE':
            return self.analisar_estrutura_controle()
        # Se começar com identificador, provavelmente é atribuição
        elif token.tipo == 'IDENTIFICADOR':
            return self.analisar_atribuicao()
        else:
            # Token não reconhecido, pula para o próximo
            self.consumir_token()
            return None
    
    def analisar_variavel_ou_funcao(self) -> NoAST:
        """Decide se é declaração de variável ou função"""
        token_tipo = self.consumir_token('TIPO')
        token_nome = self.consumir_token('IDENTIFICADOR')
        
        # Se o próximo token é '(', então é uma função
        if self.token_atual() and self.token_atual().tipo == 'PAREN_ESQ':
            return self.analisar_funcao(token_tipo.valor, token_nome.valor)
        else:
            # Senão é uma variável
            return self.analisar_declaracao_variavel(token_tipo.valor, token_nome.valor)
    
    def analisar_declaracao_variavel(self, tipo: str, nome: str) -> DeclaracaoVariavel:
        """Analisa uma declaração de variável"""
        valor_inicial = None
        
        # Verifica se há inicialização
        if self.token_atual() and self.token_atual().tipo == 'ATRIBUICAO':
            self.consumir_token('ATRIBUICAO')
            valor_inicial = self.analisar_expressao()
        
        self.consumir_token('PONTO_VIRGULA')
        return DeclaracaoVariavel(tipo, nome, valor_inicial)
    
    def analisar_funcao(self, tipo_retorno: str, nome: str) -> DeclaracaoFuncao:
        """Analisa uma declaração de função"""
        self.consumir_token('PAREN_ESQ')
        parametros = []
        
        # Analisa os parâmetros da função
        while self.token_atual() and self.token_atual().tipo != 'PAREN_DIR':
            if self.token_atual().tipo == 'TIPO':
                tipo_param = self.consumir_token('TIPO').valor
                nome_param = self.consumir_token('IDENTIFICADOR').valor
                parametros.append(DeclaracaoVariavel(tipo_param, nome_param))
                
                # Se há vírgula, continua lendo parâmetros
                if self.token_atual() and self.token_atual().tipo == 'VIRGULA':
                    self.consumir_token('VIRGULA')
        
        self.consumir_token('PAREN_DIR')
        self.consumir_token('CHAVE_ESQ')
        
        # Analisa o corpo da função
        corpo = []
        while self.token_atual() and self.token_atual().tipo != 'CHAVE_DIR':
            declaracao = self.analisar_declaracao()
            if declaracao:
                corpo.append(declaracao)
        
        self.consumir_token('CHAVE_DIR')
        return DeclaracaoFuncao(tipo_retorno, nome, parametros, corpo)
    
    def analisar_estrutura_controle(self) -> NoAST:
        """Analisa estruturas de controle (if, while, for)"""
        token_controle = self.consumir_token('CONTROLE')
        
        if token_controle.valor == 'seObstaculo':
            return self.analisar_se()
        elif token_controle.valor == 'enquantoHouverComida':
            return self.analisar_enquanto()
        elif token_controle.valor == 'marchar':
            return self.analisar_para()
        
        return None
    
    def analisar_se(self) -> ComandoSe:
        """Analisa um comando if"""
        self.consumir_token('PAREN_ESQ')
        condicao = self.analisar_expressao()
        self.consumir_token('PAREN_DIR')
        self.consumir_token('CHAVE_ESQ')
        
        # Analisa o bloco do if
        bloco_se = []
        while self.token_atual() and self.token_atual().tipo != 'CHAVE_DIR':
            declaracao = self.analisar_declaracao()
            if declaracao:
                bloco_se.append(declaracao)
        
        self.consumir_token('CHAVE_DIR')
        
        # Verifica se há else
        bloco_senao = None
        if self.token_atual() and self.token_atual().valor == 'senaoCavar':
            self.consumir_token('CONTROLE')  # consome 'else'
            self.consumir_token('CHAVE_ESQ')
            
            bloco_senao = []
            while self.token_atual() and self.token_atual().tipo != 'CHAVE_DIR':
                declaracao = self.analisar_declaracao()
                if declaracao:
                    bloco_senao.append(declaracao)
            
            self.consumir_token('CHAVE_DIR')
        
        return ComandoSe(condicao, bloco_se, bloco_senao)
    
    def analisar_enquanto(self) -> ComandoEnquanto:
        """Analisa um comando while"""
        self.consumir_token('PAREN_ESQ')
        condicao = self.analisar_expressao()
        self.consumir_token('PAREN_DIR')
        self.consumir_token('CHAVE_ESQ')
        
        corpo = []
        while self.token_atual() and self.token_atual().tipo != 'CHAVE_DIR':
            declaracao = self.analisar_declaracao()
            if declaracao:
                corpo.append(declaracao)
        
        self.consumir_token('CHAVE_DIR')
        return ComandoEnquanto(condicao, corpo)
    
    def analisar_para(self) -> ComandoPara:
        """Analisa um comando for"""
        self.consumir_token('PAREN_ESQ')
        
        # Analisa inicialização (opcional)
        inicializacao = None
        if self.token_atual().tipo != 'PONTO_VIRGULA':
            inicializacao = self.analisar_expressao()
        self.consumir_token('PONTO_VIRGULA')
        
        # Analisa condição (opcional)
        condicao = None
        if self.token_atual().tipo != 'PONTO_VIRGULA':
            condicao = self.analisar_expressao()
        self.consumir_token('PONTO_VIRGULA')
        
        # Analisa atualização (opcional)
        atualizacao = None
        if self.token_atual().tipo != 'PAREN_DIR':
            atualizacao = self.analisar_expressao()
        
        self.consumir_token('PAREN_DIR')
        self.consumir_token('CHAVE_ESQ')
        
        corpo = []
        while self.token_atual() and self.token_atual().tipo != 'CHAVE_DIR':
            declaracao = self.analisar_declaracao()
            if declaracao:
                corpo.append(declaracao)
        
        self.consumir_token('CHAVE_DIR')
        return ComandoPara(inicializacao, condicao, atualizacao, corpo)
    
    def analisar_atribuicao(self) -> Atribuicao:
        """Analisa uma atribuição de valor"""
        nome = self.consumir_token('IDENTIFICADOR').valor
        self.consumir_token('ATRIBUICAO')
        valor = self.analisar_expressao()
        self.consumir_token('PONTO_VIRGULA')
        return Atribuicao(nome, valor)
    
    def analisar_expressao(self) -> NoAST:
        """Analisa uma expressão completa (ponto de entrada)"""
        return self.analisar_ou_logico()
    
    def analisar_ou_logico(self) -> NoAST:
        """Analisa operações OU lógico (||) - menor precedência"""
        esquerda = self.analisar_e_logico()
        
        while self.token_atual() and self.token_atual().tipo == 'OU_LOGICO':
            operador = self.consumir_token('OU_LOGICO').valor
            direita = self.analisar_e_logico()
            esquerda = OperacaoBinaria(esquerda, operador, direita)
        
        return esquerda
    
    def analisar_e_logico(self) -> NoAST:
        """Analisa operações E lógico (&&)"""
        esquerda = self.analisar_igualdade()
        
        while self.token_atual() and self.token_atual().tipo == 'E_LOGICO':
            operador = self.consumir_token('E_LOGICO').valor
            direita = self.analisar_igualdade()
            esquerda = OperacaoBinaria(esquerda, operador, direita)
        
        return esquerda
    
    def analisar_igualdade(self) -> NoAST:
        """Analisa operações de igualdade (==, !=)"""
        esquerda = self.analisar_relacional()
        
        while self.token_atual() and self.token_atual().tipo in ['IGUAL', 'DIFERENTE']:
            operador = self.consumir_token().valor
            direita = self.analisar_relacional()
            esquerda = OperacaoBinaria(esquerda, operador, direita)
        
        return esquerda
    
    def analisar_relacional(self) -> NoAST:
        """Analisa operações relacionais (<, >, <=, >=)"""
        esquerda = self.analisar_aditivo()
        
        while self.token_atual() and self.token_atual().tipo in ['MENOR', 'MAIOR', 'MENOR_IGUAL', 'MAIOR_IGUAL']:
            operador = self.consumir_token().valor
            direita = self.analisar_aditivo()
            esquerda = OperacaoBinaria(esquerda, operador, direita)
        
        return esquerda
    
    def analisar_aditivo(self) -> NoAST:
        """Analisa operações aditivas (+, -)"""
        esquerda = self.analisar_multiplicativo()
        
        while self.token_atual() and self.token_atual().tipo in ['SOMA', 'SUBTRACAO']:
            operador = self.consumir_token().valor
            direita = self.analisar_multiplicativo()
            esquerda = OperacaoBinaria(esquerda, operador, direita)
        
        return esquerda
    
    def analisar_multiplicativo(self) -> NoAST:
        """Analisa operações multiplicativas (*, /, %)"""
        esquerda = self.analisar_unario()
        
        while self.token_atual() and self.token_atual().tipo in ['MULTIPLICACAO', 'DIVISAO', 'MODULO']:
            operador = self.consumir_token().valor
            direita = self.analisar_unario()
            esquerda = OperacaoBinaria(esquerda, operador, direita)
        
        return esquerda
    
    def analisar_unario(self) -> NoAST:
        """Analisa operações unárias (+, -, !)"""
        if self.token_atual() and self.token_atual().tipo in ['SOMA', 'SUBTRACAO', 'NEGACAO']:
            operador = self.consumir_token().valor
            operando = self.analisar_unario()
            return OperacaoUnaria(operador, operando)
        
        return self.analisar_primario()
    
    def analisar_primario(self) -> NoAST:
        """Analisa expressões primárias (literais, identificadores, expressões parentizadas)"""
        token = self.token_atual()
        
        if not token:
            raise SyntaxError("Expressão esperada")
        
        # Números
        if token.tipo == 'NUMERO':
            self.consumir_token()
            if '.' in token.valor:
                return Literal(float(token.valor), 'float')
            else:
                return Literal(int(token.valor), 'int')
        
        # Strings
        elif token.tipo == 'STRING':
            self.consumir_token()
            return Literal(token.valor[1:-1], 'string')  # Remove aspas
        
        # Caracteres
        elif token.tipo == 'CHAR':
            self.consumir_token()
            return Literal(token.valor[1:-1], 'char')  # Remove aspas simples
        
        # Booleanos
        elif token.tipo == 'BOOLEANO':
            self.consumir_token()
            return Literal(token.valor == 'vigia', 'bool')
        
        # Identificadores (nomes de variáveis)
        elif token.tipo == 'IDENTIFICADOR':
            self.consumir_token()
            return Identificador(token.valor)
        
        # Expressões entre parênteses
        elif token.tipo == 'PAREN_ESQ':
            self.consumir_token('PAREN_ESQ')
            expressao = self.analisar_expressao()
            self.consumir_token('PAREN_DIR')
            return expressao
        
        else:
            raise SyntaxError(f"Token inesperado: {token.tipo} na linha {token.linha}")

class GeradorCodigo:
    """Gerador de código C a partir da AST"""
    
    def __init__(self):
        # Mapeamento dos tipos das formigas para tipos C
        self.mapeamento_tipos = {
            'formigaSaudavel': 'int',
            'formigaFlutuante': 'float', 
            'formigaCumprida': 'double',
            'formigaLetra': 'char',
            'formigaSentinela': 'bool',
            'tunelVazio': 'void',
            'formigaAncia': 'long',
            'formigaLarva': 'short',
            'operario': 'unsigned'
        }
        
        # Mapeamento das estruturas de controle
        self.mapeamento_controle = {
            'seObstaculo': 'if',
            'senaoCavar': 'else',
            'senaoSeOutroObstaculo': 'else if',
            'marchar': 'for',
            'enquantoHouverComida': 'while',
            'cavarAteEnquanto': 'do',
            'inspecionarTunel': 'switch',
            'caminho': 'case',
            'retornarAoNinho': 'break',
            'ignorarFolha': 'continue'
        }
        
        # Mapeamento dos valores booleanos
        self.mapeamento_booleanos = {
            'vigia': 'true',
            'descansa': 'false'
        }
        
    def gerar_codigo(self, programa: Programa) -> str:
        """Gera o código C completo a partir da AST"""
        linhas_codigo = []
        
        # Adiciona os headers necessários
        linhas_codigo.append('// Código C gerado pelo compilador C-lasse Trabalhadora')
        linhas_codigo.append('#include <stdio.h>')
        linhas_codigo.append('#include <stdbool.h>')
        linhas_codigo.append('')
        
        # Gera código para todas as declarações do programa
        for declaracao in programa.declaracoes:
            codigo_declaracao = self.gerar_declaracao(declaracao)
            if codigo_declaracao:
                linhas_codigo.append(codigo_declaracao)
        
        return '\n'.join(linhas_codigo)
    
    def gerar_declaracao(self, declaracao: NoAST) -> str:
        """Gera código para uma declaração específica"""
        if isinstance(declaracao, DeclaracaoVariavel):
            return self.gerar_declaracao_variavel(declaracao)
        elif isinstance(declaracao, DeclaracaoFuncao):
            return self.gerar_declaracao_funcao(declaracao)
        elif isinstance(declaracao, ComandoSe):
            return self.gerar_comando_se(declaracao)
        elif isinstance(declaracao, ComandoEnquanto):
            return self.gerar_comando_enquanto(declaracao)
        elif isinstance(declaracao, ComandoPara):
            return self.gerar_comando_para(declaracao)
        elif isinstance(declaracao, Atribuicao):
            return self.gerar_atribuicao(declaracao)
        else:
            return f"// Declaração não suportada: {type(declaracao).__name__}"
    
    def gerar_declaracao_variavel(self, declaracao: DeclaracaoVariavel) -> str:
        """Gera código para declaração de variável"""
        tipo_c = self.mapeamento_tipos.get(declaracao.tipo, declaracao.tipo)
        
        if declaracao.valor_inicial:
            valor = self.gerar_expressao(declaracao.valor_inicial)
            return f"{tipo_c} {declaracao.nome} = {valor};"
        else:
            return f"{tipo_c} {declaracao.nome};"
    
    def gerar_declaracao_funcao(self, declaracao: DeclaracaoFuncao) -> str:
        """Gera código para declaração de função"""
        tipo_retorno_c = self.mapeamento_tipos.get(declaracao.tipo_retorno, declaracao.tipo_retorno)
        
        # Gera lista de parâmetros
        parametros = []
        for parametro in declaracao.parametros:
            tipo_c = self.mapeamento_tipos.get(parametro.tipo, parametro.tipo)
            parametros.append(f"{tipo_c} {parametro.nome}")
        
        lista_parametros = ', '.join(parametros) if parametros else 'void'
        
        # Gera o cabeçalho da função
        linhas_codigo = [f"{tipo_retorno_c} {declaracao.nome}({lista_parametros}) {{"]
        
        # Gera o corpo da função
        for comando in declaracao.corpo:
            codigo_comando = self.gerar_declaracao(comando)
            if codigo_comando:
                # Adiciona indentação para comandos dentro da função
                linhas_indentadas = ['    ' + linha for linha in codigo_comando.split('\n') if linha.strip()]
                linhas_codigo.extend(linhas_indentadas)
        
        linhas_codigo.append("}")
        return '\n'.join(linhas_codigo)
    
    def gerar_comando_se(self, comando: ComandoSe) -> str:
        """Gera código para comando if/else"""
        condicao = self.gerar_expressao(comando.condicao)
        linhas_codigo = [f"if ({condicao}) {{"]
        
        # Gera bloco do if
        for comando_se in comando.bloco_se:
            codigo_comando = self.gerar_declaracao(comando_se)
            if codigo_comando:
                linhas_indentadas = ['    ' + linha for linha in codigo_comando.split('\n') if linha.strip()]
                linhas_codigo.extend(linhas_indentadas)
        
        linhas_codigo.append("}")
        
        # Gera bloco else se existir
        if comando.bloco_senao:
            linhas_codigo.append("else {")
            for comando_senao in comando.bloco_senao:
                codigo_comando = self.gerar_declaracao(comando_senao)
                if codigo_comando:
                    linhas_indentadas = ['    ' + linha for linha in codigo_comando.split('\n') if linha.strip()]
                    linhas_codigo.extend(linhas_indentadas)
            linhas_codigo.append("}")
        
        return '\n'.join(linhas_codigo)
    
    def gerar_comando_enquanto(self, comando: ComandoEnquanto) -> str:
        """Gera código para comando while"""
        condicao = self.gerar_expressao(comando.condicao)
        linhas_codigo = [f"while ({condicao}) {{"]
        
        # Gera corpo do while
        for comando_corpo in comando.corpo:
            codigo_comando = self.gerar_declaracao(comando_corpo)
            if codigo_comando:
                linhas_indentadas = ['    ' + linha for linha in codigo_comando.split('\n') if linha.strip()]
                linhas_codigo.extend(linhas_indentadas)
        
        linhas_codigo.append("}")
        return '\n'.join(linhas_codigo)
    
    def gerar_comando_para(self, comando: ComandoPara) -> str:
        """Gera código para comando for"""
        # Gera as três partes do for (init; condition; update)
        init_str = self.gerar_expressao(comando.inicializacao) if comando.inicializacao else ""
        condicao_str = self.gerar_expressao(comando.condicao) if comando.condicao else ""
        atualizacao_str = self.gerar_expressao(comando.atualizacao) if comando.atualizacao else ""
        
        linhas_codigo = [f"for ({init_str}; {condicao_str}; {atualizacao_str}) {{"]
        
        # Gera corpo do for
        for comando_corpo in comando.corpo:
            codigo_comando = self.gerar_declaracao(comando_corpo)
            if codigo_comando:
                linhas_indentadas = ['    ' + linha for linha in codigo_comando.split('\n') if linha.strip()]
                linhas_codigo.extend(linhas_indentadas)
        
        linhas_codigo.append("}")
        return '\n'.join(linhas_codigo)
    
    def gerar_atribuicao(self, atribuicao: Atribuicao) -> str:
        """Gera código para atribuição de valor"""
        valor = self.gerar_expressao(atribuicao.valor)
        return f"{atribuicao.nome} = {valor};"
    
    def gerar_expressao(self, expressao: NoAST) -> str:
        """Gera código para uma expressão"""
        if isinstance(expressao, OperacaoBinaria):
            esquerda = self.gerar_expressao(expressao.esquerda)
            direita = self.gerar_expressao(expressao.direita)
            return f"({esquerda} {expressao.operador} {direita})"
        
        elif isinstance(expressao, OperacaoUnaria):
            operando = self.gerar_expressao(expressao.operando)
            return f"({expressao.operador}{operando})"
        
        elif isinstance(expressao, Identificador):
            return expressao.nome
        
        elif isinstance(expressao, Literal):
            # Formata literais de acordo com o tipo
            if expressao.tipo == 'string':
                return f'"{expressao.valor}"'
            elif expressao.tipo == 'char':
                return f"'{expressao.valor}'"
            elif expressao.tipo == 'bool':
                return 'true' if expressao.valor else 'false'
            else:
                return str(expressao.valor)
        
        else:
            return f"/* Expressão não suportada: {type(expressao).__name__} */"

def compilar_classe_trabalhadora(codigo_fonte: str) -> str:
    """
    Função principal do compilador
    Recebe código na linguagem C-lasse Trabalhadora e retorna código C equivalente
    """
    try:
        # Fase 1: Análise Léxica - quebra o código fonte em tokens
        print("🐜 Iniciando análise léxica...")
        analisador_lexico = AnalisadorLexico(codigo_fonte)
        tokens = analisador_lexico.tokenizar()
        print(f"✅ Análise léxica concluída. {len(tokens)} tokens encontrados.")
        
        # Fase 2: Análise Sintática - constrói a árvore sintática abstrata
        print("🐜 Iniciando análise sintática...")
        analisador_sintatico = AnalisadorSintatico(tokens)
        arvore_sintatica = analisador_sintatico.analisar()
        print("✅ Análise sintática concluída. AST construída.")
        
        # Fase 3: Geração de Código - traduz a AST para código C
        print("🐜 Iniciando geração de código C...")
        gerador = GeradorCodigo()
        codigo_c = gerador.gerar_codigo(arvore_sintatica)
        print("✅ Geração de código concluída.")
        
        return codigo_c
        
    except SyntaxError as erro_sintaxe:
        return f"❌ Erro de sintaxe: {str(erro_sintaxe)}"
    except Exception as erro_geral:
        return f"❌ Erro de compilação: {str(erro_geral)}"

def demonstrar_compilador():
    """Função para demonstrar o funcionamento do compilador"""
    print("🐜🏗️ COMPILADOR C-LASSE TRABALHADORA 🏗️🐜")
    print("=" * 50)
    
    # Código exemplo na linguagem C-lasse Trabalhadora
    codigo_exemplo = """
    // Função principal da colônia
    formigaSaudavel principal() {
        // Declaração de variáveis das formigas
        formigaSaudavel numero_formigas = 42;
        formigaFlutuante peso_carga = 3.14;
        formigaSentinela tem_comida = vigia;
        
        // Estrutura condicional - se encontrar obstáculo
        seObstaculo (numero_formigas > 0) {
            numero_formigas = numero_formigas + 1;
            peso_carga = peso_carga * 2;
        } senaoCavar {
            numero_formigas = 0;
            tem_comida = descansa;
        }
        
        // Loop enquanto houver comida
        enquantoHouverComida (numero_formigas < 100) {
            numero_formigas = numero_formigas * 2;
            peso_carga = peso_carga + 1;
        }
        
        // Loop organizado (for)
        marchar (formigaSaudavel i = 0; i < numero_formigas; i = i + 1) {
            peso_carga = peso_carga - 0.1;
        }
    }
    
    // Função auxiliar para calcular força
    formigaFlutuante calcular_forca(formigaFlutuante peso, formigaSaudavel quantidade) {
        formigaFlutuante forca_total = peso * quantidade;
        retornar forca_total;
    }
    """
    
    print("📝 Código fonte (C-lasse Trabalhadora):")
    print("-" * 40)
    print(codigo_exemplo)
    
    print("\n🔄 Compilando...")
    print("-" * 40)
    
    # Compila o código
    codigo_c_gerado = compilar_classe_trabalhadora(codigo_exemplo)
    
    print("\n💻 Código C gerado:")
    print("-" * 40)
    print(codigo_c_gerado)

def executar_teste_unitario():
    """Executa testes básicos do compilador"""
    print("\n🧪 EXECUTANDO TESTES UNITÁRIOS")
    print("=" * 50)
    
    # Teste 1: Declaração simples de variável
    print("Teste 1: Declaração de variável")
    codigo_teste1 = "formigaSaudavel x = 10;"
    resultado1 = compilar_classe_trabalhadora(codigo_teste1)
    print("✅" if "int x = 10;" in resultado1 else "❌", "Declaração de variável")
    
    # Teste 2: Estrutura condicional
    print("Teste 2: Estrutura condicional")
    codigo_teste2 = """
    seObstaculo (x > 5) {
        x = x + 1;
    }
    """
    resultado2 = compilar_classe_trabalhadora(codigo_teste2)
    print("✅" if "if (x > 5)" in resultado2 else "❌", "Estrutura if")
    
    # Teste 3: Valores booleanos
    print("Teste 3: Valores booleanos")
    codigo_teste3 = "formigaSentinela ativo = vigia;"
    resultado3 = compilar_classe_trabalhadora(codigo_teste3)
    print("✅" if "bool ativo = true;" in resultado3 else "❌", "Valores booleanos")
    
    print("\n✅ Testes concluídos!")

# Função principal para execução do programa
if __name__ == "__main__":
    # Demonstra o funcionamento do compilador
    demonstrar_compilador()
    
    # Executa testes unitários básicos
    executar_teste_unitario()
    
    print("\n🎉 Compilador C-lasse Trabalhadora pronto para uso!")
    print("🐜 As formigas trabalhadoras estão prontas para construir código C!")