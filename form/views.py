from django.shortcuts import render
# from django.http import HttpResponse
# from django.template import Context, loader
from django.core.files import File
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
from .models import WordFrequency

#View for frequency page - returns template urlForm
def frequency(request):
    return render(request, "form/urlForm.html")

#View for result page - returns template
def result(request):

    #Function to find the frequency of words appearing on the webpage
    def repetitions(final_list_of_words):

        set_words = set(final_list_of_words) # To remove repeated words
        count_of_words = {} # This dictionary will store all the words with their respective frequency
        max_count = 0
        for word in set_words:
            count_of_words[word] = final_list_of_words.count(word)
        list_of_count = list(count_of_words.values())
        list_of_count = sorted(list_of_count,reverse=True)


        top10 = {} # This dictionary will store the top 10 words with their respective frequency
        num_of_words = 0
        for i in list_of_count:
            if num_of_words >= 10:
                break
            for j in count_of_words:
                if count_of_words[j]==i:
                    # print(j)
                    top10[j]=count_of_words[j]
                    del count_of_words[j]
                    num_of_words = num_of_words + 1
                    break
        return top10

    # print(request.POST['urlField'])
    enteredURL = request.POST['urlField']

    # Query to check whether the url has been used before. If it is used, we fetch the top 10 words from the database
    if WordFrequency.objects.filter(url=enteredURL).exists():
        print("URL exists", WordFrequency.objects.filter(url=enteredURL))
        context={
            "object":WordFrequency.objects.filter(url=enteredURL),
            "title":"Fetched from Database"
        }
        return render(request, "form/result.html", context)

    # If the url has not been used before...
    html = urlopen(enteredURL).read()
    soup = BeautifulSoup(html, "html.parser")

    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'commonWordsFile.txt') # This file was created by scraping the top 100 common words from wikipedia page. The script for the same is in the ATG directory
    words = soup.get_text().split()
    commonWordsFile = open(file_path,"r")
    commonWords = commonWordsFile.read()
    symbols = "!@#$%^&*()-_+={[|\?/>.<,~`]}':;'" # Using it to remove the symbols from the words eg. "folder." "task-" etc

    final_list_of_words = [] #Stores all the words on the webpage
    for word in words:
        word=word.lower()
        if word in commonWords:
            continue
        for ch in word:
            if ch in symbols:
                word=word.replace(ch,'')
        if word=="":
            continue
        final_list_of_words.append(word)

    top10 = repetitions(final_list_of_words) # Stores the top 10 words as a dictionary
    for key in top10:
        obj = WordFrequency(url=enteredURL, word=key, freq=top10[key]) # Creating an object of class WordFrequency to store the top 10 words of the url in the database
        obj.save()

    context={
        "object":WordFrequency.objects.filter(url=enteredURL),
        "title":"Freshly Processed Data"
    }
    return render(request, "form/result.html", context)
