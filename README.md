[![PyPI version](https://badge.fury.io/py/choicepy.svg)](https://badge.fury.io/py/choicepy)
# choicepy
A python module for social choice

**Creators**: Annika Hennes & Ali Seyhun Saral 

**Warning**: This package is at an early stage. Please use with caution. 

## Installation
The package can be installed via the package manager pip:
```bash
pip install choicepy
```

## Available voting rules
- dictator rule
- plurality rule
- majority rule
- approval rule
- Condorcet rule
- Borda rule

## Initialization
First, generate a profile:

```python
import choicepy

my_profile = choicepy.Profile()
```

### Voters
Voters are represented by their preferences over the candidates, i.e. an electorate
is a list of lists. Every inner list represents a voter and the elements in this
list are the candidates sorted according to the preference of the voter. We support the case where voters have strict and complete preferences over candidates.

#### Custom Voter preferences
You can set the voters using the method set_voters.
```python
my_profile.set_voters([["a", "b", "c"], ["b", "c", "a"]])
print(my_profile.voters)
print(my_profile.candidates)
```
Output:
```bash
[['a', 'b', 'c'], ['b', 'c', 'a']]
['a', 'b', 'c']
```
#### Generate Voters from uniform distribution
The voters can also be automatically generated according to a uniform distribution over all possible profiles 
on a given set of candidates. 
You need to specify the list of candidates and the number of voters first and then call the following method:
```python
gen_uniform_voters(self, candidate_list, num_voters)
```
#### Generate Voters according to Mallows Phi-Model 
If there exists an underlying truth which all the voters want to achieve as the outcome of the voting procedure
but do not know yet   
In some cases, there exists an underlying truth (reference ranking) which is not known to the voters but all voters agree to 
have as the outcome of their election. But the voters might not be completely clueless and have a rough idea how the
true ranking is looking, some of them more, some less.
Such a situation can be modeled using the Mallows phi-model.

```python
gen_mallows_voters(self, candidate_list, num_voters, dispersion_parameter, transformation_parameter=0)
```
The ```dispersion_paramater``` takes a value in the interval (0,1] and determines how clueless the voters are. 
The lower the value of ```dispersion_parameter```, the higher the probability that a voter has the reference ranking as
her own preference. As ```dispersion_parameter``` approaches 0, the probability of seeing the reference ranking 
approaches 1, for ```dispersion_parameter = 1```, the Mallows phi-model is equivalent to a uniform distribution over
all rankings.
    
### Candidates
After initializing the voters, the candidates do not need to be specified.
They will be automatically read from the voters preferences.

### Voting rules

#### dictator rule
The winning alternative is the top preference of one single designated voter.
```bash
dictator(self, dictator_index=None)
```
With ```dictator_index``` it can be specified which voter will be the designated one. 
If this parameter is not set, a voter will be chosen uniformly at random.

#### plurality rule
The winning alternative is the one that the greatest fraction of voters ranked on top of their preferences.
It does not need to be unique.

```bash
plurality(self)
```

#### majority rule
The winning alternative is the one that the majority of voters (i.e. at least 50%) ranked on top of their preferences.
It does not need to be unique.

```bash
majority(self)
```

#### approval rule
Every voter can either approve or disapprove any candidate. 
The winning alternative is then the candidate that is approved by most of the voters.
Just as for the other rules, the voters preferences will be represented by ordered lists 
of alternatives. All candidates up to a certain index will be approved, 
the rest will be disapproved.

```bash
approval(self, acceptable_rank=None)
```

With ```acceptable_rank``` you can specify the index up to which candidates are approved. 
If this parameter is not set, an index will be generated uniformly at random 
for every voter independently.

#### Condorcet rule
The winning alternative is the candidate that wins against every other candidate 
in pairwise comparisons.
```bash
condorcet(self)
```

#### Borda rule
Every preference of a voter is assigned a score. 
The winning alternative is the candidate with the highest sum of scores.
```bash
borda(self, points_list=None)
```
The parameter ```points_list``` specifies the scoring. It takes a list of length n, where n is the 
number of alternatives. The elements in this list represent the numerical weights the preferences will get, 
starting with the top-ranked alternative.
It can be either set manually by specifying a list of numerical values of length n or using the output of 
the following method:

```bash
gen_borda_rule(self, point_distribution)
```
The parameter ```point_distribution``` can be set to one of the following strings 
indicating the scoring method:
1) ```"borda_0"``` generates the scoring [n-1, n-2, ..., 1, 0] (this scoring is used by default).
2) ```"borda_1"``` generates the scoring [n, n-1, ..., 2, 1].
3) ```"dowdall``` generates the scoring [1, 1/2, 1/3, ..., 1/n].

If it is not set, the default scoring [n-1,n-2,...,0] is used, where n is the number of alternatives.

## Example 

```
import choicepy

# Create a new profile
my_profile = choicepy.Profile()

# Generate voters from unform distribution 
my_profile.gen_uniform_voters(4,9)

# Show profile
print(my_profile)

# 4 candidates, 9 voters 
# Profile: abcd:1 | abdc:1 | acbd:1 | adbc:1 | bacd:1 | bcad:1 | bdac:1 | cbad:1 | dcba:1 | 
# 
# [0] [1] [2] [3] [4] [5] [6] [7] [8] 
# d   a   b   a   c   b   a   a   b   
# c   b   a   d   b   c   c   b   d   
# b   d   c   b   a   a   b   c   a   
# a   c   d   c   d   d   d   d   c   

# Show Borda outcome
my_profile.borda()
# ['b']

# Show Plurality outcome
my_profile.plurality()
# ['a']

# Show Condorcet outcome
my_profile.condorcet()
# ['b']

# Show Approval voting outcome (voters approve first two candidates in their preference ordering)
my_profile.approval(2)
# ['b']

# Show Approval voting outcome (voters approve the first n of the candidates while n is determined randomly between 1 and number_of_candidates - 1)
my_profile.approval()
# ['a','b']
```
