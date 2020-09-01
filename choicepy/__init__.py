import itertools
import os
import random
import string
from collections import Counter

import numpy as np
from choicepy.profile import Profile

def get_lexicographic_list(n):
    """
    get_lexicographic_list(n)

    Returns a list that contains the first n lexicographically ordered strings
        ["a", "b", "c", ..., "z", "aa", "ab", "ac", ...]

    Parameters
    ----------
    n: int
       number of strings

    Returns
    -------
    list

    Example
    -------
    get_lexicographic_list(3) # returns ['a','b','c']
    """
    repetitions = range(n // 26 + 2)
    candidate_tuples = itertools.chain.from_iterable(itertools.product(
        string.ascii_lowercase, repeat=r) for r in repetitions)
    return list(map(lambda x: "".join(x), candidate_tuples))[1:n + 1]


def mode(elements):
    """
    mode(elements)

    Returns the elements with highest number of occurrence.


    Parameters
    ----------
    elements: list
        a list of elements to be counted

    Returns
    -------
    list

    Example
    -------
    a = [1,1,2,3,3]
    mode(a) # returns [1,3]
    """
    if not isinstance(elements, list):
        raise TypeError("Not a list")

    if not elements:
        raise ValueError("Empty list provided")

    counts = Counter(elements)
    max_value = max(counts.values())
    return sorted(key for key, value in counts.items() if value == max_value)


def compare(numA, numB):
    """
    compare(numA, numB):

    Compares two numbers. Returns:
        1,  if the first number is greater than the second,
        0,  if they are equal,
       -1, if the first number is smaller than the second.

    Parameters
    ----------
    numA: integer or float
    numB: integer of float

    Returns
    -------
    integer

    """
    if numA > numB:
        return 1
    if numA < numB:
        return -1
    if numA == numB:
        return 0


def ranking_distance(rnkA, rnkB, method="kendalltau"):
    """
    Calculates the distance between two rankings

    """

    available_methods = {"kendalltau"}

    if method not in available_methods:
        raise ValueError(""" methods: please choose correct measure. \n
                         Available measures: """ + str(available_methods))

    candidates = sorted(rnkA)
    pairwise_comparisons = itertools.combinations(candidates, 2)

    if method == "kendalltau":
        distance = 0
        for c1, c2 in pairwise_comparisons:
            compA = compare(rnkA.index(c1), rnkA.index(c2))
            compB = compare(rnkB.index(c1), rnkB.index(c2))

            if compA != compB:
                distance += 1
        return distance


# kendall tau
# stackexchange
# https://stats.stackexchange.com/questions/168602/whats-the-kendall-taus-distance-between-these-2-rankings


def calculate_rank(vector):
    a = {}
    rank = 0
    for num in sorted(vector):
        if num not in a:
            a[num] = rank
            rank = rank + 1
    return [a[i] for i in vector]


def convert_condensed(voters):
    """
    This functions gets a list of voters and convert in each voter preferences
    in condensed string form.

    Example:
    list_of_voters = [["a","b","c","d"],["b","a","c","d"]]

    convert_condensed(list_of_voters)
    ## Output: ['abcd', 'bacd']
    """
    return ["".join(voter) for voter in voters]


# This is nice, it might be useful
# list(itertools.combinations(list("abcd"),4))


def all_preferences(candidates, concentrate=False):
    """
    Generates all possible preferences given a list of candidates
    """
    permutations_tuple = list(itertools.permutations(candidates))
    permutations_list = list(map(list, list(permutations_tuple)))
    if concentrate:
        return convert_condensed(permutations_list)
    else:
        return permutations_list


def all_profiles(candidates, num_voters):
    profile_list = []
    prefs = all_preferences(candidates)
    profile_feed = list(itertools.product(prefs, repeat=num_voters))

    for p in profile_feed:
        profile_list.append(Profile(list(p)))

    return profile_list


def filter_unique(voterlist):
    unique_voter_list = []

    for v in voterlist:
        if v not in unique_voter_list:
            unique_voter_list.append(v)

    return unique_voter_list


def append_to_profile_list(profile, profile_list):
    for p in profile_list:
        if p == profile:
            return

    profile_list.append(profile)


def filter_unique_profile(profile_list):
    new_profile_list = []

    for p in profile_list:
        append_to_profile_list(p, new_profile_list)

    return new_profile_list


def remove_if_exists(profile, profile_list):
    try:
        profile_list.remove(profile)
    except TypeError:
        pass


def print_profile_list(profile_list):
    for p in profile_list:
        p.print_full()


def gen_mallows_culture_old(true_ordering,
                            sigma,
                            distance_weight=1,
                            concentrate=False):

    preferences = all_preferences(true_ordering, concentrate=concentrate)
    kemeny_distances = np.array([ranking_distance(p, true_ordering)
                                 for p in preferences])
    kemeny_distances_weighted = kemeny_distances ** distance_weight
    probabilities = (1 / (kemeny_distances_weighted *
                          sum(kemeny_distances_weighted))) * (1 - sigma)
    probabilities[
        kemeny_distances_weighted == 0] = sigma  # replace the zero distance
    # ordering with sigma (assuming there is only one)
    return [list(preferences), list(probabilities)]


def get_mallows_normalization_constant(number_of_alternatives,
                                       dispersion_parameter):
    # Normalization constant is Z.
    normalization_constant = 1
    for j in range(1, number_of_alternatives):
        dispersionoverdistance = [dispersion_parameter ** j
                                  for j in range(0, j + 1)]
        sum_of_dispersionoverdistance = sum(dispersionoverdistance)
        normalization_constant *= sum_of_dispersionoverdistance
    return normalization_constant


# def get_transformed_mallows_normalization_constant(number_of_alternatives,
#                                                    dispersion_parameter,
#                                                    transformation_parameter):
#    # Normalization constant is Z.
#    normalization_constant = 1
#    for j in range(1,number_of_alternatives+1):
#        dispersionoverdistance = [dispersion_parameter ** (j **
#        np.exp(transformation_parameter)) for j in range(0,j)]
#        sum_of_dispersionoverdistance = sum(dispersionoverdistance)
#        normalization_constant *= sum_of_dispersionoverdistance
#    return normalization_constant

def get_transformed_mallows_normalization_constant(dispersion_parameter,
                                                   transformation_parameter,
                                                   kemeny_distances):
    normalization_constant = sum(
        dispersion_parameter ** (k ** np.exp(transformation_parameter))
        for k in kemeny_distances)
    return normalization_constant


def mallows_pdf(distance, number_of_alternatives, dispersion_parameter):
    likelihood = dispersion_parameter ** distance
    probability = likelihood / get_mallows_normalization_constant(
        number_of_alternatives,
        dispersion_parameter)

    return probability


def transformed_mallows_pdf(distance, number_of_alternatives,
                            dispersion_parameter, transformation_parameter,
                            kemeny_distances):

    likelihood = dispersion_parameter ** (distance **
                                          np.exp(transformation_parameter))

    normalization_constant = get_transformed_mallows_normalization_constant(
        dispersion_parameter,
        transformation_parameter,
        kemeny_distances)

    probability = likelihood / normalization_constant

    return probability


def gen_mallows_culture(reference_rank,
                        dispersion_parameter,
                        concentrate=False):

    number_of_alternatives = len(reference_rank)
    preferences = all_preferences(reference_rank, concentrate=concentrate)
    kemeny_distances = np.array([ranking_distance(p, reference_rank)
                                 for p in preferences])
    probabilities = [mallows_pdf(d,
                                 number_of_alternatives,
                                 dispersion_parameter)
                     for d in kemeny_distances]

    return [list(preferences), list(probabilities), list(kemeny_distances)]


def gen_trans_mallows_culture(reference_rank,
                              dispersion_parameter,
                              transformation_parameter=0,
                              concentrate=False):

    number_of_alternatives = len(reference_rank)
    preferences = all_preferences(reference_rank, concentrate=concentrate)
    kemeny_distances = np.array([ranking_distance(p, reference_rank)
                                 for p in preferences])

    probabilities = [transformed_mallows_pdf(d,
                                             number_of_alternatives,
                                             dispersion_parameter,
                                             transformation_parameter,
                                             kemeny_distances)
                     for d in kemeny_distances]

    return [list(preferences), list(probabilities), list(kemeny_distances)]


def make_dictionary(pref1, pref2):
    return dict(zip(pref1, pref2))


def create_all_mappings(candidates):
    # This creates al mappings from candidate lists.
    # I will use it to generate candidate permutations
    all_prefs = all_preferences(candidates)
    list_of_mappings = []

    for p in all_prefs:
        list_of_mappings.append(make_dictionary(candidates, p))

    return list_of_mappings

