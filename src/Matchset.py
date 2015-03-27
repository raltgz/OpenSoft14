'''
    Represents the Matching part (Result of Match Function)
'''

from Fragment import Fragment

class Matchset:
    fragment_1= Fragment() # Contour Fragment 1  
    fragment_2= Fragment() # Contour Fragment 2
    match_1_start=0
    match_1_end=0
    match_2_end=0
    match_2_start=0
    match_1=Fragment()
    match_2=Fragment()
    i=0
    j=0
    score=0 # Matching Score
    
    
    
    