from bs4 import BeautifulSoup
from urllib.request import urlopen

enteredURL = "https://en.wikipedia.org/wiki/Most_common_words_in_English"
html = urlopen(enteredURL).read()
soup = BeautifulSoup(html, "html.parser")
words = soup.find_all('a','extiw')
f = open("demofile3.txt", "w")



#open and read the file after the appending:

count=0
for word in words[:-2]:
    print(word.text)
    f.write(word.text+"\n")
    count=count+1
print(count)
f.close()
f = open("demofile3.txt", "r")
print(f.read())
# print(words)
