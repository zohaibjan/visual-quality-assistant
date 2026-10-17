import os
import unittest
from unittest.mock import Mock, patch
from utils.snowflake_utils import query_cortex
from utils.prompt_utils import build_defect_code_prompt
from utils.defect_codes_utils import load_defect_codes, validate_defect_codes
class CoreTests(unittest.TestCase):
    def test_sql_parameters(self):
        session=Mock()
        session.sql.return_value.collect.return_value=[['observations']]
        with patch.dict(os.environ,{'MODEL_NAME':'test-model'}):
            result=query_cortex(session,"quote ' and $$",'@DEMO','image.png')
        sql=session.sql.call_args.args[0]
        self.assertNotIn('quote',sql)
        self.assertEqual(session.sql.call_args.kwargs['params'],['test-model',"quote ' and $$",'@DEMO','image.png'])
        self.assertEqual(result,'observations')
    def test_synthetic_codes(self):
        codes=load_defect_codes('codes/defect_codes.json')
        self.assertEqual(validate_defect_codes(codes),[])
        self.assertTrue(all(x['code'].startswith('DEMO-') for x in codes))
    def test_prompt_sets_review_boundary(self):
        prompt=build_defect_code_prompt('describe',[])
        self.assertIn('A person must review',prompt)
        self.assertIn('UNKNOWN',prompt)
if __name__=='__main__':unittest.main()
