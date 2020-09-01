import choicepy

my_profile = choicepy.Profile()

my_profile.set_voters([["a", "b", "c"], ["a", "c", "b"], ["c", "b", "a"]])


def test_plurality():
    assert my_profile.plurality() == ['a']
