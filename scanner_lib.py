import tab_simbolos_lib

ignora = [' ','\n', '\t']
simbolos = ['+','-','*','/',
              ',', '.', ';',
              '(', ')',
              '{', '}',
              '"',
              '_',
              '>', '<', '='
             ]
estados = {
    'inicio': {
        'digito': 'INTEIRO',        # feito
        '"': 'possivel_literal',    # feito
        'letra': 'ID',              # feito
        '{': 'possivel_comentario', # feito
        '$': 'EOF',                 # feito. Fim do arquivo precisa do $?
        '<': 'OPR_menor',           # feito
        '>': 'OPR_maior',           # feito
        '=': 'OPR_atribuicao',      # feito
        '+': 'OPM',                 # feito
        '-': 'OPM',                 # feito
        '*': 'OPM',                 # feito
        '/': 'OPM',                 # feito
        '(': 'AB_P',                # feito
        ')': 'FC_P',                # feito
        ',': 'VIR',                 # feito
        ';': 'PT_V',                # feito
        'ignora': 'inicio'          # feito
    },
    'INTEIRO': {
        'digito': 'INTEIRO',
        'Ee': 'possivel_exponencial',
        '.': 'possivel_real'
    },
    'possivel_real': {
        'digito': 'REAL'
    },
    'REAL': {
        'digito': 'REAL',
        'Ee': 'possivel_exponencial'
    },
    'possivel_exponencial': {
        'digito': 'REAL_final',
        '-': 'possivel_exponencial_com_sinal',
        '+': 'possivel_exponencial_com_sinal'
    },
    'possivel_exponencial_com_sinal': {
        'digito': 'REAL_final'
    },
    'REAL_final': {
        'digito': 'REAL_final'
    },
    'possivel_literal': {
        'letra': 'possivel_literal',
        'digito': 'possivel_literal',
        'outro': 'possivel_literal',
        'ignora': 'possivel_literal',
        '+': 'possivel_literal',
        '-': 'possivel_literal',
        '*': 'possivel_literal',
        '/': 'possivel_literal',
        ',': 'possivel_literal',
        '.': 'possivel_literal',
        ';': 'possivel_literal',
        '(': 'possivel_literal',
        ')': 'possivel_literal',
        '{': 'possivel_literal',
        '}': 'possivel_literal',
        '_': 'possivel_literal',
        '>': 'possivel_literal',
        '<': 'possivel_literal',
        '=': 'possivel_literal',
        '"': 'LITERAL'
    },
    'ID': {
        'letra': 'ID',
        'digito': 'ID',
        '_': 'ID'
    },
    'possivel_comentario': {
        'letra': 'possivel_comentario',
        'digito': 'possivel_comentario',
        'outro': 'possivel_comentario',
        'ignora': 'possivel_comentario',
        '+': 'possivel_comentario',
        '-': 'possivel_comentario',
        '*': 'possivel_comentario',
        '/': 'possivel_comentario',
        ',': 'possivel_comentario',
        '.': 'possivel_comentario',
        ';': 'possivel_comentario',
        '(': 'possivel_comentario',
        ')': 'possivel_comentario',
        '"': 'possivel_comentario',
        '_': 'possivel_comentario',
        '>': 'possivel_comentario',
        '<': 'possivel_comentario',
        '=': 'possivel_comentario',
        '}': 'COMENTARIO'
    },
    'OPR_menor': {
        '-': 'RCB',
        '=': 'OPR_final',
        '>': 'OPR_final'
    },
    'OPR_maior': {
        '=': 'OPR_final'
    }
}

template_tokens = {
    'INTEIRO': {
        'classe': 'NUM',
        'tipo': 'inteiro'
    },
    'REAL': {
        'classe': 'NUM',
        'tipo': 'real'
    },
    'REAL_final': {
        'classe': 'NUM',
        'tipo': 'real'
    },
    'LITERAL': {
        'classe': 'LIT',
        'tipo': 'literal'
    },
    'ID': {
        'classe': 'ID',
        'tipo': 'NULO'
    },
    'ERRO': {
        'classe': 'ERRO',
        'tipo': 'NULO',
        'lexema': 'NULO'
    }
}

def eh_final(estado: str) -> bool:
    return any(char.isupper() for char  in estado)

def pega_tipo(char: str):
    if len(char) > 1: 
        raise Exception(f'Caracter possui tamanho {len(char)}.')
    if (char.isalpha()):
        return "letra"
    if(char.isnumeric()):
        return "digito"
    if(char in ignora):
        return "ignora"
    if(char in simbolos):
        return char
    return "outro"

def pega_estado(estado_atual, nova_entrada): 
    # print(f"DEBUG - Atual: {estado_atual} | Entrada: {nova_entrada}")
    if not (estado_atual in estados) and eh_final(estado_atual):
        return None
    if nova_entrada in estados[estado_atual]:
        return estados[estado_atual][nova_entrada]
    else:
        if (eh_final(estado_atual)):
            return None
        else:
            return 'ERRO'

def formata_estado(estado: str) -> str:
    underline_index = estado.find('_')
    if underline_index >= 0:
        return estado[:underline_index] if estado[underline_index + 1].islower() else estado
    else:
        return estado

def scanner(estado: str, lexema: str, linha: int, coluna: int) -> dict:
    if not estado in template_tokens:
        token = {
            'classe': estado,
            'tipo': 'NULO',
            'lexema': lexema
        }
        tab_simbolos_lib.inserir(token)
        return token
    else:
        if estado == 'ID':
            resultado_busca = tab_simbolos_lib.buscar(lexema)
            if resultado_busca:
                return resultado_busca
        elif estado == 'ERRO':
            lexema = 'NULO'
            print((f"Caractere inválido na linguagem, linha {linha}, coluna {coluna}"))
        token = template_tokens[estado]
        token['lexema'] = lexema
        tab_simbolos_lib.inserir(token)
        return token