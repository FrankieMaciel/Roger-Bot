from src.RogerModel.config import DEL_token

def remove_items_by_indices(input_list, indices_to_remove):
    # Ordena os índices em ordem decrescente para que a remoção não altere os índices dos outros elementos.
    indices_to_remove.sort(reverse=True)

    for index in indices_to_remove:
        # Verifica se o índice está dentro dos limites válidos da lista
        if 0 <= index < len(input_list):
            del input_list[index]

    return input_list

def removeDelTokens(output):
    removeIndexes = []
    for index, item in enumerate(output):
        if index == (len(output) - 1): break
        if output[index + 1][0] == DEL_token:
            removeIndexes.append(index)
            removeIndexes.append(index + 1)
            print('Apagado')

    return remove_items_by_indices(output, removeIndexes)
