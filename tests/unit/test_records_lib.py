import datetime
from unittest import TestCase

from record_lib import (
    Record,
    Gender,
    update_records,
    records_sorted_by_gender_and_last_name,
    records_sorted_by_date_of_birth,
    records_sorted_by_last_name_descending,
    records_sorted_by_order,
    RecordSortOrder,
)


class TestUpdateRecords(TestCase):
    def test_update_records__no_existing_records(self):
        new_records = ["Trate, Josh, Male, green, 08/14/1995"]
        self.assertListEqual(
            [
                Record(
                    last_name="Trate",
                    first_name="Josh",
                    gender=Gender.MALE,
                    favorite_color="green",
                    date_of_birth=datetime.date(1995, 8, 14),
                )
            ],
            update_records([], new_records, ","),
        )

    def test_update_records__existing_records(self):
        existing_records = [
            Record(
                last_name="Trate",
                first_name="Josh",
                gender=Gender.MALE,
                favorite_color="green",
                date_of_birth=datetime.date(1995, 8, 14),
            )
        ]
        new_records = ["Smith, Josh, Male, green, 09/14/1997"]
        self.assertIn(
            Record(
                last_name="Smith",
                first_name="Josh",
                gender=Gender.MALE,
                favorite_color="green",
                date_of_birth=datetime.date(1997, 9, 14),
            ),
            update_records(existing_records, new_records, ","),
        )

    def test_update_records__pipe_separated(self):
        new_records = ["Trate | Josh | Male | green | 08/14/1995"]
        self.assertListEqual(
            [
                Record(
                    last_name="Trate",
                    first_name="Josh",
                    gender=Gender.MALE,
                    favorite_color="green",
                    date_of_birth=datetime.date(1995, 8, 14),
                )
            ],
            update_records([], new_records, "|"),
        )

    def test_update_records__space_separated(self):
        new_records = ["Trate Josh Male green 08/14/1995"]
        self.assertListEqual(
            [
                Record(
                    last_name="Trate",
                    first_name="Josh",
                    gender=Gender.MALE,
                    favorite_color="green",
                    date_of_birth=datetime.date(1995, 8, 14),
                )
            ],
            update_records([], new_records, " "),
        )

    def test_update_records__missing_fields(self):
        new_records = ["Trate Josh Male green"]
        with self.assertRaises(ValueError):
            update_records([], new_records, " ")


