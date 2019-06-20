import argparse
import operator
from enum import Enum, auto, unique
from typing import NamedTuple, List
import datetime
from datetime import date, datetime
import tabulate

@unique
class Gender(Enum):
    FEMALE = 'Female'
    MALE = 'Male'


class Record(NamedTuple):
    first_name: str
    last_name: str
    gender: Gender
    favorite_color: str
    date_of_birth: date


@unique
class RecordSortOrder(Enum):
    GENDER_AND_LAST_NAME_ASCENDING = 'gender_and_last_name_ascending'
    DATE_OF_BIRTH_ASCENDING = 'date_of_birth_ascending'
    LAST_NAME_DESCENDING = 'last_name_descending'


def update_records(current_records: List[Record], new_records: List[str], delimiter: str) -> List[Record]:
    combined_records = current_records.copy()
    for line in new_records:
        fields = line.split(delimiter)
        combined_records.append(
            Record(
                first_name=fields[0],
                last_name=fields[1],
                gender=Gender.get(fields[2]),
                favorite_color=fields[3],
                date_of_birth=datetime.strptime(fields[4], '%m/%d/%Y').date(),
            )
        )
    return combined_records


def records_sorted_by_gender_and_last_name(records: List[Record]) -> List[Record]:
    return sorted(records, key=operator.attrgetter('gender', 'last_name'))


def records_sorted_by_date_of_birth(records: List[Record]) -> List[Record]:
    return sorted(records, key=operator.attrgetter('date_of_birth'))


def records_sorted_by_last_name_descending(records: List[Record]) -> List[Record]:
    return sorted(records, key=operator.attrgetter('last_name'), reverse=True)


def records_sorted_by_order(records: List[Record], order: RecordSortOrder):
    if order == RecordSortOrder.GENDER_AND_LAST_NAME_ASCENDING:
        return records_sorted_by_gender_and_last_name(records)
    elif order == RecordSortOrder.DATE_OF_BIRTH_ASCENDING:
        return records_sorted_by_date_of_birth(records)
    elif order == RecordSortOrder.LAST_NAME_DESCENDING:
        return records_sorted_by_last_name_descending(records)
    else:
        raise ValueError(f"Unhandled sort order {order}")


def main(
        comma_separated_file_name: str,
        pipe_separated_file_name: str,
        space_separated_file_name: str,
        sort_order: RecordSortOrder
) -> None:
    records = []
    record_files = zip(
        (comma_separated_file_name, pipe_separated_file_name, space_separated_file_name),
        (',', '|', ' ')
    )
    for file_name, delimiter in record_files:
        with open(file_name) as file:
            records = update_records(records, file.readlines(), delimiter)

    sorted_records = records_sorted_by_order(records, sort_order)

    print(
        tabulate.tabulate(
            sorted_records,
            headers=('First Name', 'Last Name', 'Gender', 'Favorite Color', 'Date of Birth')
        )
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Sort records.")
    parser.add_argument('comma_separated_records_file', help="file containing ',' separated records")
    parser.add_argument('pipe_separated_records_file', help="file containing '|' separated records")
    parser.add_argument('space_separated_records_file', help="file containing ' ' separated records")
    parser.add_argument('output_sort_order', type=RecordSortOrder, choices=list(RecordSortOrder))
    args = parser.parse_args()

    main(
        args.comma_separated_records_file,
        args.pipe_separated_records_file,
        args.space_separated_records_file,
        args.output_sort_order
    )
