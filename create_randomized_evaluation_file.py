import csv  
import sys
import os
from random import sample
import hashlib
import random

NUM_SAMPLES = 100

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

def read_output_files(files):
    samples = list()
    word_set = set()
    for f in files:
        words = get_sample(read_words_from_output_file(f))
        word_set = word_set | set(words)
        samples.append(words)
    
    return word_set, samples

def randomize_word_set(word_set):
    word_list = list(word_set)
    random.shuffle(word_list)
    return word_list

def create_sample_file(samples):
    with open('./eval/samples.smpl', "w") as f:
        for i, sample in enumerate(samples):
            for word in sample:
                f.write(f"{i}\t{word}")

def write_evaluation_file(sampled_words, output_filename):
    with open(f'./eval/{output_filename}.csv', "w") as f:
        writer = csv.writer(f)
        writer.writerow(['word','valid','notes'])
        for word in sampled_words:
            writer.writerow([word,'',''])


if __name__ == "__main__":
    # We will read in all term files that are passed in with the
    # format: python create_randomized_evaluation_file "file1 file2 file3"
    files = ['l4_base.out_term_list', 'l4_l3.out_term_list', 'l4_l2.out_term_list', 'l4_l1.out_term_list']

    if not os.path.exists('./eval'):
        os.makedirs('./eval')

    word_set, samples = read_output_files(files)
c
    create_sample_file(samples)

    shuffled_word_list = randomize_word_set(word_set)

    write_evaluation_file(shuffled_word_list, 'collated_words')