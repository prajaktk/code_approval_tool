#!/usr/bin/env python3
''' Code Approval Tool
RootDirectory/
    directory1/
        .dependencies => path to other directories that current directory depends on
        .owners => tells who the approver is

1) take in approvers and files changed
2) determine if approvers have sufficient privileges to file/directory

'''
from argparse import ArgumentParser
from typing import List, Set, Dict, Sequence
from collections import defaultdict
from pprint import pprint as pp
import os

base = './'

# populate dependencies
def get_dependencies(files: [str]) -> List[str]:
    dependencies_list = defaultdict(list)

    # get traversal paths for each file
    for file_path in files:
        base_directory = os.path.dirname(file_path)
        while os.path.dirname(file_path) != base:
            file_path = os.path.dirname(file_path)
            dependencies_list.setdefault(base_directory,[]).append(file_path)
    # get all dependencies for each file
    for file_path in files:
        base_directory = os.path.dirname(file_path)
        with open(base_directory +'/.dependencies','r') as f:
            if len((file_content := f.read())) > 0:
                f_paths = file_content.split('\n')
                for p in f_paths:
                    dependencies_list.setdefault(base_directory,[]).append(p)
    return dict(dependencies_list)

# populate owners
def get_owners(dependencies_list): #:
    owners_list = defaultdict(set)
    for file, dependency in dependencies_list.items():
        for directory in dependency:
            with open(directory+'/.owners','r') as f:
                for owner in f.read().split('\n'):
                    owners_list[file].add(owner)
    return dict(owners_list)

#get approver list for each folder
def main(changed_files: List[str], approvers: List[str]) -> None:
    dependencies_dict = get_dependencies(changed_files)
    owners_list = get_owners(dependencies_dict)
    missing_approvals = []
    approvals_needed = set()
    for values in owners_list.values():
        for owner in values:
            approvals_needed.add(owner)
    
    if set(approvers).issubset(approvals_needed):
        pass
    else:
        missing_approvals.append(approvals_needed.difference(set(approvers)))     
    
    if len(missing_approvals) > 0:
        missing_owners = ''
        for element in missing_approvals:
            missing_owners = missing_owners + ' ' + str(element) 
        
        pp(f'Missing Approvals: {missing_owners}'')
        return ('Insufficient approvals')
    else:
        return ('Approved')


if __name__ == "__main__":
    parser = ArgumentParser(
    prog = 'code_approval_tool',
    description = 'An validate approval tool',
    epilog = '',
    allow_abbrev = False,)

    parser.add_argument('--approvers', nargs='*', metavar='approvers')
    parser.add_argument('--changed-files', nargs='*', metavar='changed-files')
    args = parser.parse_args()
    pp(main(args.changed_files, args.approvers))

    approvers = ['alovelace1']
    changed_files = ['./folder2/folder4/test4.txt', './folder3/test3.txt']
    reponse = main(changed_files, approvers)
    assert reponse == 'Insufficient approvals'
    approvers = ['alovelace', 'testuser1', 'testuser', 'testuser4', 'testuser4']
    assert main(changed_files, approvers) == 'Approved'
