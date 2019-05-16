"""
Convert the json file to MD for readibility
"""

from __future__ import print_function
import argparse
import json
from collections import OrderedDict




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_file','-jf',default='robust04_paper_info.json')
    parser.add_argument('--new_md_file','-mf',default='README.md')
    args=parser.parse_args()


    paper_info = json.load(open(args.json_file))

    with open(args.new_md_file, 'w') as f:
        f.write('# Robust04 Effectiveness  \n\n') 

        f.write('| paper | is neural paper | baseline AP | best AP |  \n')
        f.write(':-------|-----------------|-------------|----------  \n')

        for single_paper_info in paper_info:
            try:
                f.write(
                    '| [{}]({}) | {} | {} | {} |  \n'.format(
                                                    single_paper_info['short_cite'],
                                                    single_paper_info['link'],
                                                    single_paper_info['is_nn_paper'],
                                                    single_paper_info['baseline']['AP'],
                                                    single_paper_info['best']['AP']
                                                )
                )

            except KeyError:
                # ignore paper not having AP
                pass

if __name__ == '__main__':
    main()