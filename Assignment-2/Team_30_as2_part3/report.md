# Assignment 2 Part-3 | Machine Data Learning

## Team 30:

### Anvita Reddy :2019115009
### Stella Sravanthi: 2019101101

> Procedure of making A matrix
- Firstly the dimensions are
    + rows: no.of states that is calculated on creating MDP that is Union of position, material, arrows, state and MM's health which are of size 5,3,4,2,5. **5 * 3 * 4 * 2 * 5** = **600** states
    + columns: The number of coloumns for the matrix A is equal to the number of (STATE, ACTION) pairs that are possible in the MDP. 
    Eg: mat_a11,mat_a12,mat_a12,mat_21,mat_a22 ... Where each (mat_xy) describes the action y taken in state x. which is **1936**
- And the values are probabilities of that state-action pair
- Here the valid actions and correct probabilites are allowed.
- Thus on subtracting the probabilities of  incoming edges into  a state and adding the probabilities of outgoing edges.
- The "NONE" action is filled with probability *1.0*
> Explain procedure of finding the policy and analyze the results.
- Objective function was :   **objective = cp.Maximize(cp.matmul(mat_r, x))**
Thus resultin the optimal policy for the MDP  with maximum reward 
- The different matrices in this are:<br>
 -> The A matrix <br>
-> The R array <br>
-> The alpha array<br>
-> The optimised x array
Also the using the Bellmann equation we know that :

    Vi < = [ R ( I , A ) + \gamma  * \sigma P ( J | I , A ) *Vj ]

Therefore, there were two  constraints:
constraints = [
        cp.matmul(mat_a, x) == mat_alp,
        x >= 0
    ]
    One for showing consistency of solution with the initial condition and the other is non-negative one which says there can't be negative action taken place.
> Can there be multiple policies? Why? What changes can you make in your
code to generate another policy? 
- Yes
- On altering the reward/step-cost/penalty for each state 
This results in a reaching the terminal state faster (if change is more reward)
- Different start states
 It definelty results in different policy and thus diferent alpha vector.
 
