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
        'digito': 'INTEIRO',        
        '"': 'possivel_literal',    
        'letra': 'ID',              
        '{': 'possivel_comentario', 
        'EOF': 'EOF',
        '<': 'OPR_menor',           
        '>': 'OPR_maior',           
        '=': 'OPR_atribuicao',      
        '+': 'OPM',                 
        '-': 'OPM',                 
        '*': 'OPM',                 
        '/': 'OPM',                 
        '(': 'AB_P',                
        ')': 'FC_P',                
        ',': 'VIR',                 
        ';': 'PT_V',                
        'ignora': 'inicio'          
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

def pega_tipo(estado_atual: str, char: str):
    if (estado_atual == 'INTEIRO' or estado_atual == 'REAL') and (char == 'e' or char == 'E'):
        return 'Ee'
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
    estado = formata_estado(estado)
    if not estado in template_tokens:
        token = {
            'classe': estado,
            'tipo': 'NULO',
            'lexema': lexema
        }
        return token
    else:
        token = template_tokens[estado]
        token['lexema'] = lexema
        if estado == 'ID':
            resultado_busca = tab_simbolos_lib.buscar(lexema)
            if resultado_busca:
                print("achou")
                return resultado_busca
            else:
                tab_simbolos_lib.inserir(token)
        elif estado == 'ERRO':
            token['lexema'] = 'NULO'
            print((f"Caractere inválido na linguagem, linha {linha}, coluna {coluna}"))
        return token
        