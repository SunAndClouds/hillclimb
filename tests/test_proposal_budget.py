from hillclimb import Budget,Config
from hillclimb.harness.loop import Loop
from hillclimb.sdk import Action
from hillclimb.agents.fake import FakeAgent
from tests.harness_factory import make_harness


class Fill(Loop):
    def run(self,harness):
        while harness.capacity:
            assert not harness.submit(Action('draft')).rejected
        while harness.inflight:harness.wait()


def test_pending_and_failed_proposals_reserve_the_cap(task,config):
    config.concurrency.parallel_agents=4
    config.budget.max_proposals=2
    agent=FakeAgent()
    for _ in range(4):agent.queue(result={'ok':False,'error_kind':'error','error_message':'fixture failure'})
    harness,_,_=make_harness(task,config,agent)
    harness.execute(Fill())
    assert len(agent.requests)==harness.spend().proposals==2
    assert harness.spend().evaluations==0
    assert harness.view().budget.proposals_remaining==0
    assert harness.closed_reason=='proposal budget spent'


def test_proposal_budget_is_recorded_for_resume():
    cfg=Config()
    assert Budget(proposals=20).apply(cfg)==['budget.max_proposals=20']
    assert cfg.budget.max_proposals==20
