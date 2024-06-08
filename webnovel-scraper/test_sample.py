import pandas as pd
import core
import helpers


def test_answer():

    websites = core.initiateClasses()
    print(websites)
    assert len(websites) == 2
    novels = core.searchWebsites(websites, "martial world")
    if len(novels) == 0:
        return 0
    assert len(novels) == 3

    novel = novels[0]
    assert type(novel) == pd.Series

