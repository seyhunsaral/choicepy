import choicepy

my_profile = choicepy.Profile()
my_profile.generate_mallows_voters(list("abcd"), 5, 1, 0)
print(my_profile.borda([4, 3, 2, 1]))
print(my_profile.borda(my_profile.generate_borda_rule("borda_1")))
print(my_profile.borda(my_profile.generate_borda_rule("borda_0")))
print(my_profile.borda(my_profile.generate_borda_rule("dowdall")))
my_profile.generate_uniform_voters(list("abcd"),3)


my_profile.set_candidates(50)
print(my_profile.candidates)
my_profile.set_candidates(list("abcdefghi"))
print(my_profile.candidates)