import json

def ler_escrever_json(data: dict = None) -> dict:
    if data is None:
        with open("tabela_de_simbolos.json", 'r') as f:
            data = json.load(f)
    else:
        with open("tabela_de_simbolos.json", 'w') as f:
            json.dump(data, f, indent=4)
    return data

def buscar(lexema: str):
    tokens = ler_escrever_json()
    return next((item for item in tokens if item["lexema"] == lexema), None)

def inserir(token: dict):
    if not buscar(token['lexema']):
        tokens = ler_escrever_json()
        tokens.append(token)
        ler_escrever_json(tokens)
    else:
        atualizar(token)

def atualizar(token: dict):
    tokens = ler_escrever_json()
    token_antigo = buscar(token['lexema'])
    if token_antigo:
        tokens.remove(token_antigo)
        tokens.append(token)
        ler_escrever_json(tokens)
    else:
        raise Exception('Token não encontrado. Impossível atualizar.')