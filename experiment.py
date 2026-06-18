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
            "coins":"[(10, 10), (20, 20), (30, 10)]"
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

    def metadata(self, **kwargs):
        # UnityPage.metadata() sets time_taken=None, which overwrites the client's value in
        # combined_metadata = {**metadata, **extra_metadata}. Use Unity's value or 0.0.
        out = super().metadata(**kwargs)
        client = kwargs.get("metadata") or {}
        tt = client.get("time_taken")
        out["time_taken"] = 0.0 if tt is None else tt
        logger.info(f"time_taken: {out['time_taken']}")
        return out


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
            # InfoPage(
            #     f"Here are the coins collected: {self.participant.var.coins_collected}",
            #     time_estimate=10,
            # ),
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