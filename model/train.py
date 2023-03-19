import torch
import os

def train(model, epochs, learning_rate, data):

    loss_function = torch.nn.MSELoss()

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr = learning_rate
        )

    for epoch in range(epochs):

        allResults = torch.tensor([], requires_grad=True)
        allideal = torch.tensor([], requires_grad=True)

        for i in range(len(data)):
            result = model(torch.tensor(data[i][0]))
            allResults = torch.cat((allResults, result))

            idealResult = torch.tensor(data[i][1])
            allideal = torch.cat((allideal, idealResult))

            # print(result)
            # print(idealResult)

        print(allResults)
        loss = loss_function(allResults, allideal)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f'| Epoch: {epoch} Loss: {loss}')

    torch.save(model.state_dict(), './RogerModel.pth')