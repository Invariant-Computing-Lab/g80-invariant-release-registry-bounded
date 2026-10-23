import unittest,json
from pathlib import Path
from invariant_tools import operate,sha
class BoundedTests(unittest.TestCase):
 def test_fixture_deterministic(self):
  p=json.loads(Path(__file__).with_name('sample.json').read_text('utf-8'))
  a=operate('release_registry',p);b=operate('release_registry',p)
  self.assertEqual(a,b)
  self.assertEqual(a['status'],'PASS')
  self.assertTrue(isinstance(a,dict))
 def test_unknown_operation_fails_closed(self):
  with self.assertRaises(ValueError): operate('unknown',{ })
if __name__=='__main__': unittest.main()
