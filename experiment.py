import psynet.experiment
from psynet.page import InfoPage, UnityPage
from psynet.timeline import (
    Timeline, 
    join,
)
from psynet.trial.static import (
    StaticNode, 
    StaticTrial, 
    StaticTrialMaker,
)
from psynet.utils import get_logger

logger = get_logger()


class UnityTestPage(UnityPage):  # derived from UnityQuestionPage
    def __init__(
        self,
        message: str,
        time_estimate: int,
    ):
        data = {
            "goal": "This is the goal",
            "gain": "This is the rule",
        }
        super().__init__(
            title="Unity test",
            resources="/static",
            contents=data,  # json.dumps(contents),
            debug=False,
            time_estimate=time_estimate,
            session_id="1",  # customize it -- trigger for unity to do stuff ; also can use the type
            game_container_width="960px",
            game_container_height="600px"
        )


class UnityTestTrialMaker(StaticTrialMaker):
    pass


class UnityTestTrial(StaticTrial):
    time_estimate = 5
    accumulate_answers = True

    def show_trial(self, experiment, participant):
        return join(
            InfoPage(
                "Here we go!",
                time_estimate=10,
            ),
            UnityTestPage(
                message="Helo world!",
                time_estimate=10,
            ),
        )


class Exp(psynet.experiment.Experiment):
    label = "Unity demo"
    initial_recruitment_size = 1

    timeline = Timeline(
        UnityTestTrialMaker(
            id_="unity_test",
            trial_class=UnityTestTrial,
            nodes=[
                StaticNode(definition={'test': "ok"})
            ],
            expected_trials_per_participant=1,
            max_trials_per_participant=1,
        ),
    )