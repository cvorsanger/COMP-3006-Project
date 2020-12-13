import Covid, unittest
import pandas as pd

class TestCovid(unittest.TestCase):

    def test_import_data(self):
        #Import data and check engineered columns were created
        df = Covid.import_data()
        self.assertIsNotNone(df)
        self.assertIn('Total GA', df.columns)
        self.assertIn('Total Military', df.columns)

    def test_ops_percentage(self):
        from pandas.testing import assert_frame_equal
        #Create a test dataframe and test if it is equal to known answers
        test_df=pd.DataFrame([{'Calendar Year': 2019,'Total Air Carrier': 3, 'Total Air Taxi': 1, 'Total GA':4, 'Total Military':2, 'Facility':'AAA'}])
        answer_df=pd.DataFrame([{'Facility':'AAA', 'Total':10, '2019 Percent GA': 40.0, '2019 Percent Air Carrier':30.0}])
        assert_frame_equal(Covid.ops_percentages(test_df), answer_df)

    def test_section_airports(self):
        #Test Case for Almost All GA
        df=pd.DataFrame([{'2019 Percent GA': 85.0, 'Facility':'AAA'}])
        a = df.apply(Covid.section_airports, axis=1)
        self.assertAlmostEqual(a.item(), 1)
        #Test Case for Mostly GA
        df=pd.DataFrame([{'2019 Percent GA': 79.9, 'Facility':'AAA'}])
        a = df.apply(Covid.section_airports, axis=1)
        self.assertAlmostEqual(a.item(), 2)
        #Test Case for ~ 50/50 split
        df=pd.DataFrame([{'2019 Percent GA': 54.75, 'Facility':'AAA'}])
        a = df.apply(Covid.section_airports, axis=1)
        self.assertAlmostEqual(a.item(), 3)
        #Test case for Mostly Commercial
        df=pd.DataFrame([{'2019 Percent GA': 20.0, 'Facility':'AAA'}])
        a = df.apply(Covid.section_airports, axis=1)
        self.assertAlmostEqual(a.item(), 4)
        #Test case for Almost all Commercial
        df=pd.DataFrame([{'2019 Percent GA': 0.6, 'Facility':'AAA'}])
        a = df.apply(Covid.section_airports, axis=1)
        self.assertAlmostEqual(a.item(), 5)

if __name__ == '__main__':
    unittest.main()