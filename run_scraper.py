import argparse

from scraper import TableScraper
from db_init import Database

db = Database()


if __name__ == '__main__':
    """Script for running Scraper"""

    parser = argparse.ArgumentParser()
    parser.add_argument('--dry_run', '-D', action="store_true",
                        help='Variable for printing table')

    args = vars(parser.parse_args())
    tp = TableScraper()
    data = tp.get_data_by_url()

    if args['dry_run']:
        tp.print_table()
    else:
        db.insert_data_to_db(data)


