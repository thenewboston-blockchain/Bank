from distutils.dir_util import copy_tree

from_dir = '/Users/bucky/Desktop/Projects/Validator/v1/network'
to_dir = '/Users/bucky/Desktop/Projects/Bank/v1/network'

if __name__ == '__main__':
    copy_tree(from_dir, to_dir)
