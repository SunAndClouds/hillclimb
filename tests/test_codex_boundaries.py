import json,tomllib
from hillclimb.agents.base import AgentRequest
from hillclimb.agents.codex_cli import CodexCliAgent
from hillclimb.harness.sandbox import SandboxPolicy

def test_native_fork_effort_and_evidence_boundaries(tmp_path):
    private=tmp_path/'private';data=tmp_path/'data';work=tmp_path/'candidate'
    request=AgentRequest(operator='improve',prompt='fixture',candidate_dir=work,timeout_s=300,
        model='gpt-6.1-sol#high',allow_internet=False,resume_session_id='parent',fork_session=True,
        sandbox=SandboxPolicy(read_only=(str(data),),deny_read=(str(private),)))
    cmd=CodexCliAgent()._command(request,{})
    assert cmd[cmd.index('--model')+1]=='gpt-6.1-sol'
    assert 'model_reasoning_effort="high"' in cmd
    assert '--sandbox' not in cmd and '--ignore-user-config' in cmd
    assert cmd[-5:]==['fork','--json','--skip-git-repo-check','parent','-']
    config=tomllib.loads('\n'.join(cmd[i+1] for i,x in enumerate(cmd) if x=='-c'))
    fs=config['permissions']['hillclimb']['filesystem']
    assert fs[str(private)]=='deny' and fs[str(data)]=='read' and fs[':root']=='deny'
    assert config['permissions']['hillclimb']['network']['enabled'] is False
