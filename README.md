# Record Manager
A set of utilites for examining user records with a cli interface and a http interface

# Directory Structure
`records_lib.py`: library with primitives for loading and sorting user records  
`records_cli.py`: CLI interface for processing user records stored in files  
`records_server.py`: HTTP interface for loading user records and sorting them  
`tests/unit/`: tests for `records_lib.py` and `records_server.py`. Run the tests with `pytest`  
`tests/cli_e2e_tests`: test for `records_cli.py`. Run the tests with `cd tests/cli_e2e_tests && sh test_records_cli.sh`  

# Running the tests
`source env.py` to set the flask app and project root envronment variables  
`pytest` for the `records_lib.py` and `records_server.py` tests  
`cd tests/cli_e2e_tests && sh test_records_cli.sh` for the e2e cli tests  

# Dependencies
1. `flask`
2. `tabulate`
3. `pytest`
