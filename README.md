[![PyPI version](https://badge.fury.io/py/choicepy.svg)](https://badge.fury.io/py/choicepy)
# choicepy
A python module for social choice

**Creators**: Annika Hennes & Ali Seyhun Saral 

**Warning**: This package is at an early stage. Please use with caution. 


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
