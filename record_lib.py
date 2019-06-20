import datetime
import functools
import operator
from datetime import date, datetime
from enum import unique, Enum
from typing import NamedTuple, List


@unique
@functools.total_ordering
class Gender(Enum):
    FEMALE = 'Female'
    MALE = 'Male'

    def __str__(self):
        return self.value

    def __lt__(self, other):
        return self == Gender.FEMALE and other == Gender.MALE


class Record(NamedTuple):
    last_name: str
    first_name: str
    gender: Gender
    favorite_color: str
    date_of_birth: date


@unique
class RecordSortOrder(Enum):
    GENDER_AND_LAST_NAME_ASCENDING = 'gender_and_last_name_ascending'
    DATE_OF_BIRTH_ASCENDING = 'date_of_birth_ascending'
    LAST_NAME_DESCENDING = 'last_name_descending'

    def __str__(self):
        return self.value


def update_records(current_records: List[Record], new_records: List[str], delimiter: str) -> List[Record]:
    combined_records = current_records.copy()
    for line in new_records:
        fields = [field.strip() for field in line.split(delimiter)]
        combined_records.append(
            Record(
                last_name=fields[0],
                first_name=fields[1],
                gender=Gender(fields[2]),
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
