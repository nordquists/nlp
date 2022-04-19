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

def read_words_from_output_file(filename):
    terms = []
    with open(filename) as f:
        for line in f:
            items = line.split('\t')
            terms.append(items[0].strip())

    return terms

def get_top(terms):
    return terms[0:100]

def write_evaluation_file(sampled_words, output_filename):
    with open(f'./{output_filename}.csv', "w") as f:
        writer = csv.writer(f)
        writer.writerow(['word'])
        for word in sampled_words:
            writer.writerow([word])


if __name__ == '__main__':
    output_filename = sys.argv[1]

    words = read_words_from_output_file(output_filename)

    top = get_top(words)
    for word in top:
        print(word)

    write_evaluation_file(top, output_filename)