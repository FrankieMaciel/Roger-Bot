import math

def create_position_embedding(dimension, max_length):
    position_embedding = []
    for i in range(max_length):
        embedding = []
        for j in range(dimension):
            if j % 2 == 0:
                val = math.sin(i / (10000 ** (2 * j / dimension)))
            else:
                val = math.cos(i / (10000 ** (2 * j / dimension)))
            embedding.append(val)
        position_embedding.append(embedding)
    return position_embedding

def convert(Msg, contextSize):

    convertText = [ord(c) for c in Msg]
    for i in range(contextSize - len(convertText)):
        convertText.append(0.0)

    embedding_dimension = 1
    PositionEnconding = create_position_embedding(embedding_dimension, contextSize)

    flat_position_embedding = []
    for emb in PositionEnconding:
        flat_position_embedding.extend(emb)

    result_array = [(a + b) for a, b in zip(flat_position_embedding, convertText)]

    return result_array