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
list are the candidates sorted according to the preference of the voter.
You can set the voters using the method set_candidates.
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
    
### Candidates
After initializing the voters, the candidates do not need to be specified.
They will be automatically read from the voters preferences.

### Voting rules
Decide on a voting rule.

#### dictator rule

#### plurality rule

#### majority rule

#### approval rule

#### Condorcet rule

#### Borda rule


## Example 

```
import choicepy

# Create a new profile
my_profile = choicepy.Profile()

# Generate voters from unform distribution 
my_profile.generate_uniform_voters(4,10)

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
['b']

# Show Approval voting outcome (voters approve a random number between 1 and n-1 in their prefernce ordering)
my_profile.approval()
['a','b']
```
