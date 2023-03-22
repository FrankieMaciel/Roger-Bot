from ConvertMsg import create_position_embedding

def createData(prompt, message, contextSize):
    data = []
    for i in range(len(message)):
        promptData = []
        for j in range(i):
            promptData.append(prompt[j])
        for k in range(contextSize - len(promptData)):
            promptData.append(0.0)
        data.append(promptData)
    
    embedding_dimension = 1
    PositionEnconding = create_position_embedding(embedding_dimension, contextSize)

    flat_position_embedding = []
    for emb in PositionEnconding:
        flat_position_embedding.extend(emb)

    result_array = []
    for d in data:
        result_array.append([(a + b) for a, b in zip(flat_position_embedding, d)])

    return result_array