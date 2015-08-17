import sys
import os
from jobs import settings


def _startdir(folder):
    return '{}/{}'.format(os.getcwd(), folder)


def backfill_data(collection_name, source_folder, max=None):
    for k, filename in enumerate(get_files(source_folder)):
        if max is not None and k == max:
            print('Stopped at limit {}'.format(max))
            break
        try:
            filename = '{}{}'.format(_startdir(source_folder), filename)
            print('Backfilling: {}'.format(filename))
            cmd = ('mongoimport --jsonArray --db {} --collection {} --file {}')
            os.system(cmd.format(
                settings.MONGODB_DATABASE,
                collection_name,
                filename,))
        except KeyboardInterrupt:
            print('Stopped.')
            break


# mongoimport --db users --collection contacts --file contacts.json


def get_files(folder, pattern='.json'):
    start_dir = _startdir(folder)
    return filter(lambda x: x.endswith(pattern), os.listdir(start_dir))


if __name__ == '__main__':
    if '--backfill' in sys.argv:
        collection = sys.argv[2]
        folder = sys.argv[3]
        if '--limit' in sys.argv:
            backfill_data(collection, folder, max=sys.argv[5])
        else:
            backfill_data(collection, folder)
