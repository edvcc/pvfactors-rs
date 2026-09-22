import datetime,json,pathlib,subprocess,sys,time
root=pathlib.Path('/Users/chenchen/GitRepo/github.com/edvcc/pvfactors-rs')
work=root/'reference/work/lcb01-owner-closure'
name=sys.argv[1];argv=sys.argv[2:]
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
clean=not subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True).strip()
assert clean,'Tracked/untracked content must be clean before verification'
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
with (work/(name+'.log')).open('w') as f:
 p=subprocess.run(argv,cwd=root,stdout=f,stderr=subprocess.STDOUT,text=True)
record=dict(name=name,argv=argv,tested_content_commit=head,clean_at_start=clean,
 clean_at_end=not subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True).strip(),
 started_at=start,finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-t,exit_code=p.returncode,log=name+'.log')
(work/(name+'-command.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2));print((work/(name+'.log')).read_text()[-2500:])
sys.exit(p.returncode)
