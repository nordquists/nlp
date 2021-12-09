import os
import sys
import glob
from random import sample
import shutil

CPC_ORDERING = ['section',
                'class',
                'subclass',
                'maingroup',
                'subgroup']

def decode_cpc(cpc): 
    parameters = cpc.split('/')
    cpc_dict = dict()

    cpc_dict['section'] = parameters[0] if len(parameters) >= 1 else None
    cpc_dict['class'] = parameters[1] if len(parameters) >= 2 else None
    cpc_dict['subclass'] = parameters[2] if len(parameters) >= 3 else None
    cpc_dict['maingroup'] = parameters[3] if len(parameters) >= 4 else None
    cpc_dict['subgroup'] = parameters[4] if len(parameters) >= 5 else None

    return cpc_dict

def construct_cpc_path(cpc_dict):
    path = ''

    for parameter in CPC_ORDERING:
        if cpc_dict[parameter]:
            path += cpc_dict[parameter]
            path += '/'
        else:
            return path
    return path

def get_relevant_patents(directory, cpc_dict):
    relevant_patents = []
    cpc_path = construct_cpc_path(cpc_dict)

    for filename in glob.iglob(f'{directory}/{cpc_path}**/*.xml', recursive=True):
        relevant_patents.append(filename)

    return relevant_patents

def copy_relevant_patents(relevant_patents, output):
    if not os.path.exists(output):
        os.makedirs(output)
    for f in relevant_patents:
        shutil.copy(f, output + '/' + f.split('/')[-1])

directory = sys.argv[1]
cpc = sys.argv[2]
num_to_sample = int(sys.argv[3])
output = sys.argv[4]

cpc_dict = decode_cpc(cpc)

relevant_patents = get_relevant_patents(directory, cpc_dict)

if len(relevant_patents) > num_to_sample:
    sample_patents = sample(relevant_patents, num_to_sample)
else:
    print("WARNING: Number of patents too small for desired sample size. Continuing anyway.")
    sample_patents = relevant_patents

copy_relevant_patents(sample_patents, output)