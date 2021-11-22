"""
We will take a '.scored_output' output from Termolator and sample 100
lines from the output. 

With the 100 lines sampled, we create a '.csv' file with three columns:
"term", "is_valid_term", and "notes."

After filling out the csv file, run python3 evaluate.py [.csv file] to 
get the recall. 
"""
import csv  
import sys
from random import sample


NUM_SAMPLES = 100

def read_words_from_output_file(filename):
    terms = []
    with open(filename) as f:
        for line in f:
            items = line.split('\t')
            terms.append(items[0])

    return terms

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

def write_evaluation_file(sampled_words, output_filename):
    with open(f'./{output_filename}.csv', "w") as f:
        writer = csv.writer(f)
        writer.writerow(['word','valid','notes'])
        for word in sampled_words:
            writer.writerow([word,'',''])



if __name__ == '__main__':
    output_filename = sys.argv[1]

    words = read_words_from_output_file(output_filename)
    print(words)

    sampled_words = get_sample(words)

    write_evaluation_file(sampled_words, output_filename)