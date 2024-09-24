# probabilistic-random-surfer

In the classical [random surfer model](https://www.cs.cmu.edu/~avrim/Papers/webgraph.pdf), when choosing the next node to "surf" to, link probabilities in the webpage are chosen with uniform probabilities. This is a strong assumption that probably doesn't hold in the real world. In this project, we propose a few methods for computing out links probabilities. Those methods have to be efficient and fast, because the random surfer algorithm is usually ran on large amounts of web data. 

### Usage examples:

* Print & save XML db for a given site:
`python surf.py --save-html --save-xml --url https://en.wikipedia.org/wiki/Random_surfing_model --only-print`

* Print out link probabilities for a given site, with uniform probabilities
`python surf.py --url https://en.wikipedia.org/wiki/Random_surfing_model --strategy uniform`

#### Use XPath expressions to select a subset of the db:

* Select all links under 'head', give each one uniform probability:
`python surf.py --url https://en.wikipedia.org/wiki/Random_surfing_model --strategy uniform --xpath /html/body//@class=mw-body-content`

* Select all links under div's which have an attribute of 'class' which is equal to 'mw-body-content':
`python surf.py --url https://en.wikipedia.org/wiki/Random_surfing_model --strategy uniform --xpath /html/body//div[@class='mw-body-content']`

#### Defining and using custom automatons:
1. To implement a new automaton, create a class that derives from `BottomUpTreeAutomaton` and implement the abstract `delta()` method. See `ExponentialDepthAutomaton` for an example. After implementation, add an alias mapping to your automaton type in `automata/__init__.py`.
2. Run it: (replace `exponential_depth` by your automaton alias)
`python surf.py --url https://en.wikipedia.org/wiki/Random_surfing_model --strategy automaton --automaton exponential_depth`

### Defining automatas
In order to make bottom up tree automatas work in this project, we use a slightly different notation for them. We define a non-deterministic tree automaton as a set $(\Sigma, Q, \Delta)$ where $\Sigma$ is our fixed alphabet of all possible urls (represented as a string), $Q$ is a set of states defined by the automaton, and $\Delta: (\Sigma \times [Q, ...])\rightarrow Q$ is a state transition function for nodes, mapping a node with any given number of children states $[0, \infty)$ to a new state $Q$ in a non-deterministic manner (for leaves, this function is just called with 0 children states instead of defining another $\Delta_0$ or $\Delta$ _leaf function). For optimization purposes, the automaton actaully returns a list of possible output states instead of choosing one randomly.

Since the objective of the automatas is to return possible out link urls, the automatas have no notion of "accepting states", thus we have no need of defining a set of accepting states $F$. Furthermore, the most generic state set definition for url's is a basic string, we implement automata states via a simple string. This allows each automaton to choose whatever url state set it wants, without being restricted.

To define a new automaton in the code, TODO

Because the automatas $\Delta$ returns a list of states instead of a single state in a non-deterministic manner, we can actually extract an exact url probability map by running the automaton only once. This is a big improvement over trivial Monte-Carlo sampling, since if we would implement MC, we would have to run the automaton a large number of times only to get an approximation for the url probabilities.


### URLs list this project was tested on:
```
https://en.wikipedia.org/wiki/Random_surfing_model
https://en.wikipedia.org/wiki/XPath
https://readspike.com/
https://lobste.rs/
https://www.nytimes.com/timeswire
https://www.newsinlevels.com/
```