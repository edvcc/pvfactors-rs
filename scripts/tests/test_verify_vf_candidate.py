"""Mutation tests: reciprocity and closure must not hide invalid geometric F."""
import copy
import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from verify_vf_candidate import invariants, matrix, fast_group_errors, compare_payload


class VFInvariantTests(unittest.TestCase):
    def setUp(self):
        self.s=[dict(active=[True],length_m=[1.],logical_key=dict(kind='pvrow',row=0,side='front')),
                dict(active=[True],length_m=[1.],logical_key=dict(kind='ground',row=None,side=None))]
        self.f=[[0.,.2,.8],[.2,0.,.8],[0.,0.,0.]]

    def check(self): return invariants(self.f,self.s,1e-10)

    def test_valid_nonzero_matrix(self): self.assertEqual(self.check()['status'],'PASS')

    def test_negative_injection(self):
        self.f[0][1]=-.2
        self.assertEqual(self.check()['status'],'FAIL')

    def test_above_one_injection(self):
        self.f[0][1]=1.2
        self.assertEqual(self.check()['status'],'FAIL')

    def test_reciprocal_but_negative(self):
        self.f=[[0.,-.2,1.2],[-.2,0.,1.2],[0.,0.,0.]]
        r=self.check()
        self.assertEqual(r['reciprocity_max_error'],0.)
        self.assertEqual(r['row_closure_max_error'],0.)
        self.assertEqual(r['bound_violations'],4)
        self.assertEqual(r['status'],'FAIL')

    def test_closure_pass_invalid_entry(self):
        self.f[0]=[0.,1.2,-.2]
        self.assertEqual(self.check()['row_closure_max_error'],0.)
        self.assertEqual(self.check()['status'],'FAIL')

    def test_small_roundoff_allowance_does_not_clamp(self):
        self.f[0]=[0.,-1e-12,1.+1e-12]
        self.f[1]=[-1e-12,0.,1.+1e-12]
        before=copy.deepcopy(self.f)
        self.assertEqual(self.check()['status'],'PASS')
        self.assertEqual(self.f,before)

    def test_nonfinite_is_never_pass(self):
        self.f[0][1]=math.nan
        self.assertEqual(self.check()['status'],'FAIL')

    def test_all_zero_active_matrix_fails(self):
        self.f=[[0.]*3 for _ in range(3)]
        self.assertEqual(self.check()['status'],'FAIL')

    def test_inactive_nonzero_fails(self):
        self.s[0]['active']=[False]
        self.assertEqual(self.check()['status'],'FAIL')

    def test_same_side_nonzero_fails_even_with_bounds(self):
        self.s[1]['logical_key']=dict(kind='pvrow',row=1,side='front')
        self.assertEqual(self.check()['status'],'FAIL')

    def test_duplicate_sparse_entry_fails(self):
        with self.assertRaises(ValueError):
            matrix(dict(surfaces=self.s,matrix=dict(shape=[3,3],omitted_value=0.,entries=[[0,1,.2],[0,1,.3]])))

    def test_oversized_epsilon_rejected(self):
        with self.assertRaises(ValueError): invariants(self.f,self.s,.3)


class VFSeedComparisonTests(unittest.TestCase):
    def setUp(self):
        self.s=[dict(active=[True],length_m=[1.],logical_key=dict(kind='pvrow',row=0,side='back')),
                dict(active=[True],length_m=[1.],logical_key=dict(kind='ground',row=None,side=None))]
        group=dict(row=0,back_ground=.5,back_pv=0.,back_shaded_pv=0.,independent_back_ground=.2,independent_back_pv=0.)
        self.data=dict(surfaces=self.s,matrix=dict(shape=[3,3],omitted_value=0.,entries=[[0,1,.2],[1,0,.2],[0,2,.8],[1,2,.8]]),
            fast_group_candidate=[group])
        self.raw=dict(fast_helpers=[dict(row=0,back_ground=.5,back_pv=0.,back_shaded_pv=0.)])

    def test_fast_valid_finite_aggregation(self):
        self.assertEqual(fast_group_errors(self.data,self.raw,2e-9),[])

    def test_fast_positive_reference_is_not_expected(self):
        self.data['fast_group_candidate'][0]['independent_back_ground']=.5
        self.assertTrue(fast_group_errors(self.data,self.raw,2e-9))

    def test_missing_fast_row_fails(self):
        self.data['fast_group_candidate']=[]
        self.assertTrue(fast_group_errors(self.data,self.raw,2e-9))

    def test_fast_raw_provenance_mutation_fails(self):
        self.data['fast_group_candidate'][0]['back_ground']=.2
        self.assertTrue(fast_group_errors(self.data,self.raw,2e-9))

    def test_expected_mismatch_despite_valid_invariants(self):
        actual=copy.deepcopy(self.data)
        actual['matrix']['entries']=[[0,1,.3],[1,0,.3],[0,2,.7],[1,2,.7]]
        self.assertEqual(invariants(matrix(actual),self.s,1e-10)['status'],'PASS')
        self.assertTrue(compare_payload(self.data,actual,2e-9))

    def test_expected_numeric_budget(self):
        actual=copy.deepcopy(self.data);actual['matrix']['entries'][0][2]+=1e-10
        self.assertEqual(compare_payload(self.data,actual,2e-9),[])

    def test_expected_exact_identity_mutation(self):
        actual=copy.deepcopy(self.data);actual['surfaces'][0]['logical_key']['side']='front'
        self.assertTrue(compare_payload(self.data,actual,2e-9))

    def test_expected_fast_value_mismatch(self):
        actual=copy.deepcopy(self.data);actual['fast_group_candidate'][0]['independent_back_ground']=.3
        self.assertTrue(compare_payload(self.data,actual,2e-9))


if __name__=='__main__': unittest.main()
