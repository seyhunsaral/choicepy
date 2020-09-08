import choicepy
my_profile = choicepy.Profile()

my_profile.gen_mallows_voters(list("abcd"), 5, 1, 0)
print(my_profile.borda([4, 3, 2, 1]))
print(my_profile.borda(my_profile.gen_borda_rule("borda_1")))
print(my_profile.borda(my_profile.gen_borda_rule("borda_0")))
print(my_profile.borda())
print(my_profile.borda(my_profile.gen_borda_rule("dowdall")))
my_profile.gen_uniform_voters(list("abcd"),3)
#
#

rules = ["dictator", "plurality", "majority", "approval", "condorcet", "borda"]

for rule in rules:
    print(my_profile.elect(rule))
