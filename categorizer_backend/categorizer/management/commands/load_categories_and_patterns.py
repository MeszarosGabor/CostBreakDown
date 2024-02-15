import json
import logging
import typing

from django.core import management
import django.db as db

import categorizer.models as models


logger = logging.getLogger(__name__)


def load_file(file_path: str):
    with open(file_path) as handle:
        return json.load(handle)


class Command(management.BaseCommand):
    help = """
        Load transactions csv file.

        Example:
            python manage.py load_bb_transactions_from_csv
    """
    def handle(self, *args, **options):
        json_path = options.get("json_path")
        verbosity = int(options['verbosity'])
        root_logger = logging.getLogger('')
        if verbosity > 1:
            root_logger.setLevel(logging.DEBUG)

        categories_and_patterns = load_file(json_path)

        stats = {
            "category_created": 0,
            "category_updated": 0,
            "category_integrity_error": 0,
            "pattern_created": 0,
            "pattern_updated": 0,
            "pattern_integrity_error": 0,
        }
        for category in categories_and_patterns:
            try:
                category_obj, created = models.Category.objects.update_or_create(name=category)
                stats["category_created"] += int(created)
                stats["category_updated"] += 1 - int(created)
            except db.utils.IntegrityError as err:
                stats["category_integrity_error"] += 1
                logging.error(f"IntegrityError at category {category}: {err}")
            for pattern in categories_and_patterns[category]:
                try:
                    _, created = models.CategoryPattern.objects.update_or_create(
                        pattern=pattern,
                        defaults={
                            "category": category_obj
                        }
                    )
                    stats["pattern_created"] += int(created)
                    stats["pattern_updated"] += 1 - int(created)
                except db.utils.IntegrityError as err:
                    stats["pattern_integrity_error"] += 1
        logging.info(f"Population finished. Stats: {stats}")


    def add_arguments(self, parser: management.CommandParser):
        parser.add_argument(
            "--json_path",
            help="The JSON path of the file containing the categories and patterns",
            type=str,
            required=False,
        )
