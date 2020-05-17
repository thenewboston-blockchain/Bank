from distutils.dir_util import copy_tree

from_dir = '/Users/bucky/Desktop/Projects/thenewboston-python/thenewboston'
to_dir = '/Users/bucky/Desktop/Projects/Bank/thenewboston'

if __name__ == '__main__':
    copy_tree(from_dir, to_dir)
