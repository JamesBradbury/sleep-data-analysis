import unittest

from analyse_from_csv import enrich_missed_sleep


class TestMissedSleepScaled(unittest.TestCase):

    def setUp(self):
        self.row = {}

    def test_max_over_8_ignored(self):
        self.row['Max possible (hrs)'] = float(8)
        self.row['Hours that night'] = float(7)
        result_8 = enrich_missed_sleep(self.row)
        self.row['Max possible (hrs)'] = float(9.5)
        result_9 = enrich_missed_sleep(self.row)
        self.assertEqual(result_8, result_9)

    def test_long_sleep_means_smaller_scaled_missed_sleep_score(self):
        self.row['Max possible (hrs)'] = float(8)
        self.row['Hours that night'] = float(7.25)
        result_missed_0p75_of_8 = enrich_missed_sleep(self.row)
        self.row['Max possible (hrs)'] = float(7)
        self.row['Hours that night'] = float(6.25)
        result_missed_0p75_of_7 = enrich_missed_sleep(self.row)
        self.row['Max possible (hrs)'] = float(6)
        self.row['Hours that night'] = float(5.25)
        result_missed_0p75_of_6 = enrich_missed_sleep(self.row)
        self.assertGreater(result_missed_0p75_of_6, result_missed_0p75_of_7)
        self.assertGreater(result_missed_0p75_of_7, result_missed_0p75_of_8)

    def test_more_missed_means_greater_scaled_missed_sleep_score(self):
        self.row['Max possible (hrs)'] = float(7.5)
        self.row['Hours that night'] = float(7.25)
        result_missed_0p75_of_7p5 = enrich_missed_sleep(self.row)
        self.row['Max possible (hrs)'] = float(7.5)
        self.row['Hours that night'] = float(6)
        result_missed_1p5_of_7 = enrich_missed_sleep(self.row)
        self.row['Max possible (hrs)'] = float(7.5)
        self.row['Hours that night'] = float(5)
        result_missed_2p5_of_7 = enrich_missed_sleep(self.row)
        self.assertGreater(result_missed_2p5_of_7, result_missed_1p5_of_7)
        self.assertGreater(result_missed_1p5_of_7, result_missed_0p75_of_7p5)


class TestExploreSleepScaled(unittest.TestCase):
    def setUp(self):
        self.row = {}

    def test_missed_1_max_8(self):
        self.row['Max possible (hrs)'] = float(8)
        self.row['Hours that night'] = float(7)
        result = enrich_missed_sleep(self.row)
        print(self.row['Max possible (hrs)'], self.row['Hours that night'], result)

    def test_missed_1_max_7(self):
        self.row['Max possible (hrs)'] = float(7)
        self.row['Hours that night'] = float(6)
        result = enrich_missed_sleep(self.row)
        print(self.row['Max possible (hrs)'], self.row['Hours that night'], result)

    def test_missed_1_max_6(self):
        self.row['Max possible (hrs)'] = float(6)
        self.row['Hours that night'] = float(5)
        result = enrich_missed_sleep(self.row)
        print(self.row['Max possible (hrs)'], self.row['Hours that night'], result)

    def test_missed_2_max_8(self):
        self.row['Max possible (hrs)'] = float(8)
        self.row['Hours that night'] = float(6)
        result = enrich_missed_sleep(self.row)
        print(self.row['Max possible (hrs)'], self.row['Hours that night'], result)

    def test_missed_2_max_7(self):
        self.row['Max possible (hrs)'] = float(7)
        self.row['Hours that night'] = float(5)
        result = enrich_missed_sleep(self.row)
        print(self.row['Max possible (hrs)'], self.row['Hours that night'], result)

    def test_missed_2_max_6(self):
        self.row['Max possible (hrs)'] = float(6)
        self.row['Hours that night'] = float(4)
        result = enrich_missed_sleep(self.row)
        print(self.row['Max possible (hrs)'], self.row['Hours that night'], result)

    def test_missed_0p75_max_6p5(self):
        self.row['Max possible (hrs)'] = float(6.5)
        self.row['Hours that night'] = float(5.75)
        result = enrich_missed_sleep(self.row)
        print(self.row['Max possible (hrs)'], self.row['Hours that night'], result)

    def test_missed_0p75_max_6(self):
        self.row['Max possible (hrs)'] = float(5)
        self.row['Hours that night'] = float(4.25)
        result = enrich_missed_sleep(self.row)
        print(self.row['Max possible (hrs)'], self.row['Hours that night'], result)


if __name__ == '__main__':
    unittest.main()
