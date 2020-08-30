# anagram_api.py
# By Cole Riechert
# Please see README.md for more information

import json
from flask import Flask, request, Response
from statistics import mean

api = Flask(__name__)                       # define the Flask API

# This function takes in a word (from a GET request) and a list of words (from the dictionary.txt file) and returns
# a JSON representation of the word's anagrams.
# It has an optional parameter for number of results, which by default is set to -1 (no limit).
# It also has an optional "proper" parameter which sets whether proper noun anagrams will be included. This is set to
# true by default.

def find_anagrams(word, dictionary, num_results=-1, proper=True):
    anagrams = {
        'anagrams': []
    }
    i = 0
    to_add = True
    if num_results == -1:
        i = -2
    for item in dictionary:
        if sorted(item) == sorted(word) and not item == word:
            if proper == True:
                if item[0].isupper(): to_add = False
            if i < num_results and to_add:
                anagrams['anagrams'].append(item)
                if not num_results == -1:
                    i += 1
    return anagrams

# Here I read from the dictionary.txt file and make a list of words I can read from in later functions.

dict_file = open('resources/dictionary.txt', 'r')

dictionary = dict_file.read().splitlines()
dict_file.close()

# This route is the "single word" endpoint for GET and for DELETE anagrams.
# It receives a word as URL input and returns a JSON representation of its anagrams using the find_anagrams function
# defined above.
# If DELETE request, is takes the word and removes it and any anagrams from the data store words.txt.
# The GET endpoint does nothing with the data store containing words added/removed by POST and DELETE.

@api.route('/anagrams/<path_str>', methods=['GET', 'DELETE'])
def get_data(path_str):
    limit = request.args.get('limit')
    if not limit == None: limit = int(limit)
    else: limit = -1

    proper = request.args.get('proper')
    if not proper == None: proper = bool(proper)
    else: proper = True
    no_json_str = path_str[:len(path_str)-5]            # gets rid of '.json' at end of input for just the word
    anagrams = find_anagrams(no_json_str, dictionary, limit, proper)
    if request.method == 'GET':
        return anagrams
    elif request.method == 'DELETE':
        del_file = open('resources/words.txt', 'r')
        full_file = del_file.read().splitlines()
        del_file.close()
        del_file = open('resources/words.txt', 'w')
        first = True
        for line in full_file:
            if not line == no_json_str and not line in anagrams['anagrams']:
                if not first:
                    del_file.write('\n')
                del_file.write(line)
                first = False
        del_file.close()
        return Response(status=204)


# This route is the "single word" endpoint for DELETE.
# It receives a word as URL input and removes the word from the data store.

@api.route('/words/<path_str>', methods=['DELETE'])
def delete_data(path_str):
    no_json_str = path_str[:len(path_str) - 5]          # gets rid of '.json' at end of input for just the word
    del_file = open('resources/words.txt', 'r')
    full_file = del_file.read().splitlines()
    del_file.close()
    del_file = open('resources/words.txt', 'w')
    first = True
    for line in full_file:
        if not line == no_json_str:
            if not first:
                del_file.write('\n')
            del_file.write(line)
            first = False
    del_file.close()
    return Response(status=204)


# This route is the "all words" endpoint for POST and DELETE.
# It adds to or subtracts from the data store, which is a simple text file with each word on its own line.
# Neither POST nor DELETE in this endpoint have anything to do with the find_anagrams function.

@api.route('/words.json', methods=['POST', 'DELETE'])
def all_data():

    if request.method == 'POST':
        input_str = request.get_data()
        input_json = json.loads(input_str)
        for word in input_json['words']:
            post_pre = open('resources/words.txt', 'r')
            post_list = post_pre.read().splitlines()
            post_pre.close()
            post_file = open('resources/words.txt', 'a')
            if not len(post_list) == 0:
                post_file.write('\n')
            post_file.write(word)
            post_file.close()
        return Response(status=201, content_type='application/json')
    if request.method == 'DELETE':
        wiped_file = open('resources/words.txt', 'w')
        wiped_file.write("")
        wiped_file.close()
        return Response(status=204)

# ----- Optional Endpoints -----

# This is the "stats" endpoint. It takes an input of either min, max, total, or avg and returns whichever value is
# chosen, based on the current contents of the file words.txt.
# If one of those options is not given as the argument, this function will return "Invalid argument input"

@api.route('/stats/<stat_arg>')
def get_stats(stat_arg):
    stat_file = open('resources/words.txt', 'r')
    corpus = stat_file.read().splitlines()
    stat_file.close()

    corpus.sort(key=len)
    if stat_arg == 'total':
        return str(len(corpus))
    elif stat_arg == 'min':
        return str(len(corpus[0]))
    elif stat_arg == 'max':
        return str(len(corpus[len(corpus)-1]))
    elif stat_arg == 'avg':
        sum = 0
        for word in corpus:
            sum += len(word)
        mean = sum/len(corpus)
        return str(mean)
    else:
        return "Invalid argument input"

# Run the API when anagram_api.py is called in command line:

if __name__ == '__main__':
    api.run()
