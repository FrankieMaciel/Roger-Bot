import os
from ConvertMsg import convert
from CreateData import createData
from model.train import train
from model.generate import generate

alphabet = {'a','A','á','Á','à','À','â','Â','ã','Ã','b','B','c','C','ç','Ç','d','D','e',
            'E','é','É','è','È','ê','Ê','f','F','g','G','h','H','i','I','í','Í','ì','Ì',
            'î','Î','j','J','k','K','l','L','m','M','n','N','o','O','ó','Ó','ò','Ò','ô',
            'Ô','õ','Õ','p','P','q','Q','r','R','s','S','t','T','u','U','ú','Ú','ù','Ù',
            'û','Û','v','V','w','W','x','X','y','Y','z','Z','0','1','2','3','4','5','6',
            '7','8','9','!','?','@','#','$','%','¨','&','*','(',')','-','_','+','=',"'",
            '"','<','>',':',';','.',',','/','{','}','[',']','\n',' '}

def create(model, message, contexSize, isToGenerate):

    prompt = convert(message, contexSize)
    print('Prompt criado!')
    data = createData(prompt, message, contexSize)
    print('Dados criado!')
    # print(prompt)
    # print(len(alphabet))

    epochs = 10
    learning_rate = 0.001

    # treina com as mensagens recebidas
    loss = train(model, epochs, learning_rate, data, message, list(alphabet))
    print('Modelo treinado!')

    # gera respostas
    textResult = generate(model, message, contexSize, list(alphabet))
    print('Resposta gerada!')

    return textResult, loss