import torch
import os

import sys
sys.path.append("..")

from ConvertMsg import convert

def generate(model, message, contextSize, alfabeto):

    msg = message
    textResult = ''

    for i in range(round(contextSize / 2)):

        prompt = convert(msg, contextSize)
        result = model(torch.tensor(prompt))
       
        max_value = max(result)
        index = result.tolist().index(max_value.item())
        # print(index)
        msg += alfabeto[index]
        textResult += alfabeto[index]

        if  alfabeto[index] == '\n':
            break

    return textResult