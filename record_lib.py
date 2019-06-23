import datetime
import functools
import operator
from datetime import date, datetime
from enum import unique, Enum
from typing import NamedTuple, List


@unique
@functools.total_ordering
class Gender(Enum):
    """Enum of the possible genders
    
    We define less than to allow sorting by gender.
    """
    FEMALE = "Female"
    MALE = "Male"

    def __str__(self):
        return self.value

    def __lt__(self, other):
        return self == Gender.FEMALE and other == Gender.MALE


class Record(NamedTuple):
    """Represents the information about a single person"""
    last_name: str
    first_name: str
    gender: Gender
    favorite_color: str
    date_of_birth: date

    def to_dict(self):
        """Returns the record as a dictionary
        
        We define this so records can be serialized as json
        """
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "gender": self.gender.value,
            "favorite_color": self.favorite_color,
            "date_of_birth": self.date_of_birth.strftime("%m/%d/%Y"),
        }


@unique
class RecordSortOrder(Enum):
    """Possible sort orders of records"""
    GENDER_AND_LAST_NAME_ASCENDING = "gender_and_last_name_ascending"
    DATE_OF_BIRTH_ASCENDING = "date_of_birth_ascending"
    LAST_NAME_DESCENDING = "last_name_descending"

    def __str__(self):
        return self.value


def update_records(
    current_records: List[Record], new_records: List[str], delimiter: str
) -> List[Record]:
    """Combine existing records with records parsed from new records

    Args:
        current_records: Existing records
        new_records: list str to parse into records
        delimiter: separator to use when parsing new records
    Returns:
        A list containing both the new and existing records
    Raises:
        ValueError if one of the new records could not be parsed
    """
    combined_records = current_records.copy()
    for line in new_records:
        fields = [field.strip() for field in line.split(delimiter)]

        if len(fields) != 5:
            raise ValueError(f"record '{line}' does not have 5 fields")

        gender = Gender(fields[2])
        date_of_birth = datetime.strptime(fields[4], "%m/%d/%Y").date()

        combined_records.append(
            Record(
                last_name=fields[0],
                first_name=fields[1],
                gender=gender,
                favorite_color=fields[3],
                date_of_birth=date_of_birth,
            )
        )
    return combined_records


def records_sorted_by_gender_and_last_name(records: List[Record]) -> List[Record]:
    """Return a list of records sorted by gender and last name

    Args:
        records: list of records to sort
    Returns:
        records sorted by gender and last name
    """
    return sorted(records, key=operator.attrgetter("gender", "last_name"))


def records_sorted_by_date_of_birth(records: List[Record]) -> List[Record]:
    """Return a list of records sorted by date of birth

    Args:
        records: list of records to sort
    Returns:
        records sorted by date of birth
    """
    return sorted(records, key=operator.attrgetter("date_of_birth"))


def records_sorted_by_last_name_descending(records: List[Record]) -> List[Record]:
    """Return a list of records sorted by last name descending

    Args:
        records: list of records to sort
    Returns:
        records sorted by last name descending
    """
    return sorted(records, key=operator.attrgetter("last_name"), reverse=True)


def records_sorted_by_order(records: List[Record], order: RecordSortOrder):
    """Return records sorted by the given order
    
    Args:
        records: records to sort
        order: order to sort the records into
    Returns:
        sorted records
    Raises:
        ValueError: if the provided order is unknown
    """
    if order == RecordSortOrder.GENDER_AND_LAST_NAME_ASCENDING:
        return records_sorted_by_gender_and_last_name(records)
    elif order == RecordSortOrder.DATE_OF_BIRTH_ASCENDING:
        return records_sorted_by_date_of_birth(records)
    elif order == RecordSortOrder.LAST_NAME_DESCENDING:
        return records_sorted_by_last_name_descending(records)
    else:
        raise ValueError(f"Unhandled sort order {order}")
