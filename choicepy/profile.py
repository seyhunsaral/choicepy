import choicepy as cp
import random


class Profile():

    def __init__(self, voters=None):
        self.voters = voters
        if voters:
            self.num_voters = len(self.voters)
            self.candidates = sorted(self.voters[0])
            self.num_candidates = len(self.candidates)
        else:
            self.num_voters = 0
            self.candidates = None
            self.num_candidates = 0

    def __getitem__(self, voter_no):
        return self.voters[voter_no]

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.num_voters:
            next_voter = self.voters[self.n]
            self.n += 1
            return next_voter
        else:
            raise StopIteration

    def __eq__(self, other):
        # equality check
        if isinstance(other, list):
            return self.voters == other

        if isinstance(other, Profile):
            return self.voters == other.voters

    def __str__(self):
        if self.voters:
            size_string = os.popen('stty size', 'r').read()
            term_rows, term_columns = list(map(int, (size_string.split())))

            max_length = len(max(self.voters[0], key=len))
            justify_length = max_length + 3

            voters_printable = str(self.num_candidates) \
                + " candidates, " + str(self.num_voters) \
                + " voters \n"

            voters_printable += "Profile: " + str(self.print_summary()) + "\n"
            voters_printable += "\n"
            if self.num_voters * justify_length <= term_columns:
                voters_printable += self.profile_string_full()
            else:
                voters_printable += """omitting full print due to terminal size.
                use .print_full() to print the full profile"""

            return voters_printable
        else:
            return "Empty profile"

    def __repr__(self):
        return self.__str__()

    def profile_string_full(self):

        max_length = len(max(self.voters[0], key=len))
        justify_length = max_length + 3

        profile_string = "".join([("[" + str(item) + "]").ljust(justify_length)
                                  for item in range(self.num_voters)])
        profile_string += "\n"
        for i in range(self.num_candidates):
            for j in range(self.num_voters):
                profile_string += self.voters[j][i].ljust(justify_length)
            profile_string += "\n"

        return profile_string

    def print_full(self):
        print(self.profile_string_full)

    def set_voters(self, voter_list):
        self.voters = voter_list
        self.num_voters = len(self.voters)
        self.set_candidates(sorted(self.voters[0]))

    def set_candidates(self, candidates):
        if isinstance(candidates, list):
            self.candidates = sorted(candidates)
        elif isinstance(candidates, float) or isinstance(candidates, int):
            self.candidates = cp.get_lexicographic_list(candidates)
        self.num_candidates = len(self.candidates)

    def gen_uniform_voters(self, candidate_list, num_voters):
        self.num_voters = num_voters
        self.set_candidates(candidate_list)
        self.voters = [random.sample(self.candidates, len(self.candidates))
                       for _ in range(num_voters)]

    def gen_mallows_voters(self,
                           candidate_list,
                           num_voters,
                           dispersion_parameter,
                           transformation_parameter=0):

        self.num_voters = num_voters
        self.set_candidates(candidate_list)
        orders, probs, _ = gen_trans_mallows_culture(candidate_list,
                                                     dispersion_parameter,
                                                     transformation_parameter)
        np_orders = np.array(orders)
        self.voters = np_orders[np.random.choice(len(orders),
                                                 num_voters,
                                                 p=probs)].tolist()

    def gen_mistaken_truth_voters(self, candidate_list, num_voters, stdev):
        self.num_voters = num_voters
        self.set_candidates(candidate_list)

        new_voters = []
        for v in range(num_voters):
            norms = np.array(list(range(len(candidate_list)))) \
                + np.random.normal(0, stdev, len(candidate_list))

            norm_ranks = calculate_rank(norms)
            new_voter = np.take(candidate_list, norm_ranks)
            new_voters.append(list(new_voter))
        self.voters = new_voters

    def create_voter_permutations(self, with_myself=False):
        permutation_list = []
        voter_permutations = list(itertools.permutations(self.voters))
        unique_voter_permutations = filter_unique(voter_permutations)
        for p in unique_voter_permutations:
            if not list(p) == self.voters or with_myself:
                permutation_list.append(Profile(list(p)))
        return permutation_list

    def rename_candidates(self, dictionary):
        # I used this numpy implementation because I had it already.
        # Later we should decide if we'd like to switch to numpy
        voters = np.array(self.voters)
        new_voters = np.copy(voters)
        for i in range(np.shape(voters)[0]):
            for j in range(np.shape(voters)[1]):
                new_voters[i, j] = dictionary[voters[i, j]]
        return new_voters.tolist()

    def create_candidate_permutations(self, with_myself=False):
        permutation_list = []

        candidate_permutations = []
        mappings = create_all_mappings(self.candidates)

        for m in mappings:
            candidate_permutations.append(self.rename_candidates(m))

        unique_candidate_permutations = filter_unique(candidate_permutations)

        for p in unique_candidate_permutations:
            if not list(p) == self.voters or with_myself:
                permutation_list.append(Profile(list(p)))
        return permutation_list

    def create_vc_permutations(self, with_myself=False):
        # Combination of both. First gets voters perms then candidate
        permutation_list = []
        final_list = []
        voter_permutations = list(itertools.permutations(self.voters))
        unique_voter_permutations = filter_unique(voter_permutations)

        for p in unique_voter_permutations:
            permutation_list.append(Profile(list(p)))

        for profile in permutation_list:
            final_list.extend(profile.create_candidate_permutations())

        return permutation_list + final_list

    def get_voter(self, voter_index):
        return self.voters[voter_index]

    def get_voters(self, concentrate=False):
        if concentrate:
            return convert_condensed(self.voters)
        else:
            return self.voters

    def summarize_voters(self):
        return dict(Counter(convert_condensed(self.voters)))

    def print_summary(self):
        summary = self.summarize_voters()
        sortedkeys = sorted(summary, key=str.lower)
        sortedlist = [k + ":" + str(summary[k]) + " | " for k in sortedkeys]
        return "".join(sortedlist)

    def dictator(self, dictator_index=None):
        # print(self.num_voters)
        if dictator_index is not None:
            if dictator_index <= self.num_voters:
                return self.voters[dictator_index][0]
            else:
                print("Invalid dictator index")
                return None
        else:
            return list(self.voters[random.randrange(self.num_voters)][0])

    def plurality(self):
        top_votes = [self.voters[i][0] for i in range(self.num_voters)]
        return cp.mode(top_votes)

    def majority(self):
        winners = []
        top_votes = [self.voters[i][0] for i in range(self.num_voters)]
        counts = Counter(top_votes)
        plurality_winner = max(counts)
        if counts[plurality_winner] >= (0.5 * self.num_voters):
            winners.append(plurality_winner)

        return winners

    def approval(self, acceptable_rank=None):

        if acceptable_rank is None:
            acceptable_rank = [random.randint(1, self.num_candidates - 1)
                               for _ in range(self.num_voters)]
        else:
            acceptable_rank = [acceptable_rank] * self.num_voters

        approved_candidates = [self.voters[i][0:acceptable_rank[i]]
                               for i in range(self.num_voters)]
        approvals = [j for i in approved_candidates for j in i]  # concatenate

        return mode(approvals)

    def condorcet(self):
        pairwise_comp_matrix = np.zeros((self.num_candidates,
                                         self.num_candidates))

        for voter in self.voters:
            for can1 in range(len(self.candidates)):
                for can2 in range(len(self.candidates)):
                    if can1 == can2:
                        pairwise_comp_matrix[can1, can2] = np.nan
                    else:
                        comparison = int(voter.index(self.candidates[can1])
                                         < voter.index(self.candidates[can2]))

                        pairwise_comp_matrix[can1, can2] += comparison

        pairwise_positive_matrix = pairwise_comp_matrix - self.num_voters / 2

        winners = []

        for c, candidate in enumerate(self.candidates):

            if np.all(np.delete(pairwise_positive_matrix[c, :], c) > 0):
                winners.append(candidate)
        # print(pairwise_comp_matrix)
        return winners

    def gen_borda_rule(self, point_distribution):
        """
        This function gets a string and returns the corresponding list of
        points used in the Borda-count rule.
        :param point_distribution: string, valid inputs:
          "borda_0",
          "borda_1",
          "dowdall"
        :return: a list
            -"borda_0": returns [n-1,n-2,...,0]
            -"borda_1": returns [n,n-1,...,1]
            -"dowdall": returns [1, 1/2, 1/3, ..., 1/n]
            (n = len(self.candidates))
        """
        if point_distribution == "borda_0":
            points_list = [len(self.candidates) - i
                           for i in range(1, len(self.candidates) + 1)]

        elif point_distribution == "borda_1":
            points_list = [len(self.candidates) - i
                           for i in range(0, len(self.candidates))]

        elif point_distribution == "dowdall":
            points_list = [1 / i for i in range(1, len(self.candidates) + 1)]
        return points_list

    def borda(self, points_list=None):
        """
        Elects a winner according to the weighted rankings of the voters.
        :param points_list: a list (for example the output of
        gen_borda_rule(self, point_distribution))
        :return: a string (the name of the winner of the election)
        """

        voters = np.array(self.voters)
        if points_list is None:
            points_list = self.gen_borda_rule("borda_0")

        cumulated = Counter(voters[:, 0])
        for key in cumulated:
            cumulated[key] *= points_list[0]
        for v in range(1, len(voters[0][:])):
            count = Counter(voters[:, v])
            for key in count:
                count[key] *= points_list[v]
            cumulated += count
        max_value = max(cumulated.values())
        return sorted(key for key, value in cumulated.items()
                      if value == max_value)

    def elect(self, rule):
        if rule == "dictator":
            return self.dictator()

        if rule == "condorcet":
            return self.condorcet()

        if rule == "approval":
            return self.approval()

        if rule == "plurality":
            return self.plurality()

        if rule == "borda":
            return self.borda()
