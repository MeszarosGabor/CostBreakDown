import csv
import logging
import typing

from django.core import management
import django.db as db

import categorizer.models as models
import categorizer.utils as utils


logger = logging.getLogger(__name__)



def amount_to_int(amount: str) -> int:
    return int(amount.split('.')[0])


def format_date(date: str) -> str:
    """
    Input format: '2023-12-27 13:07:16'
    """
    return date.split(" ")[0]


def load_file(csv_path: str):
    with open(csv_path) as handle:
        reader = csv.DictReader(handle, delimiter=",")
        for line in reader:
            yield line


def filter_transactions(tx_iterator):
    for tx in tx_iterator:
        passing = True
        for attribute in [
            "Amount",
            "Description",
            "Started Date",
        ]:
            if not tx.get(attribute):
                logging.warning(f"{tx} filtered, missing attribute {attribute}")
                passing = False
                break
        if not passing:
            continue

        if amount_to_int(tx["Amount"]) > 0:  # income! 
            logging.warning("Income ignored.")
            continue

        yield tx


class Command(management.BaseCommand):
    help = """
        Load transactions csv file.

        Example:
            python manage.py load_bb_transactions_from_csv
    """
    def handle(self, *args, **options):
        csv_path = options.get("csv_path")
        verbosity = int(options['verbosity'])
        root_logger = logging.getLogger('')
        if verbosity > 1:
            root_logger.setLevel(logging.DEBUG)

        line_generator = load_file(csv_path)
        stats = {
            "transaction_created": 0,
            "transaction_updated": 0,
            "transaction_integrity_error": 0,
            "categorized_transaction_created": 0,
            "categorized_transaction_updated": 0,
            "categorized_transaction_integrity_error": 0,
        }
        for tx in filter_transactions(line_generator):
            # REVOLUT does not send a uuid with the transaction.
            made_up_identifier = tx["Amount"] + tx["Started Date"]
            try:
                transaction_obj, created = models.Transaction.objects.update_or_create(
                    identifier=made_up_identifier,
                    defaults = {
                        "amount": amount_to_int(tx["Amount"]),
                        "date": format_date(tx["Started Date"]),
                        "merchant": tx["Description"],
                        "comments": "",
                    }
                )
                stats["transaction_created"] += int(created)
                stats["transaction_updated"] += 1 - int(created)
            except db.utils.IntegrityError as err:
                stats["transaction_integrity_error"] += 1
                logging.error(f"IntegrityError at {tx}: {err}")
            else:
                try:
                    category_pattern = utils.find_category_pattern(transaction_obj)
                    _, created = models.CategorizedTransaction.objects.update_or_create(
                        transaction=transaction_obj,
                        defaults={
                            "category":category_pattern.category if category_pattern else None,
                            "pattern": category_pattern,
                        }
                    )
                    stats["categorized_transaction_created"] += int(created)
                    stats["categorized_transaction_updated"] += 1 - int(created)
                except db.utils.IntegrityError as err:
                    stats["categorized_transaction_integrity_error"] += 1
                    logging.error(f"IntegrityError at {category_pattern.category}: {err}")
        
        logging.info(f"Population finished. Stats: {stats}")


    def add_arguments(self, parser: management.CommandParser):
        parser.add_argument(
            "--csv_path",
            help="The CSV path of the file containing the transaction data",
            type=str,
            required=False,
        )
