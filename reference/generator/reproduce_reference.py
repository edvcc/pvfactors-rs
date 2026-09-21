"""Verify frozen inputs and run the upstream suite. This does not build a Golden corpus."""
from pathlib import Path
import argparse, hashlib, json, os, subprocess, sys, importlib.metadata as md, re
ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--verify-only',action='store_true')
parser.add_argument('--output-dir',type=Path,help='new directory for logs; required unless --verify-only')
parser.add_argument('--probes',action='store_true',help='also run research probes, not a complete capture generator')
args=parser.parse_args()
errors=[]
manifest=json.loads((ROOT/'evidence/source-file-manifest.json').read_text())
for entry in manifest:
 p=ROOT/'upstream/solarfactors'/entry['path']
 if not p.is_file():errors.append('missing '+entry['path']);continue
 b=p.read_bytes()
 got=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 if got!=entry['sha']:errors.append('blob mismatch '+entry['path'])
if sys.version_info[:3]!=(3,12,14):errors.append('canonical Python must be 3.12.14; got '+sys.version.split()[0])
for line in (ROOT/'reference/requirements-canonical.txt').read_text().splitlines():
 if not line or line.startswith('#'):continue
 name,want=line.split('==',1)
 try:got=md.version(name)
 except md.PackageNotFoundError:errors.append('missing package '+name);continue
 if got!=want:errors.append(f'version {name}: {got} != {want}')
report={'source_files':len(manifest),'canonical_version_errors':errors,'verified':not errors}
print(json.dumps(report,indent=2))
if errors:sys.exit(2)
if args.verify_only:sys.exit(0)
if args.output_dir is None:parser.error('--output-dir is required')
dest=args.output_dir.resolve();dest.mkdir(parents=True,exist_ok=False)
env=os.environ.copy()
env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',MPLBACKEND='Agg',PYTHONHASHSEED='0')
env['PYTHONPATH']=str(ROOT/'upstream/solarfactors')
(dest/'source-and-version-verification.json').write_text(json.dumps(report,indent=2))
with (dest/'pytest.txt').open('w') as log:
 result=subprocess.run([sys.executable,'-m','pytest','pvfactors/tests','-q'],cwd=ROOT/'upstream/solarfactors',env=env,stdout=log,stderr=subprocess.STDOUT)
if result.returncode:sys.exit(result.returncode)
if args.probes:
 subprocess.run([sys.executable,str(ROOT/'reference/generator/probe_reference.py'),'--output-dir',str(dest/'probes')],env=env,check=True,stdout=(dest/'probe-stdout.txt').open('w'))
print('Reference tests completed. Logs: '+str(dest))
