import csv  
import sys
from random import sample
import hashlib

def get_sample(terms):
    total_length = len(terms)
    fifth = total_length // 5
    first_fifth = fifth
    second_fifth = fifth*2
    third_fifth = fifth*3
    fourth_fifth = fifth*4

    first_sample = sample(terms[0:first_fifth], NUM_SAMPLES // 5)
    second_sample = sample(terms[first_fifth + 1:second_fifth], NUM_SAMPLES // 5)
    third_sample = sample(terms[second_fifth + 1:third_fifth], NUM_SAMPLES // 5)
    fourth_sample = sample(terms[third_fifth + 1:fourth_fifth], NUM_SAMPLES // 5)
    fifth_sample = sample(terms[fourth_fifth + 1:total_length], NUM_SAMPLES // 5)

    return first_sample + second_sample + third_sample + fourth_sample + fifth_sample

def read_words_from_output_file(filename):
    terms = []
    with open(filename) as f:
        for line in f:
            items = line.split('\t')
            terms.append(items[0].strip())

    return terms

def 

def read_output_files(files):
    word_set = set()
    for file in files:
        word_set.union(
            set(
                get_sample(
                    read_words_from_output_file(file)
                )
            ))
    
    return word_set

def randomize_word_set(word_set):
    return random.shuffle(list(word_set))






if __name__ == "__main__":
    # We will read in all term files that are passed in with the
    # format: python create_randomized_evaluation_file "file1 file2 file3"
    files = sys.argv[1].split(' ')

    word_set = read_output_files(files)




    shuffled_word_list = randomize_word_set(word_set)


    pass