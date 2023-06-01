import scanner_lib, traceback

def print_token(token):
    # print(f"Classe: '{token['classe']}' | Lexema: '{token['lexema']}' | Tipo: '{token['tipo']}'")
    print(token)

def main(file_path='programa.p'):
    with open(file_path, 'r', encoding='utf-8') as file:
            linha = 1
            coluna = 0
            estado = 'inicio'
            lexema = ''
            for conteudo_linha in file:
                coluna = 1 
                for conteudo_coluna in conteudo_linha:
                    nova_entrada = scanner_lib.pega_tipo(estado, conteudo_coluna)
                    novo_estado = scanner_lib.pega_estado(estado, nova_entrada)
                    if not novo_estado:
                        token = scanner_lib.scanner(estado, lexema, linha, coluna)
                        print_token(token)
                        lexema = ''
                        novo_estado = scanner_lib.pega_estado('inicio', nova_entrada)
                    elif novo_estado == 'ERRO':
                        token = scanner_lib.scanner(novo_estado, lexema, linha, coluna)
                        lexema = ''
                        print_token(token)
                    estado = novo_estado
                    if estado != 'inicio' :
                        lexema += conteudo_coluna
                    if estado == 'ERRO':
                        estado = 'inicio'
                        lexema = ''
                    coluna+=1
                linha+=1
            if scanner_lib.eh_final(estado):
                token = scanner_lib.scanner(estado, lexema, linha, coluna)
                print_token(token)
            elif estado == 'inicio':
                pass
            else:
                token = scanner_lib.scanner('ERRO', 'EOF', linha, coluna)
                print_token(token)
            token = scanner_lib.scanner('EOF', 'EOF', linha, coluna)
            print_token(token)







try:
    main()
except Exception as erro:
    print(erro)
    traceback.print_exc()
