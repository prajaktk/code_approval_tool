# code_approval_tool
Code Approval Tool
1) take in approvers and files changed
2) determine if approvers have sufficient privileges to file/directory


Expects following directory structure

RootDirectory/
    directory1/
        .dependencies => path to other directories that current directory depends on
        .owners => tells who the approver is
    directory2/
        .dependencies => path to other directories that current directory depends on
        .owners => tells who the approver is
    directory3/
        .dependencies => path to other directories that current directory depends on
        .owners => tells who the approver is