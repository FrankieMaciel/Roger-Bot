import os

pathdir = os.path.join('src','RogerModel','data','messages.html');
resultFile = os.path.join('src','RogerModel','data','basedata.txt');

lines = open(pathdir, encoding='utf-8').\
        read().strip().split('<div class="text">\n')

filteredLines = [line.split('\n')[0] for line in lines]
print(filteredLines)

with open(resultFile, "w") as txt_file:
    for line in filteredLines:
        txt_file.write("".join(line) + "\n") # works with any number of elements in a line