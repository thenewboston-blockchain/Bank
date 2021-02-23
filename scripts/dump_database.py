import os

"""
python3 scripts/dump_database.py

Running this script will:
- delete all migration files
- delete db.sqlite3
"""


def main():
    for root, _dirs, files in os.walk('thenewboston_bank'):
        if root[-10:] == 'migrations':
            for f in [file for file in files if file[:2] == '00']:
                os.remove(os.path.normpath(os.path.join(root, f)))
            create_init_file(root)


def create_init_file(root):
    init_file = os.path.normpath(os.path.join(root, '__init__.py'))
    if not os.path.exists(init_file):
        with open(init_file, 'wt') as f:
            f.write('')


def remove_database():
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
        print('Database removed')
    else:
        print('No database to remove')


if __name__ == '__main__':
    main()
    remove_database()
