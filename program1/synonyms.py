import re                               # used in my sentence_at_a_time generator function
import math                             # use in cosine_meteric
import prompt                           # for use in script
import goody                            # for use in script
from collections import defaultdict     #  dicts and defaultdictsare == when they have the same keys/associations
import pickle

# For use in build_semantic_dictionary: see problem specifications
def sentence_at_a_time(open_file : open, ignore_words : {str}) -> [str]:
    end_punct    = re.compile('[.?\!;:]')
    remove_punct = re.compile(r'(,|\'|"|\*|\(|\)|--|'+chr(8220)+'|'+chr(8221)+')')
    prev   = []
    answer = []
    for l in open_file:
        l = remove_punct.sub(' ',l.lower())
        prev = prev + l.split()
        while prev:
            w = prev.pop(0)
            if end_punct.search(w):
                while end_punct.search(w):
                    w = w[0:-1]
                if w != '' and w not in ignore_words:
                    if end_punct.search(w):
                        print(w)
                    answer.append(w)
                    yield answer
                    answer = []
            else:
                if w != '' and w not in ignore_words:
                    answer.append(w)
                    
    # handle special case of last sentence missing final punctuation                
    if answer:
        yield answer


def build_semantic_dictionary(training_files : [open], ignore_file : open) -> {str:{str:int}}:
    ignore_words = set()
    outer_dict = dict()
    for line in ignore_file:
        ignore_words.add(line.rstrip())
    for x in training_files:
        for sentence in sentence_at_a_time(x, ignore_words):
            for word in sentence:
                if word not in outer_dict:
                    outer_dict[word] = dict()
                for x in [z for z in sentence if z != word]:
                    if x not in outer_dict[word].keys() :
                        outer_dict[word][x] = 1
                    else : outer_dict[word][x] += 1
                if outer_dict[word] == {} :
                    del outer_dict[word]
    return outer_dict
            


def dict_as_str(semantic : {str:{str:int}}) -> str:
    string = ''
    final_string = ''
    length = []
    for word in sorted(semantic.keys()):
        string += f'  context for {word} = '
        length.append(len(semantic[word].keys()))
        for k in sorted(semantic[word]):
            if k != sorted(semantic[word])[len(sorted(semantic[word])) - 1]:
                string += f'{k}@{semantic[word][k]}, '
            else: string += f'{k}@{semantic[word][k]}'
        string += '\n'
        final_string += string
        string = ''
    final_string += f'  min/max context lengths = {min(length)}/{max(length)}\n'
    return final_string
            

       
def cosine_metric(context1 : {str:int}, context2 : {str:int}) -> float:
    val = 0
    val2 = 0
    val3 = 0
    for k in context1:
        val += context1[k] * context2.get(k,0)
    for k in context1:
        val2 += context1[k] ** 2
    for k in context2:
        val3 += context2[k] ** 2
    return val / math.sqrt(val2 * val3)


def most_similar(word : str, choices : [str], semantic : {str:{str:int}}, metric : callable) -> str:
    result = (word, 0)
    for choice in choices:
        s = cosine_metric(semantic[choice], semantic[word])
        if s > result[1]:
            result = (choice, s)
    return result[0]
     


def similarity_test(test_file : open, semantic : {str:{str:int}}, metric : callable) -> str:
    pass 




# Script

if __name__ == '__main__':
    # Write script here
    s1 = {'i': {'went': 1, 'gym': 1, 'this': 1, 'morning': 2, 'later': 1, 'rested': 1, 'was': 1, 'tired': 1}, 'went': {'i': 1, 'gym': 1, 'this': 1, 'morning': 1}, 'gym': {'i': 1, 'went': 1, 'this': 1, 'morning': 1}, 'this': {'i': 1, 'went': 1, 'gym': 1, 'morning': 1}, 'morning': {'i': 2, 'went': 1, 'gym': 1, 'this': 1, 'later': 1, 'rested': 1}, 'later': {'morning': 1, 'i': 1, 'rested': 1}, 'rested': {'later': 1, 'morning': 1, 'i': 1}, 'was': {'i': 1, 'tired': 1}, 'tired': {'i': 1, 'was': 1}}
    print(build_semantic_dictionary([open('trivial.txt', encoding='cp1252')],open('ignore_words.txt', encoding='cp1252')))
    print(dict_as_str(s1))
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc5.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
    
    """ignore_words = set()
    outer_dict = dict()
    for line in ignore_file:
        ignore_words.add(line.rstrip())
    sentences = []
    for sentence in sentence_at_a_time(open(training_files), ignore_words):
        sentences.append(sentence)
    for sentence in sentences:
        for word in sentence:
            outer_dict[word] = dict()
    for sentence in sentences:
        for word in sentence:
            for x in outer_dict.keys():
                if x in sentence:
                    if x != word :
                        if x not in outer_dict[word].keys() :
                            outer_dict[word][x] = 1
                        else : outer_dict[word][x] += 1
                
    
    print (outer_dict)"""
