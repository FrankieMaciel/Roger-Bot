from Project.vocab.normalize import normalizeString

def processLines(arquivo):
    linhas_array = []
    with open(arquivo, 'r') as file:
        linhas = file.readlines()

    for i in range(len(linhas) - 1):
        linha_atual = linhas[i].strip()
        proxima_linha = linhas[i + 1].strip()
        a1 = linha_atual.split(' ')[0] != ''
        a2 = proxima_linha.split(' ')[0] != ''
        if a1 and a2:
            linhas_array.append([
                normalizeString(linha_atual),
                normalizeString(proxima_linha)
            ])

    return linhas_array