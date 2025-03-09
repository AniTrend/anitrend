import unittest
from datetime import datetime

from core.utilities import TimeUtility


class TimeUtilTestCase(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.time_util = TimeUtility(

            time_zone="Africa/Johannesburg"
        )

    def test_as_local_time(self):
        expected = datetime.strptime('2020-03-16T21:37:14+0200', '%Y-%m-%dT%H:%M:%S%z')
        result = self.time_util.as_local_time('2020-03-16T19:37:14+0000', '%Y-%m-%dT%H:%M:%S%z')
        self.assertEqual(expected.toordinal(), result.toordinal())

