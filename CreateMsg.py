from ConvertMsg import convert

def create(message, contexSize):

    prompt = convert(message, contexSize)
    
    print(prompt)
    print(len(prompt))
    

    return 'Olá, meu nome é Roger!'