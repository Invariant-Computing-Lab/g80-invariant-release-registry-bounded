import json, subprocess, sys, tempfile, unittest
from pathlib import Path
from invariant_tools import operate

class ReleaseContracts(unittest.TestCase):
 def test_empty_evidence_never_passes(self):
  for op in ['ci_acceptance','claim_gate','dataset_split_audit','reproducibility_cli','evidence_schema','classification_benchmark']:
   with self.subTest(op=op),self.assertRaises(ValueError):operate(op,{'records':[]})
 def test_false_string_not_boolean(self):
  with self.assertRaises(ValueError):operate('classification_benchmark',{'records':[{'truth':'false','prediction':True}]})
 def test_forged_approval_held(self):
  self.assertEqual(operate('human_approval',{'approval':{'human_signed':'false','actor':'x','scope':'all'}})['status'],'HOLD')
  self.assertFalse(operate('human_approval',{'approval':{'human_signed':True,'actor':'x','scope':'all'}})['approved'])
 def test_empty_oracle_rejected(self):
  with self.assertRaises(ValueError):operate('finite_oracles',{'records':[{}]})
 def test_windows_archive_paths_blocked(self):
  for p in ['../x','/x','C:/secret','..\\x','x//a','CON.txt']:
   with self.subTest(path=p):self.assertEqual(operate('archive_indexer',{'records':[{'path':p}]})['status'],'HOLD')
 def test_good_archive_path(self):
  self.assertEqual(operate('archive_indexer',{'records':[{'path':'src/main.py'}]})['status'],'PASS')
 def test_invalid_split_rejected(self):
  with self.assertRaises(ValueError):operate('dataset_split_audit',{'records':[{'source_sha256':'a'*64,'split':None}]})
 def test_split_leak_detected(self):
  self.assertEqual(operate('dataset_split_audit',{'records':[{'source_sha256':'a'*64,'split':s} for s in ['train','test']]})['status'],'HOLD')
 def test_nonfinite_rejected(self):
  with self.assertRaises(ValueError):operate('synthetic_distributed_bench',{'replicas':[float('nan')],'dropped':[]})
 def test_fractional_bits_rejected(self):
  for x in [True,1.5,'2044']:
   with self.subTest(value=x),self.assertRaises(ValueError):operate('side_information_limits',{'alternatives':x})
 def test_graph_cycle(self):
  self.assertTrue(operate('authority_graph',{'edges':[['a','b'],['b','a']]})['cycle_detected'])
 def test_deep_graph_without_recursion_failure(self):
  self.assertEqual(operate('authority_graph',{'edges':[[str(i),str(i+1)] for i in range(1500)]})['status'],'PASS')
 def test_bad_probability_rejected(self):
  with self.assertRaises(ValueError):operate('auxiliary_lift',{'state':[-1,2],'transition':[[1,0],[0,1]]})
 def test_duplicate_registry_not_lost(self):
  self.assertEqual(operate('release_registry',{'records':[{'code':'G01','status':'x'},{'code':'G01','status':'y'}]})['status'],'HOLD')
 def test_public_status_not_approval(self):
  self.assertEqual(operate('release_registry',{'records':[{'code':'G01','status':'PUBLIC_APPROVED_AND_VERIFIED'}]})['approved_public_count'],0)
 def test_cli_invalid_json_nonzero(self):
  with tempfile.TemporaryDirectory() as t:
   f=Path(t)/'bad.json';f.write_text('{bad')
   r=subprocess.run([sys.executable,str(Path(__file__).with_name('run.py')),'--input',str(f)],capture_output=True,text=True)
   self.assertEqual(r.returncode,1);self.assertEqual(json.loads(r.stdout)['status'],'FAIL')
if __name__=='__main__':unittest.main()
