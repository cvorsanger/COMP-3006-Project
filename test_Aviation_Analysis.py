import Aviation_Analysis as AA
import unittest

class Test_Aviation_Analysis(unittest.TestCase):

    def test_write_output_file(self):
        import os
        #Import Test data
        df = AA.import_airport_info()
        f_path = 'Test.csv'
        #Delete Test file if it exists
        if os.path.exists(f_path) == True:
            os.remove(f_path)
        #Check to see if function writes to stdout if no file given
        AA.write_output_file(None, df)
        self.assertFalse(os.path.exists(f_path))
        #Check to see if function writes to a given file
        AA.write_output_file(f_path, df)
        self.assertTrue(os.path.exists(f_path))

    def test_data_option(self): 
        import pandas as pd
        #To test this function we will buld a test DataFrame with know variables
        df=[{'State': 'AZ','Total Air Carrier':2, 'Total Air Taxi':5, 'Total GA':3, 'Total Military':6, 'Calendar Year':2019}]
        df.append({'State': 'AZ','Total Air Carrier':4, 'Total Air Taxi':10, 'Total GA':6, 'Total Military':5, 'Calendar Year':2019})
        df=pd.DataFrame(df)
        #Group DataFrame and test results
        test = AA.data_option(df,'AZ', 'State')
        self.assertEqual(test['Total Air Carrier'].item(),6)
        self.assertEqual(test['Total Air Taxi'].item(),15)
        self.assertEqual(test['Total GA'].item(),9)
        self.assertEqual(test['Total Military'].item(),11)

    def test_import_ops_data(self):
        # Impoert Ops data
        df = AA.import_ops_data()
        # Test dropped columns 
        self.assertNotIn('VFR Overflight Military', df.columns)
        self.assertNotIn('IFR Overflight Air Carrier', df.columns)
        self.assertNotIn('VFR Overflight GA', df.columns)
        # Test created columns
        self.assertIn('Total GA', df.columns)
        self.assertIn('Total Military', df.columns)

    def test_import_airport_info(self):
        #import Airport Info
        df = AA.import_airport_info()
        #Test dropped and created columns
        self.assertNotIn('Facilty', df.columns)
        self.assertIn('Name', df.columns)
        self.assertIn('Abbr', df.columns)
        #Test Abbr and Name split corrected
        self.assertEqual('Mesa/Falcon Field', df[df['Abbr']=='FFZ'].Name.item())
        self.assertEqual('PHX', df[df['Name']=='Phoenix Sky Harbor Intl'].Abbr.item())

if __name__ == '__main__':
    unittest.main()