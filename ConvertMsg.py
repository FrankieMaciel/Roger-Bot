def convert(Msg, contextSize):

    convertText = [ord(c) for c in Msg]
    for i in range(contextSize - len(convertText)):
        convertText.append(0)

    

    return convertText