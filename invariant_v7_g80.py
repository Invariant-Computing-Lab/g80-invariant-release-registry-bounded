"""Bounded, offline, inspectable utilities. No third-party AI models or data access.
Every operation returns a result describing only the computation actually performed.
"""
from __future__ import annotations
import hashlib, json, math, pathlib, re, sys, zipfile
from collections import Counter, defaultdict


def sha(v):
    if isinstance(v, (bytes, bytearray)): return hashlib.sha256(v).hexdigest()
    return sha(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8'))


def _records(p):
    rows=p.get('records',[])
    if not isinstance(rows,list): raise ValueError('records must be a list')
    return rows


def _finite_num(n):
    if isinstance(n,bool) or not isinstance(n,(int,float)) or not math.isfinite(n):raise ValueError('finite number required')
    return float(n)


def operate(op,p):
    """Deterministic behavior; examples are synthetic fixtures, not domain validation."""
    if not isinstance(p,dict): raise ValueError('input must be JSON object')
    if op=='synthetic_distributed_bench':
        replicas=[_finite_num(v) for v in p.get('replicas',[])]
        dropped=set(p.get('dropped',[])); active=[v for i,v in enumerate(replicas) if i not in dropped]
        if not active: return {'status':'HOLD','reason':'NO_ACTIVE_REPLICAS'}
        return {'status':'PASS','kind':'synthetic_only','mean':sum(active)/len(active),'active':len(active),'requested':len(replicas)}
    if op=='finite_recoverability':
        source=bytes.fromhex(p['hex']); encoded=source.hex(); recovered=bytes.fromhex(encoded)
        return {'status':'PASS' if recovered==source else 'FAIL','finite_example':True,'sha256':sha(source),'bytes':len(source),'lossless':recovered==source,'compression_claim':False}
    if op=='side_information_limits':
        alternatives=int(p.get('alternatives',0))
        if alternatives<=0:raise ValueError('alternatives must be >0')
        return {'status':'PASS','min_bits_for_uniform_index':(alternatives-1).bit_length(),'counting_bound_only':True,'includes_storage_and_side_information':False}
    if op=='checkpoint_replay':
        events=_records(p);state={}
        for ev in events:
            if not isinstance(ev,dict) or not isinstance(ev.get('key'),str):raise ValueError('invalid event')
            if ev.get('op')=='set':state[ev['key']]=ev.get('value')
            elif ev.get('op')=='delete':state.pop(ev['key'],None)
            else: raise ValueError('unsupported replay op')
        return {'status':'PASS','state':state,'state_sha256':sha(state),'event_count':len(events)}
    if op=='exact_fallback':
        data=bytes.fromhex(p['original_hex']); candidate=bytes.fromhex(p.get('candidate_hex',''))
        recovered=candidate if candidate==data else data
        return {'status':'PASS','fallback_used':candidate!=data,'exact_recovery':recovered==data,'integrity':sha(recovered),'no_compression_ratio_claim':True}
    if op=='fault_injection':
        original=bytearray.fromhex(p['hex']);pos=int(p.get('position',0))
        if not 0<=pos<len(original):raise ValueError('invalid flip position')
        before=sha(original);original[pos]^=1
        return {'status':'PASS','fault_detected':before!=sha(original),'position':pos}
    if op=='replicated_recovery':
        replicas=p.get('replicas',[])
        if not isinstance(replicas,list) or not replicas:return {'status':'HOLD','reason':'NO_REPLICAS'}
        valid=[r for r in replicas if isinstance(r,str) and re.fullmatch('[0-9a-f]*',r) and len(r)%2==0]
        votes=Counter(valid)
        if not votes:return {'status':'HOLD','reason':'NO_VALID_REPLICAS'}
        winner,count=votes.most_common(1)[0]
        if count<=len(replicas)//2:return {'status':'HOLD','reason':'NO_STRICT_MAJORITY'}
        return {'status':'PASS','majority_sha256':sha(bytes.fromhex(winner)),'agreed':count,'total':len(replicas)}
    if op=='nondestruction':
        before=p.get('before',{});after=p.get('after',{})
        if not isinstance(before,dict) or not isinstance(after,dict):raise ValueError('manifests must be objects')
        changed=[k for k,v in before.items() if after.get(k)!=v]
        return {'status':'PASS' if not changed else 'FAIL','preserved':not changed,'changed_keys':changed}
    if op=='finite_oracles':
        cases=_records(p); bad=[i for i,row in enumerate(cases) if row.get('expected')!=row.get('observed')]
        return {'status':'PASS' if not bad else 'FAIL','evaluated':len(cases),'mismatched_indices':bad}
    if op=='authority_graph':
        edges=p.get('edges',[]); graph=defaultdict(set)
        for a,b in edges:graph[a].add(b)
        vis=set();stack=set()
        def visit(u):
            if u in stack:return False
            if u in vis:return True
            vis.add(u);stack.add(u)
            for v in graph[u]:
                if not visit(v):return False
            stack.remove(u);return True
        cycle=not all(visit(u) for u in list(graph))
        return {'status':'HOLD' if cycle else 'PASS','cycle_detected':cycle,'edge_count':len(edges)}
    if op=='role_delegation':
        grant=set(p.get('grantor_permissions',[]));want=set(p.get('requested_permissions',[]))
        return {'status':'PASS' if want<=grant else 'HOLD','delegable':want<=grant,'excess':sorted(want-grant)}
    if op=='provenance_chain':
        head='0'*64
        for row in _records(p):head=sha({'previous':head,'entry':row})
        return {'status':'PASS','chain_sha256':head,'event_count':len(p.get('records',[])),'note':'not a cryptographic signature'}
    if op=='conflict_resolution':
        actions=_records(p); by_resource=defaultdict(set)
        for a in actions:by_resource[a.get('resource')].add(a.get('action'))
        conflicts=[k for k,v in by_resource.items() if len(v)>1]
        return {'status':'HOLD' if conflicts else 'PASS','conflicts':conflicts,'policy':'deny-on-conflict'}
    if op=='human_approval':
        a=p.get('approval',{});valid=isinstance(a,dict) and bool(a.get('human_signed')) and bool(a.get('actor')) and bool(a.get('scope'))
        return {'status':'PASS' if valid else 'HOLD','approved':valid,'note':'signature authenticity not verified; authorization never inferred'}
    if op=='multiagent_policy':
        policies=p.get('policies',{}); results=[]
        for a in _records(p):
            allowed=a.get('permission') in policies.get(a.get('agent'),[])
            results.append({'agent':a.get('agent'),'permission':a.get('permission'),'allowed':allowed})
        return {'status':'PASS','decisions':results,'default_deny':True}
    if op=='narrative_continuity':
        lines=_records(p); ids={r.get('id') for r in lines};bad=[r.get('id') for r in lines if r.get('depends_on') and r['depends_on'] not in ids]
        return {'status':'PASS' if not bad else 'HOLD','unresolved_dependencies':bad,'semantic_truth_verified':False}
    if op=='editorial_integrity':
        before=p.get('before','');after=p.get('after','')
        return {'status':'PASS' if before==after else 'HOLD','source_sha256':sha(before.encode()),'result_sha256':sha(after.encode()),'unchanged':before==after}
    if op=='auxiliary_lift':
        kernel=[[_finite_num(v) for v in row] for row in p.get('transition',[])]
        if not kernel or len(kernel)!=len(kernel[0]) or any(len(r)!=len(kernel) for r in kernel):raise ValueError('finite square transition kernel required')
        normalized=all(all(v>=0 for v in row) and abs(sum(row)-1)<1e-9 for row in kernel)
        vector=[_finite_num(v) for v in p.get('state',[])]
        if len(vector)!=len(kernel):raise ValueError('state length mismatch')
        nxt=[sum(vector[i]*kernel[i][j] for i in range(len(vector))) for j in range(len(vector))]
        return {'status':'PASS' if normalized else 'HOLD','next_state':nxt,'stochastic':normalized,'finite_only':True,'physical_claim':False}
    if op=='evidence_schema':
        rows=_records(p);bad=[i for i,r in enumerate(rows) if not all(r.get(k) for k in ['id','source_sha256','kind']) or not re.fullmatch('[0-9a-f]{64}',str(r.get('source_sha256','')))]
        return {'status':'PASS' if not bad else 'HOLD','bad_rows':bad,'checked':len(rows),'evidence_truth_verified':False}
    if op=='evidence_registry':
        rows=_records(p);db={};conflict=[]
        for r in rows:
            key=str(r.get('id',''))
            if key in db and db[key]!=r:conflict.append(key)
            db.setdefault(key,r)
        return {'status':'HOLD' if conflict else 'PASS','unique_rows':len(db),'conflicting_ids':sorted(set(conflict))}
    if op=='claim_gate':
        claims=_records(p);checks=[]
        for c in claims:
            ok=bool(c.get('evidence_ids')) and bool(c.get('independent_verification')) and bool(c.get('rights_approved'))
            checks.append({'claim_id':c.get('id'),'allowed':ok})
        return {'status':'PASS' if all(q['allowed'] for q in checks) else 'HOLD','decisions':checks,'default_deny':True}
    if op=='classification_benchmark':
        pairs=_records(p);tp=fp=fn=tn=0
        for r in pairs:
            truth=bool(r.get('truth'));pred=bool(r.get('prediction'))
            if truth and pred:tp+=1
            elif not truth and pred:fp+=1
            elif truth and not pred:fn+=1
            else:tn+=1
        return {'status':'PASS','tp':tp,'fp':fp,'fn':fn,'tn':tn,'precision':tp/(tp+fp) if tp+fp else None,'recall':tp/(tp+fn) if tp+fn else None,'data_kind':'synthetic_fixture_only'}
    if op=='cross_domain_overlap':
        a=set(p.get('train_sha256',[]));b=set(p.get('test_sha256',[]));overlap=sorted(a&b)
        return {'status':'PASS' if not overlap else 'HOLD','overlap':overlap,'n_train':len(a),'n_test':len(b),'domain_transfer_proven':False}
    if op=='source_catalog':
        rows=_records(p);return {'status':'PASS','entries':[{'path':r['path'],'sha256':r['sha256']} for r in rows if r.get('path') and r.get('sha256')],'note':'indexes supplied manifests; never claims to have scanned remote storage'}
    if op=='archive_indexer':
        rows=_records(p);unsafe=[r.get('path') for r in rows if '..' in pathlib.PurePosixPath(r.get('path','')).parts or r.get('path','').startswith('/')]
        return {'status':'HOLD' if unsafe else 'PASS','unsafe_paths':unsafe,'entries':len(rows),'note':'validates supplied archive inventory'}
    if op=='provenance_deduper':
        rows=_records(p);groups=defaultdict(list)
        for r in rows:groups[r.get('source_sha256')].append(r.get('id'))
        dup={k:v for k,v in groups.items() if k and len(v)>1}
        return {'status':'PASS' if not dup else 'HOLD','duplicate_groups':dup,'leakage_risk':bool(dup)}
    if op=='reproducibility_cli':
        rows=_records(p);bad=[r['path'] for r in rows if r.get('expected_sha256')!=r.get('actual_sha256')]
        return {'status':'PASS' if not bad else 'FAIL','mismatches':bad,'checked':len(rows)}
    if op=='ci_acceptance':
        rows=_records(p);blocked=[r.get('gate') for r in rows if r.get('status')!='PASS']
        return {'status':'PASS' if not blocked else 'HOLD','failed_or_unverified_gates':blocked,'checked':len(rows)}
    if op=='rights_privacy_audit':
        names=[str(r.get('path','')) for r in _records(p)];pat=re.compile(r'(^|/)(\.env|id_rsa|.*private.*key|.*patient.*|.*credential.*|.*token.*)(/|$)',re.I)
        flagged=[n for n in names if pat.search(n)]
        return {'status':'HOLD','sensitive_path_candidates':flagged,'rights_owner_approval':'UNVERIFIED','automatic_grant':False}
    if op=='dataset_split_audit':
        rows=_records(p);groups=defaultdict(set)
        for r in rows:
            for key in ('subject','source_sha256','near_duplicate_group'):
                if r.get(key):groups[(key,str(r[key]))].add(r.get('split'))
        leaks=[{'key':k[0],'value':k[1],'splits':sorted(v)} for k,v in groups.items() if len(v)>1]
        return {'status':'HOLD' if leaks else 'PASS','leakage':leaks,'checked':len(rows)}
    if op=='hf_card_generator':
        title=str(p.get('title','Unverified model'))
        return {'status':'HOLD','draft':f'---\\nlicense: other\\n---\\n# {title}\\n\\n> LICENSE NOT DETERMINED. Rights/weights/test status require independent owner verification.\\n','license_verified':False,'note':'not a publishing approval'}
    if op=='release_registry':
        rows=_records(p); statuses={str(r.get('code')):str(r.get('status')) for r in rows}
        return {'status':'PASS','targets':statuses,'approved_public_count':sum(v=='PUBLIC_APPROVED_AND_VERIFIED' for v in statuses.values()),'note':'input statuses untrusted without independent receipts'}
    raise ValueError('unknown tool operation: '+op)



DEFAULT_OPERATION = 'release_registry'
# Release engineering input contracts. No new scientific claims are introduced.
_base_operate = operate
_RECORD_OPS = {
 'checkpoint_replay','finite_oracles','provenance_chain','conflict_resolution',
 'multiagent_policy','narrative_continuity','evidence_schema','evidence_registry',
 'claim_gate','classification_benchmark','source_catalog','archive_indexer',
 'provenance_deduper','reproducibility_cli','ci_acceptance','rights_privacy_audit',
 'dataset_split_audit','release_registry'}
_REQUIRED = {
 'synthetic_distributed_bench':['replicas','dropped'], 'finite_recoverability':['hex'],
 'side_information_limits':['alternatives'],'exact_fallback':['original_hex','candidate_hex'],
 'fault_injection':['hex','position'],'replicated_recovery':['replicas'],
 'nondestruction':['before','after'],'authority_graph':['edges'],
 'role_delegation':['grantor_permissions','requested_permissions'],
 'human_approval':['approval'],'editorial_integrity':['before','after'],
 'auxiliary_lift':['transition','state'],'cross_domain_overlap':['train_sha256','test_sha256'],
 'hf_card_generator':['title']}

def _text(v, name):
    if not isinstance(v,str) or not v.strip(): raise ValueError(name+' must be a nonempty string')
    return v

def _list(v, name, allow_empty=False):
    if not isinstance(v,list) or len(v)>10000 or (not v and not allow_empty):
        raise ValueError(name+' must be a bounded list'+('' if allow_empty else ' with entries'))
    return v

def _hex(v, name):
    if not isinstance(v,str) or not re.fullmatch(r'(?:[0-9a-fA-F]{2})*',v):
        raise ValueError(name+' must be even-length hexadecimal without whitespace')

def _digest(v, name):
    if not isinstance(v,str) or not re.fullmatch(r'[0-9a-f]{64}',v):
        raise ValueError(name+' must be a lowercase SHA-256 digest')

def _safe_inventory_path(v):
    if not isinstance(v,str) or not v or '\\' in v or ':' in v or '\x00' in v: return False
    parts=v.split('/')
    if any(not s or s in ('.','..') or s.endswith((' ','.')) for s in parts): return False
    reserved={'CON','PRN','AUX','NUL'}|{'COM'+str(i) for i in range(1,10)}|{'LPT'+str(i) for i in range(1,10)}
    return not any(s.split('.')[0].upper() in reserved for s in parts)

def operate(op,p):
    if not isinstance(p,dict): raise ValueError('input must be a JSON object')
    if op not in _RECORD_OPS and op not in _REQUIRED: raise ValueError('unknown tool operation: '+str(op))
    # Reject NaN/Infinity, circular objects and excessively large direct-library calls too.
    if len(json.dumps(p,allow_nan=False))>1048576: raise ValueError('input exceeds 1 MiB')
    for key in _REQUIRED.get(op,[]):
        if key not in p: raise ValueError('missing required field: '+key)
    rows=[]
    if op in _RECORD_OPS:
        rows=_list(p.get('records'),'records')
        if any(not isinstance(r,dict) for r in rows): raise ValueError('each record must be an object')
    if op=='synthetic_distributed_bench':
        vals=_list(p['replicas'],'replicas');drops=_list(p['dropped'],'dropped',True)
        if any(type(i) is not int or i<0 or i>=len(vals) for i in drops): raise ValueError('invalid dropped replica index')
    if op in ('finite_recoverability','fault_injection'): _hex(p['hex'],'hex')
    if op=='fault_injection' and type(p['position']) is not int: raise ValueError('position must be an integer')
    if op=='side_information_limits' and (type(p['alternatives']) is not int or p['alternatives']<1):
        raise ValueError('alternatives must be a positive integer')
    if op=='exact_fallback':
        _hex(p['original_hex'],'original_hex');_hex(p['candidate_hex'],'candidate_hex')
    if op=='replicated_recovery':
        _list(p['replicas'],'replicas')
        for v in p['replicas']: _hex(v,'replica')
        p=dict(p,replicas=[v.lower() for v in p['replicas']])
    if op=='nondestruction':
        if not isinstance(p['before'],dict) or not p['before'] or not isinstance(p['after'],dict):
            raise ValueError('nonempty before and object after manifests required')
    if op=='finite_oracles':
        if any('expected' not in r or 'observed' not in r for r in rows): raise ValueError('oracle fields missing')
    if op=='authority_graph':
        edges=_list(p['edges'],'edges');graph=defaultdict(set);degree={}
        for edge in edges:
            if not isinstance(edge,list) or len(edge)!=2: raise ValueError('edge must be a pair')
            a,b=(_text(edge[0],'authority'),_text(edge[1],'authority'))
            degree.setdefault(a,0);degree.setdefault(b,0)
            if b not in graph[a]:graph[a].add(b);degree[b]+=1
        pending=[n for n,d in degree.items() if d==0];visited=0
        while pending:
            n=pending.pop();visited+=1
            for v in graph[n]:
                degree[v]-=1
                if degree[v]==0:pending.append(v)
        cycle=visited!=len(degree)
        return {'status':'HOLD' if cycle else 'PASS','cycle_detected':cycle,'edge_count':len(edges),'authentication_verified':False}
    if op=='role_delegation':
        for key in ('grantor_permissions','requested_permissions'):
            for v in _list(p[key],key,True): _text(v,key)
    if op=='human_approval':
        a=p['approval']
        if not isinstance(a,dict): raise ValueError('approval must be an object')
        supplied=(a.get('human_signed') is True and isinstance(a.get('actor'),str) and bool(a['actor'].strip())
                  and isinstance(a.get('scope'),str) and bool(a['scope'].strip()))
        return {'status':'HOLD','approved':False,'complete_attestation_supplied':supplied,
                'reason':'SIGNATURE_AUTHENTICITY_NOT_VERIFIED','note':'JSON fields cannot grant real authorization'}
    if op=='conflict_resolution':
        for r in rows:_text(r.get('resource'),'resource');_text(r.get('action'),'action')
    if op=='multiagent_policy':
        if not isinstance(p.get('policies'),dict): raise ValueError('policies must be an object')
        for actor,perms in p['policies'].items():
            _text(actor,'agent')
            for v in _list(perms,'permissions',True):_text(v,'permission')
        for r in rows:_text(r.get('agent'),'agent');_text(r.get('permission'),'permission')
    if op=='narrative_continuity':
        ids=[_text(r.get('id'),'id') for r in rows]
        if len(ids)!=len(set(ids)): return {'status':'HOLD','reason':'DUPLICATE_IDS'}
        parent={r['id']:r.get('depends_on') for r in rows}
        for start in parent:
            seen=set();n=start
            while n in parent and parent[n]:
                if n in seen:return {'status':'HOLD','reason':'DEPENDENCY_CYCLE','semantic_truth_verified':False}
                seen.add(n);n=parent[n]
                if not isinstance(n,str):raise ValueError('depends_on must be a string')
    if op=='editorial_integrity':
        if not all(isinstance(p[k],str) for k in ('before','after')): raise ValueError('text strings required')
    if op=='auxiliary_lift':
        v=_list(p['state'],'state');_list(p['transition'],'transition')
        if any(_finite_num(x)<0 for x in v) or abs(sum(v)-1)>1e-9: raise ValueError('state must be a probability vector')
    if op in ('evidence_schema','evidence_registry','provenance_deduper'):
        for r in rows:_text(r.get('id'),'id');_digest(r.get('source_sha256'),'source_sha256')
    if op=='claim_gate':
        decisions=[]
        for r in rows:
            _text(r.get('id'),'claim id')
            for name in ('independent_verification','rights_approved'):
                if type(r.get(name)) is not bool: raise ValueError(name+' must be a boolean')
            ids=_list(r.get('evidence_ids'),'evidence_ids',True)
            for v in ids:_text(v,'evidence id')
            decisions.append({'claim_id':r['id'],'criteria_declared':bool(ids) and r['independent_verification'] and r['rights_approved'],'allowed':False})
        return {'status':'HOLD','decisions':decisions,'default_deny':True,'reason':'ATTESTATIONS_NOT_INDEPENDENTLY_VERIFIED'}
    if op=='classification_benchmark':
        if any(type(r.get(k)) is not bool for r in rows for k in ('truth','prediction')):
            raise ValueError('truth and prediction must be JSON booleans')
    if op=='cross_domain_overlap':
        for k in ('train_sha256','test_sha256'):
            for v in _list(p[k],k):_digest(v,k)
    if op=='source_catalog':
        for r in rows:_text(r.get('path'),'path');_digest(r.get('sha256'),'sha256')
    if op=='archive_indexer':
        unsafe=[r.get('path') for r in rows if not _safe_inventory_path(r.get('path'))]
        return {'status':'HOLD' if unsafe else 'PASS','unsafe_paths':unsafe,'entries':len(rows),'archive_opened':False}
    if op=='reproducibility_cli':
        for r in rows:
            _text(r.get('path'),'path');_digest(r.get('expected_sha256'),'expected_sha256');_digest(r.get('actual_sha256'),'actual_sha256')
    if op=='ci_acceptance':
        for r in rows:_text(r.get('gate'),'gate');_text(r.get('status'),'status')
    if op=='dataset_split_audit':
        for r in rows:
            _digest(r.get('source_sha256'),'source_sha256')
            if r.get('split') not in ('train','validation','test'):raise ValueError('invalid split')
            for k in ('subject','near_duplicate_group'):
                if k in r:_text(r[k],k)
    if op=='hf_card_generator':
        title=_text(p['title'],'title').replace('\r',' ').replace('\n',' ')
        return {'status':'HOLD','draft':'---\ntags:\n- research\n---\n# '+title+'\n\nRights and license remain unresolved.\n',
                'license_verified':False,'note':'No license declaration is fabricated'}
    if op=='release_registry':
        for r in rows:_text(r.get('code'),'code');_text(r.get('status'),'status')
        ids=[r['code'] for r in rows]
        if len(ids)!=len(set(ids)):return {'status':'HOLD','reason':'DUPLICATE_CODES'}
        return {'status':'PASS','targets':{r['code']:r['status'] for r in rows},'approved_public_count':0,
                'declared_public_count':sum(r['status']=='PUBLIC_APPROVED_AND_VERIFIED' for r in rows),'note':'Source declarations are not authenticated approvals'}
    result=_base_operate(op,p)
    result['scope']='bounded_offline_computation_not_independent_validation'
    return result


def main(argv=None):
    import argparse
    q=argparse.ArgumentParser(description='Bounded offline utility; no public release or scientific approval')
    q.add_argument('--input',required=True)
    args=q.parse_args(argv)
    try:
        f=pathlib.Path(args.input)
        if f.stat().st_size>1048576: raise ValueError('input exceeds 1 MiB')
        payload=json.loads(f.read_text('utf-8'),parse_constant=lambda x:(_ for _ in ()).throw(ValueError('Nonfinite JSON constant: '+x)))
        result=operate(DEFAULT_OPERATION,payload)
    except (OSError,ValueError,TypeError,KeyError,IndexError,OverflowError,RecursionError) as exc:
        result={'status':'FAIL','error':str(exc)}
    print(json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True,allow_nan=False))
    return {'PASS':0,'FAIL':1,'HOLD':2}.get(result.get('status'),2)

if __name__=='__main__':sys.exit(main())
