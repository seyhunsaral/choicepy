import choicepy

my_profile = choicepy.Profile()


def test_uniform_generation_by_number_of_candidates():
    my_profile.gen_uniform_voters(5, 7)
    assert len(my_profile.candidates) == 5
    assert len(my_profile.voters) == 7


def test_uniform_generation_by_list_of_candidates():
    my_profile.gen_uniform_voters(list("abc"), 7)
    assert len(my_profile.candidates) == 3
    assert len(my_profile.voters) == 7
