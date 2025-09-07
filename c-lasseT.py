#!/usr/bin/env python3
import sys
import os
import re

# =====================================================
#  ANÁLISE LÉXICA
# =====================================================
class AnalisadorLexico:
    def __init__(self):
        self.palavras_reservadas = {
            # Tipos
            'formigaInteira': 'TIPO_INT',
            'formigaFlutuante': 'TIPO_FLOAT',
            'formigaFlutuante^2': 'TIPO_DOUBLE',
            'formigaLetra': 'TIPO_CHAR',
            'formigaSentinela': 'TIPO_BOOL',
            'formigaAncia': 'TIPO_LONG',
            'formigaLarva': 'TIPO_SHORT',
            'operario': 'TIPO_UNSIGNED',
            'tunelVazio': 'TIPO_VOID',

            # Função principal
            'natureza': 'main',

            # Booleanos
            'vigia': 'BOOL_TRUE',
            'descansa': 'BOOL_FALSE',

            # Estruturas de controle
            'seObstaculo': 'IF',
            'senaoCavar': 'ELSE',
            'senaoSeOutroObstaculo': 'ELSEIF',
            'enquantoHouverComida': 'WHILE',
            'marchar': 'FOR',
            'cavarAteEnquanto': 'DO',
            'inspecionarTunel': 'SWITCH',
            'caminho': 'CASE',
            'retornarAoNinho': 'BREAK',
            'ignorarFolha': 'CONTINUE',
        }

# =====================================================
#  GERADOR DE CÓDIGO
# =====================================================
class GeradorCodigo:
    def __init__(self):
        self.mapeamento_tipos = {
            'formigaInteira': 'int',
            'formigaFlutuante': 'float',
            'formigaFlutuante^2': 'double',
            'formigaLetra': 'char',
            'formigaSentinela': 'bool',
            'formigaAncia': 'long',
            'formigaLarva': 'short',
            'operario': 'unsigned',
            'tunelVazio': 'void',
        }

        self.booleanos = {
            'vigia': 'true',
            'descansa': 'false'
        }

        self.controle_fluxo = {
            'seObstaculo': 'if',
            'senaoCavar': 'else',
            'senaoSeOutroObstaculo': 'else if',
            'enquantoHouverComida': 'while',
            'marchar': 'for',
            'cavarAteEnquanto': 'do',
            'inspecionarTunel': 'switch',
            'caminho': 'case',
            'retornarAoNinho': 'break',
            'ignorarFolha': 'continue'
        }

    def verificar_funcao_natureza(self, codigo_formiga: str) -> bool:
        """
        Verifica se existe a função natureza() no código
        Retorna True se encontrar, False caso contrário
        """
        # Padrão para encontrar a função natureza()
        # Aceita qualquer tipo de retorno antes de 'natureza'
        padrao = r'\w+\s+natureza\s*\(\s*\)\s*\{'
        
        return re.search(padrao, codigo_formiga, re.MULTILINE) is not None

    def traduzir(self, codigo_formiga: str) -> str:
        # Verifica se a função natureza() existe
        if not self.verificar_funcao_natureza(codigo_formiga):
            raise ValueError("ERRO: Função 'natureza()' não encontrada! Todo programa C-lasse Trabalhadora deve ter uma função 'natureza()'.")
        
        codigo_c = codigo_formiga
        
        # Troca 'natureza' por 'main' primeiro
        codigo_c = re.sub(r'\bnatureza\b', 'main', codigo_c)
        
        # Troca palavras reservadas
        for palavra, traducao in self.mapeamento_tipos.items():
            codigo_c = codigo_c.replace(palavra, traducao)
        for palavra, traducao in self.booleanos.items():
            codigo_c = codigo_c.replace(palavra, traducao)
        for palavra, traducao in self.controle_fluxo.items():
            codigo_c = codigo_c.replace(palavra, traducao)
        
        return codigo_c

# =====================================================
#  MAIN
# =====================================================
def main():
    if len(sys.argv) < 2:
        print("Uso: python c-lasseT.py <arquivo.formiga>")
        sys.exit(1)

    arquivo_entrada = sys.argv[1]
    if not os.path.exists(arquivo_entrada):
        print(f"Arquivo não encontrado: {arquivo_entrada}")
        sys.exit(1)

    # Lê o código formiga
    with open(arquivo_entrada, "r", encoding="utf-8") as f:
        codigo_formiga = f.read()

    try:
        # Traduz para C
        gerador = GeradorCodigo()
        codigo_c = gerador.traduzir(codigo_formiga)

        # Gera arquivo de saída
        arquivo_saida = arquivo_entrada.replace(".formiga", ".c")
        with open(arquivo_saida, "w", encoding="utf-8") as f:
            f.write("#include <stdio.h>\n#include <stdbool.h>\n\n")
            f.write(codigo_c)

        print(f"Compilação concluída! Arquivo gerado: {arquivo_saida}")
        
    except ValueError as e:
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()