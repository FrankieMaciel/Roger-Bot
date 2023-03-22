import torch
import os

def train(model, epochs, learning_rate, data, message, alphabet):

    loss_function = torch.nn.CrossEntropyLoss()

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr = learning_rate
        )
    
    losses = []

    for epoch in range(epochs):

        ideal = torch.tensor([])
        results = torch.tensor([], requires_grad=True)

        textResult = ''

        for i in range(len(data)):
            # gera e armazena todos os resultados do modelo
            result = model(torch.tensor(data[i]))
            max_value = max(result)
            index = result.tolist().index(max_value.item())
            results = torch.cat((results, torch.tensor([index]) / 100))

            textResult += alphabet[index]

            # gera e amazena todos os resultados esperados
            idealResult = torch.tensor([alphabet.index(message[i]) / 100])
            ideal = torch.cat((ideal, idealResult))

        # print(result)
        # print(ideal)
        # print(results)
        # print(textResult)
        print('teste')

        loss = loss_function(results, ideal)
        losses.append(loss.item())

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f'| Epoch: {epoch} Loss: {loss}')

    torch.save(model.state_dict(), './RogerModel.pth')
    return sum(losses) / len(losses)