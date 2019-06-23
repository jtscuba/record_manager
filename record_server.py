from flask import Flask, Response, jsonify, request

from record_lib import (
    records_sorted_by_date_of_birth,
    records_sorted_by_gender_and_last_name,
    records_sorted_by_last_name_descending,
    update_records,
)

app = Flask(__name__)

# global variable to store current records. In a real
# application this would be replaced by a database of some kind
current_records = []


class InvalidUsage(Exception):
    """Exception for any invalid input passed to an endpoint"""
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        """Initialize a new exception"""
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """get a dictionary representation of the exception"""
        return_value = dict(self.payload or ())
        return_value["message"] = self.message
        return return_value


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """Covert InvalidUsage exceptions to http errors"""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/records", methods=["POST"])
def add_record():
    """Add a new person to the set of records

    This method expects json in the following format
        {
            'separator': ',',
            'record': 'LastName, FirstName, Gender, FavoriteColor, DateOfBirth'
        }
    """
    content = request.json
    if content is None:
        raise InvalidUsage("Invalid json palyload", status_code=400)

    separator = content.get("separator")
    record = content.get("record")

    if separator is None or separator not in ",| ":
        raise InvalidUsage(
            "Separator is missing or not one of comma, pipe, or space", status_code=400
        )

    if record is None:
        raise InvalidUsage("Record is missing", status_code=400)

    try:
        global current_records
        current_records = update_records(current_records, [record], separator)
    except ValueError as e:
        raise InvalidUsage(str(e), status_code=400)

    return jsonify([record.to_dict() for record in current_records]), 201


@app.route("/records/gender", methods=["GET"])
def list_records_by_gender():
    """Get a json list of current records sorted by gender"""
    sorted_records = records_sorted_by_gender_and_last_name(current_records)
    return jsonify([record.to_dict() for record in sorted_records])


@app.route("/records/birthdate", methods=["GET"])
def list_records_by_birthdate():
    """Get a json list of current records sorted by birth date"""
    sorted_records = records_sorted_by_date_of_birth(current_records)
    return jsonify([record.to_dict() for record in sorted_records])


@app.route("/records/name", methods=["GET"])
def list_records_by_last_name():
    """Get a json list of current records sorted by last name"""
    sorted_records = records_sorted_by_last_name_descending(current_records)
    return jsonify([record.to_dict() for record in sorted_records])
