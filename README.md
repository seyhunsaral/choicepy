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


