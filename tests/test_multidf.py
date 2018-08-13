#########################
# Standard Library Import
#########################

import os
from unittest import TestCase

import pandas as pd

import gdelt
from gdelt.multipdf import _parallelize_dataframe


#########################
# Third Party Import
#########################
############################
# Custom Import
############################
class testMultiDf(TestCase):

    def test_multidf_gpd_creation(self):
        """Test creating a geometry column"""


        # loading the mock dataframe return
        events2 = pd.read_pickle(os.path.join(
                gdelt.base.BASE_DIR, "data",
                "events2samp.gz"),
                compression="gzip")

        try:
            # Applying the function
            events2 = events2.\
                assign(geometry=_parallelize_dataframe(events2))
            return self.assertTrue('geometry' in events2.columns)
        except:
            exp= ('You need to install shapely to use this feature.')
            with self.assertRaises(Exception) as context:
                events2 = events2. \
                    assign(geometry=_parallelize_dataframe(events2))
            the_exception = context.exception


            return self.assertIsInstance(str(the_exception),str, "Not installed")



