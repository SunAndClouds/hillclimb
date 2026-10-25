from types import SimpleNamespace
from hillclimb.modules.tuners.base import Observation, history_for


def test_validation_objectives_reach_tuner_without_holdout():
    trial=SimpleNamespace(index=0,params={'x':1},val_score=0.8,metrics={'empirical_msle':0.2,'robust_upper':4.0},holdout_score=-999)
    history=history_for(SimpleNamespace(trials=[trial]),pending=[{'x':2}])
    assert history[0].metrics==trial.metrics and history[0].metrics is not trial.metrics
    assert not hasattr(history[0],'holdout_score')
    assert history[1].pending and history[1].metrics=={}
    assert Observation(params={},score=1.).metrics=={}
