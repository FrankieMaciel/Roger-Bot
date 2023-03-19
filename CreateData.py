def createData(prompt, message, contextSize, alphabet):
    data = []
    for i in range(len(message)):
        promptData = []
        promptOutput = []
        for j in range(i):
            promptData.append(prompt[j])
        for k in range(contextSize - len(promptData)):
            promptData.append(0.0)
        for y in range(len(alphabet)):
            if alphabet[y] == message[i]:
                promptOutput.append(1.0)
            else:
                promptOutput.append(0.0)
        data.append([promptData, promptOutput])
    
    return data