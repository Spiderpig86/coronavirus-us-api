"""Statistics Test

Statistics unit test.
"""


import pytest

from backend.models.classes.statistics import Statistics


@pytest.mark.parametrize("confirmed, deaths", [(0, 0), (80000, 2000),])
def test__statistics__to_dict__success(confirmed, deaths):
    statistics = Statistics(confirmed, deaths)

    expected_response = {"confirmed": confirmed, "deaths": deaths}

    assert statistics.to_dict() == expected_response
