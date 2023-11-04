from Project.models.chatbot import chatbot

import os

dataset = os.path.join('Project', 'data', 'database.txt')
roger = chatbot('Roger', dataset)

response = roger.run('Qual o seu nome?')
print('Qual o seu nome?' + ' : ' + response)

response2 = roger.run('tudo bem?')
print('tudo bem?' + ' : ' + response2)

response3 = roger.run('Bom dia!')
print('Bom dia!' + ' : ' + response3)