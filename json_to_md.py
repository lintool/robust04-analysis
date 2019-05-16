"""
Convert the json file to MD for readibility
"""

from __future__ import print_function
import argparse
import json
from collections import OrderedDict




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_file','-jf',default='robust04_papers.json')
    parser.add_argument('--new_md_file','-mf',default='README.md')
    args=parser.parse_args()


    paper_info = json.load(open(args.json_file))

    with open('README.header', 'r') as header_file:
        header = header_file.read()

    with open(args.new_md_file, 'w') as f:
        f.write(header)
        f.write('\n\n')

        f.write('| paper | standard? |neural? | baseline AP | best AP \n')
        f.write(':-------|-----------|--------|:------------|:--------\n')

        for single_paper_info in paper_info:
            baseline = ''
            best = ''

            # Even if an entry doesn't have AP scores, we want to still show, even as empty entry
            if 'baseline' in single_paper_info and 'AP' in single_paper_info['baseline']:
                baseline = single_paper_info['baseline']['AP']

            if 'best' in single_paper_info and 'AP' in single_paper_info['best']:
                best = single_paper_info['best']['AP']

            f.write('| [{}]({}) | {} | {} | {} | {}\n'.format(
                single_paper_info['short_cite'], single_paper_info['cached_pdf'],
                single_paper_info['standard_setting'], single_paper_info['is_neural'], baseline, best))

if __name__ == '__main__':
    main()
