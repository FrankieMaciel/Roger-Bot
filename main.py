from Project.models.chatbot import chatbot

import os

dataset = os.path.join('Project', 'data', 'database.txt')
roger = chatbot('Roger', dataset)

response = roger.run('você?')
print(response)