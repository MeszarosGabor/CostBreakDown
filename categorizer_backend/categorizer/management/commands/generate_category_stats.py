import collections
import datetime
import logging
import typing

from django.core import management
import django.db as db

import categorizer.models as models

def prettify_amount(amount: int) -> str:
    amount = abs(amount)
    rev_digits = str(amount)[::-1]
    return ",".join([rev_digits[i: i+3] for i in range(0, len(rev_digits), 3)])[::-1]



class Command(management.BaseCommand):
    help = """
        Load transactions csv file.

        Example:
            python manage.py load_bb_transactions_from_csv
    """
    def handle(self, *args, **options):
        start_date = [int(s) for s in options.get("start_date").split("-")]
        end_date = [int(s) for s in options.get("end_date").split("-")]
        with_details = options.get("details", False)
        verbosity = int(options['verbosity'])
        root_logger = logging.getLogger('')
        if verbosity > 1:
            root_logger.setLevel(logging.DEBUG)


        targets = models.CategorizedTransaction.objects.select_related("transaction").select_related("category").filter(
            transaction__date__gte=datetime.date(*start_date),
            transaction__date__lt=datetime.date(*end_date))

        collector = collections.defaultdict(int)
        detailer = collections.defaultdict(list)

        for target in targets:
            category = target.category.name if target.category else "misc"
            collector[category] += target.transaction.amount
            if with_details:
                detailer[category].append(target)

        for k, v in collector.items():
            print(f"{k:20}: {prettify_amount(abs(v)):10} HUF")
        print(100 * "*")

        if with_details:
            for category, details in detailer.items():
                print(category.upper())
                for tx in sorted(details, key=lambda ctx: ctx.transaction.amount):
                    print(f"\t{tx.transaction.date} {prettify_amount(tx.transaction.amount):5} HUF - {tx.transaction.merchant:30}")


    def add_arguments(self, parser: management.CommandParser):
        parser.add_argument(
            "--start_date",
            help="The start date of the statistics (inclusive). Format: YYYY-MM-DD",
            type=str,
        )
        parser.add_argument(
            "--end_date",
            help="The end date of the statistics (exclusive). Format: YYYY-MM-DD",
            type=str,
        )
        parser.add_argument(
            "--details",
            help="List the items of every category",
            action="store_true",
        )