class TestRecordsSorted(TestCase):
    def test_records_sorted_by_gender_and_last_name__multiple_records_unsorted(self):
        unsorted_records = [
            Record("Trate", "Josh", Gender.MALE, "green", datetime.date(1995, 8, 14)),
            Record("Smith", "Josh", Gender.MALE, "blue", datetime.date(1997, 9, 1)),
            Record(
                "Zwicki", "Allison", Gender.FEMALE, "brown", datetime.date(2001, 6, 5)
            ),
        ]
        self.assertListEqual(
            records_sorted_by_gender_and_last_name(unsorted_records),
            [
                Record(
                    "Zwicki",
                    "Allison",
                    Gender.FEMALE,
                    "brown",
                    datetime.date(2001, 6, 5),
                ),
                Record("Smith", "Josh", Gender.MALE, "blue", datetime.date(1997, 9, 1)),
                Record(
                    "Trate", "Josh", Gender.MALE, "green", datetime.date(1995, 8, 14)
                ),
            ],
        )

    def test_records_sorted_by_gender_and_last_name__empty_list(self):
        self.assertListEqual([], records_sorted_by_gender_and_last_name([]))

    def test_records_sorted_by_date_of_birth__multiple_records_unsorted(self):
        unsorted_records = [
            Record("Smith", "Josh", Gender.MALE, "blue", datetime.date(1997, 9, 1)),
            Record("Trate", "Josh", Gender.MALE, "green", datetime.date(1995, 8, 14)),
        ]
        self.assertListEqual(
            records_sorted_by_date_of_birth(unsorted_records),
            [
                Record(
                    "Trate", "Josh", Gender.MALE, "green", datetime.date(1995, 8, 14)
                ),
                Record("Smith", "Josh", Gender.MALE, "blue", datetime.date(1997, 9, 1)),
            ],
        )

    def test_records_sorted_by_date_of_birth__empty_list(self):
        self.assertListEqual(records_sorted_by_date_of_birth([]), [])

    def test_records_sorted_by_last_name_descending__multiple_records_unsorted(self):
        unsorted_records = [
            Record("Smith", "Josh", Gender.MALE, "blue", datetime.date(1997, 9, 1)),
            Record("Trate", "Josh", Gender.MALE, "green", datetime.date(1995, 8, 14)),
        ]
        self.assertListEqual(
            records_sorted_by_last_name_descending(unsorted_records),
            [
                Record(
                    "Trate", "Josh", Gender.MALE, "green", datetime.date(1995, 8, 14)
                ),
                Record("Smith", "Josh", Gender.MALE, "blue", datetime.date(1997, 9, 1)),
            ],
        )

    def test_records_sorted_by_last_name_descending__empty_list(self):
        self.assertListEqual(records_sorted_by_last_name_descending([]), [])

    def test_records_sorted_by_order__gender_and_last_name_ascending(self):
        unsorted_records = [
            Record("Trate", "Josh", Gender.MALE, "green", datetime.date(1995, 8, 14)),
            Record("Smith", "Josh", Gender.MALE, "blue", datetime.date(1997, 9, 1)),
            Record(
                "Zwicki", "Allison", Gender.FEMALE, "brown", datetime.date(2001, 6, 5)
            ),
        ]
        self.assertListEqual(
            records_sorted_by_order(
                unsorted_records, RecordSortOrder.GENDER_AND_LAST_NAME_ASCENDING
            ),
            [
                Record(
                    "Zwicki",
                    "Allison",
                    Gender.FEMALE,
                    "brown",
                    datetime.date(2001, 6, 5),
                ),
                Record("Smith", "Josh", Gender.MALE, "blue", datetime.date(1997, 9, 1)),
                Record(
                    "Trate", "Josh", Gender.MALE, "green", datetime.date(1995, 8, 14)
                ),
            ],
        )

    def test_records_sorted_by_order__date_of_birth_ascending(self):
        unsorted_records = [
            Record("Smith", "Josh", Gender.MALE, "blue", datetime.date(1997, 9, 1)),
            Record("Trate", "Josh", Gender.MALE, "green", datetime.date(1995, 8, 14)),
        ]
        self.assertListEqual(
            records_sorted_by_order(
                unsorted_records, RecordSortOrder.DATE_OF_BIRTH_ASCENDING
            ),
            [
                Record(
                    "Trate", "Josh", Gender.MALE, "green", datetime.date(1995, 8, 14)
                ),
                Record("Smith", "Josh", Gender.MALE, "blue", datetime.date(1997, 9, 1)),
            ],
        )

    def test_records_sorted_by_order__last_name_descending(self):
        unsorted_records = [
            Record("Smith", "Josh", Gender.MALE, "blue", datetime.date(1997, 9, 1)),
            Record("Trate", "Josh", Gender.MALE, "green", datetime.date(1995, 8, 14)),
        ]
        self.assertListEqual(
            records_sorted_by_order(
                unsorted_records, RecordSortOrder.LAST_NAME_DESCENDING
            ),
            [
                Record(
                    "Trate", "Josh", Gender.MALE, "green", datetime.date(1995, 8, 14)
                ),
                Record("Smith", "Josh", Gender.MALE, "blue", datetime.date(1997, 9, 1)),
            ],
        )

    def test_records_sorted_by_order__unknown_order(self):
        with self.assertRaises(ValueError):
            records_sorted_by_order([], "unknown")
