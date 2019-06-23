import json
import unittest

from record_server import app


class TestRecordServer(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        client = app.test_client()
        self.app = client

    def test_add_record__valid_payload(self):
        resp = self.app.post(
            "/records",
            data=json.dumps(
                {"separator": ",", "record": "Trate, Josh, Male, green, 08/14/1995"}
            ),
            content_type="application/json",
        )

        self.assertEqual(resp.status_code, 201)

    def test_add_record__invalid_json(self):
        resp = self.app.post("/records", data="hi", content_type="application/json")

        self.assertEqual(resp.status_code, 400)

    def test_add_record__missing_separator(self):
        resp = self.app.post(
            "/records",
            data=json.dumps({"record": "Trate, Josh, Male, green, 08/14/1995"}),
            content_type="application/json",
        )

        self.assertEqual(resp.status_code, 400)

    def test_add_record__invalid_separator(self):
        resp = self.app.post(
            "/records",
            data=json.dumps(
                {"separator": "g", "record": "Trate, Josh, Male, green, 08/14/1995"}
            ),
            content_type="application/json",
        )

        self.assertEqual(resp.status_code, 400)

    def test_add_record__missing_record(self):
        resp = self.app.post(
            "/records",
            data=json.dumps({"separator": ","}),
            content_type="application/json",
        )

        self.assertEqual(resp.status_code, 400)

    def test_add_record__invalid_record(self):
        resp = self.app.post(
            "/records",
            data=json.dumps({"separator": "g", "record": "Trate, Josh, Male, green, "}),
            content_type="application/json",
        )

        self.assertEqual(resp.status_code, 400)

    def test_get_records__sorted_by_gender(self):
        resp = self.app.post(
            "/records",
            data=json.dumps(
                {"separator": ",", "record": "Trate, Josh, Male, green, 08/14/1995"}
            ),
            content_type="application/json",
        )

        resp = self.app.get("/records/gender")
        self.assertEqual(resp.status_code, 200)

    def test_get_records__sorted_by_date_of_birth(self):
        resp = self.app.post(
            "/records",
            data=json.dumps(
                {"separator": ",", "record": "Trate, Josh, Male, green, 08/14/1995"}
            ),
            content_type="application/json",
        )

        resp = self.app.get("/records/birthdate")
        self.assertEqual(resp.status_code, 200)

    def test_get_records__sorted_by_last_name(self):
        resp = self.app.post(
            "/records",
            data=json.dumps(
                {"separator": ",", "record": "Trate, Josh, Male, green, 08/14/1995"}
            ),
            content_type="application/json",
        )

        resp = self.app.get("/records/name")
        self.assertEqual(resp.status_code, 200)
