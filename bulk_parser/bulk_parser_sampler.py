import sys
import glob







curr_path = ''
# root_dir needs a trailing slash (i.e. /root/dir/)
for filename in glob.iglob(root_dir + f'./{curr_path}/**/*.xml', recursive=True):
     print(filename)






if __name__ == '__main__':
    category_tree = sys.argv[1]
    num_to_sample = sys.argv[2]
    output_file = sys.argv[3]

    categories_separated = category_tree.split('.')

    sampled, num_sampled, total = sample_patents(categories_separated, int(num_to_sample))

    if total == 0:
        print("Error: category does not have any patents.")
        exit()
    elif total < int(num_to_sample):
        print(f"Warning: not enough patents in that category to sample {num_to_sample} patents.")

    write_sampled_patents(sampled)

    print(f"Sampled {num_sampled} from a total of {total}.")