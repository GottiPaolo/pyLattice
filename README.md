# pyLattice

pyLattice is a python library to menage Lattice and PoSet.
I'm a statiscs student, so maybe this not the best programming option but you know


## Structure


- Construct a PoSet
    - main
    - from cover matrix
    - from function
    - operation beetwen PoSet

- Rappresentation
    - hasse: 

- Action on PoSet
    - join
    - meet
    - ...
    - Dedekind completetion

- Lattice object
    - Differences beetwen poset

- Construct a Lattice
    - main
    - Special Lattice
        - Chain
        - Powerset:
            `pl.Lattice.from_power_set(3).hasse(labels = True, shape = (400,300))`
            will return:
        - "cw"
    - from function

- Congruences stuff!
    - Congruence structure
    - Calculate a Con(a,b)
    - Calculate join_irriducible Con
    - Calculate ConL
    - "dinamic con"

## PoSet
A PoSet object has just four different attributes:
- `domination_matrix`: a domination matrix, $Z$ is a squared matrix $n\times n$ where $n$ is the number of element in the PoSet. 
    $$Z_{ij} = 1 \Longleftrightarrow x_i \unlhd x_j;\space 0 \space \text{otherwise} $$
- `cover_matrix`: a cover matrix, $M$,  is a squared matrix $n\times n$ where $n$ is the number of element in the PoSet. 
    $$M_{ij} = 1 \Longleftrightarrow x_i \prec x_j;\space 0 \space \text{otherwise} $$
- `obj`: a list of the object in the PoSet
- `labels`: a list of labels to show in the rappresentation of the PoSet.

### Construct a poset
To construct a PoSet you just need a domination matrix:

```python
P = PoSet(domination_matrix)
```
If you don't specify object and labels they will just be progressive number from $0$ to $n-1$

To define a PoSet there are other ways:

- From a cover matrix:  
    Some times you need to construct a PoSet from just the cover matrix. For example if you hand-draw a PoSet it's fast to manually compute cover matrix then domination matrix.
    For this situation you can just use the `from_cover_matrix` function:
    `P = PoSet.from_cover_matrix(cover_matrix)`

- From a function:  
    You maybe want to create a PoSet from some object and a function to determinate if an element dominate an other. For this you can use `from_function` module:  
    `P = PoSet.from_function(list(range(1,20)), lambda a,b: a%b == 0)`
    You need to pass to elemnt:
    - `X`: Element to compare
    - `f`: function to compare. This function should be to the form: $f(a,b) = True \Leftrightarrow a\unlhd b\space; False \space\text{otehrwise}$  

- From operation beetwen different PoSet (_see later_)

### Operation in a PoSet
With a PoSet you can compute all this operation (_see example file_)
- Chek a domination
- Chek a cover
- Calculate upset and down set of one or more element
- Max and min in a sub set of element
- Join and Meet:
    - If they are not unique and you have specify `force = True` it returns a list of all
    - If they are not unique and you haven't specify `force = True` or it's not define it return `None`
_

### Operation beetwen PoSets
With two or more PoSet you can compute this operation
- Sum: `P + Q`  
    the sum of two (_disjoin_) PoSet $P,Q$ is a PoSet with the union of element as obects and this order rule: $x\unlhd y$ if one and only if one of this occures:
    - $x,y \in P$ and $x\unlhd_P y$
    - $x,y \in Q$ and $x\unlhd_Q y$
    - $x \in P$ and $y\in Q$

- Cartesian product: `P * Q`  
    the cartesian product $P_1 \times P_2$ is an ordered set where the object is the cartesian product of the objec in $P_1,P_2$ ordered by : $(x_1,x_2)\unlhd (y_1,y_2)\Leftrightarrow x_1 \unlhd_1 y_1 \vee x_2 \unlhd_2 y_2  $

### Hasse diagram
You can represent a PoSet by a Hasse diagram.  
To get the Hasse diagram of a PoSet you can just call the function `P.hasse()`. Eventually you can plot multiple hasse diagram.  
`P.hasse(Q,H)` will show a window with all the hasse diagram of $P$, $Q$ adn $H$. You can specify these parameters
- `grid`: tuples of two integers rapresenting the grid for plot multiple hasse. Default is all poset in a single line
- `shape`: tuples of two integers rapresenting the pixels dimention of window, default 500x500
- `radius`: radius of the circles, default 5
- `hasse_mode`: for know you can choose beetwen 5 different modes for an hasse diagram. they're codes just by progressive numbers. (I'm going to implemente more ones in the future)
- `title`: windows title
- `labels`: boolean to show or hide labels
- `t_size`: text size of the labels

Hasse diagram could be ambigous in some situation. Points could allign and looks like there are connection then effictevly there aren't. The best way to improve this problem is to make the graph interactive (later update.)

Know this i possible by using the function `P.rappresenta()` instead  `P.hasse()`. The first one use the `p5` module instead the `tk`. But it could have some serious problem.

## Lattice
The main differences beetwen PoSet and Lattice is that the last ones are algebric structure. Infact in lattice _join_ and _meet_ are **always** defined. The structure of a Lattice module is the same as the PoSet. The difference beetwen the two are in some function and operation 

### Construct a Lattice
There are several ways to construct a Lattice.
Every single one seen for PoSets is still valid. But we have something more:
- Dedekind completion of a PoSet (not implemented yet)
- Built-in function for classic Lattice:
    - `Lattice.from_power_set(n)`: return a Lattice of the powerset of a three elements set order by $\subseteq$
    - `Lattice.from_chain(n)`: return a Lattice of $n$ element where $x_i\unlhd x_j \Longleftrightarrow x\le j$
    - `Lattice.from_cw(*numbers)`: return a Lattice construct as the cartesian product of chains. For example `Lattice.from_cw(3,3,2)` returns a Lattice wich is the same of `Lattice.from_chain(3) * Lattice.from_chain(3) * Lattice.from_chain(2)`
- Moltiplicadion and addition beetwen Lattice return always a Lattice.
- You can convert a PoSet in a Lattice by the confuction `P.as_lattice()`. Be sure that P is actually a Lattice with the command `P.is_lattice()`.
- Be very careful to construct a Lattice. The program never check thata the domination matrix is actually the domination matrix of a Lattice.


### Congruences
One of the most important properties of a Lattice is the Congruence.