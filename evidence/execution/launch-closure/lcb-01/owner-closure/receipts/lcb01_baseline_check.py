import json,pathlib,subprocess,hashlib
root=pathlib.Path.cwd();work=root/'reference/work/lcb01-owner-closure'
def git(*a):return subprocess.check_output(['git',*a],text=True).strip()
expected={'master':'bc0b7ec1cb17938be9f4d53c83e1fb80a1abd9ba','develop':'fb63a96ef06cc0375fca9dbceb4f59e89e7157a7','feature/p3-rust-geometry-kernel':'c2bc8572a976279abacbcd1d4f9c460233785bdb','research/full-project-launch-closure':'d5bc38ebd6ba853c4cec530e4787d1ab6168203d'}
observed={b.removeprefix('refs/heads/'):s for s,b in (x.split() for x in (work/'protected-remote-refs.txt').read_text().splitlines())}
assert observed==expected,(observed,expected)
paths=['upstream','reference/approved/geometry-golden-v0.1','reference/tolerance','docs/g2','docs/p3','crates/solarfactors-core','Cargo.toml','Cargo.lock','rust-toolchain.toml']
comparisons=[]
for baseline in ['3d854a564afd44b6f50f860454c37582f1ad5302','c2bc8572a976279abacbcd1d4f9c460233785bdb']:
 changes=git('diff','--name-only',baseline,'HEAD','--',*paths).splitlines()
 assert not changes,changes
 comparisons.append(dict(baseline=baseline,paths=paths,changed_files=changes,status='PASS'))
assets=json.loads((work/'assets.json').read_text())
assert assets['checks']['baseline_integrity']['status']=='PASS'
assert assets['checks']['g2']['status']=='PASS'
original=json.loads((root/'evidence/execution/launch-closure/lcb-01/historical/comparator-policy.before-owner-review.json').read_text())
current=json.loads((root/'reference/candidate/vf-lcb01-v0.1/comparator-policy.json').read_text())
nums={k:v for k,v in original.items() if isinstance(v,(int,float))}
assert all(current[k]==v for k,v in nums.items()),nums
report=dict(status='PASS',tested_content_commit=git('rev-parse','HEAD'),clean_at_verification=not git('status','--porcelain'),protected_remote_refs=observed,protected_content=comparisons,baseline_manifest_files=assets['checks']['baseline_integrity']['files'],g2='PASS',production_implementation_started=False,comparator_values_unchanged=nums,approved_geometry_manifest_sha256=assets['checks']['g2']['report']['approved_safety']['approved_manifest_sha256'])
(work/'baseline-integrity.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
