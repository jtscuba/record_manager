import argparse

import tabulate

from record_lib import RecordSortOrder, update_records, records_sorted_by_order


def main(
    comma_separated_file_name: str,
    pipe_separated_file_name: str,
    space_separated_file_name: str,
    sort_order: RecordSortOrder,
) -> None:
    """Read records from provided files and print them in the desired order
    
    Args:
        comma_separated_file_name: name of file with comma separated records
        pipe_separated_file_name: name of the file with pipe separated records
        space_separated_file_name: name of the file with space separated records
        sort_order: order to print the parsed records in
    """
    records = []
    record_files = zip(
        (
            comma_separated_file_name,
            pipe_separated_file_name,
            space_separated_file_name,
        ),
        (",", "|", " "),
    )
    for file_name, delimiter in record_files:
        with open(file_name) as file:
            records = update_records(records, file.readlines(), delimiter)

    sorted_records = records_sorted_by_order(records, sort_order)

    print(
        tabulate.tabulate(
            sorted_records,
            headers=(
                "Last Name",
                "First Name",
                "Gender",
                "Favorite Color",
                "Date of Birth",
            ),
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sort records.")
    parser.add_argument(
        "comma_separated_records_file", help="file containing ',' separated records"
    )
    parser.add_argument(
        "pipe_separated_records_file", help="file containing '|' separated records"
    )
    parser.add_argument(
        "space_separated_records_file", help="file containing ' ' separated records"
    )
    parser.add_argument(
        "output_sort_order", type=RecordSortOrder, choices=list(RecordSortOrder)
    )
    args = parser.parse_args()

    main(
        args.comma_separated_records_file,
        args.pipe_separated_records_file,
        args.space_separated_records_file,
        args.output_sort_order,
    )
