# probabilistic-random-surfer

In the classical [random surfer model](https://www.cs.cmu.edu/~avrim/Papers/webgraph.pdf), The choice of the next "surf" node / link is performed with a uniform distribution. i.e., the link probabilities in the webpage are chosen with uniform probabilities. This is a strong assumption that doesn't necessarily hold in practice. In this project, we propose a few methods for computing out links probabilities. Those methods have to be efficient and fast, because the random surfer algorithm is usually ran on large amounts of web data. 

## Quickstart:

TODO python env installation, etc.

## Usage examples:

* Print & save the XML db for a given site:

`python surf.py --save-html --save-xml --url https://en.wikipedia.org/wiki/Random_surfing_model --only-print`

* Print out link probabilities for a given site, with uniform probabilities:

`python surf.py --url https://en.wikipedia.org/wiki/Random_surfing_model --strategy uniform`

This is equivalent to the naive approach in the classical random surfer model.

#### Use XPath expressions to select a subset of the db:

* Select all links under 'head', give each one uniform probability:

`python surf.py --url https://en.wikipedia.org/wiki/Random_surfing_model --strategy uniform --xpath /html/head`

* Select all links under div's which have an attribute of 'class' which is equal to 'mw-body-content':

`python surf.py --url https://en.wikipedia.org/wiki/Random_surfing_model --strategy uniform --xpath /html/body//div[@class='mw-body-content']`

> XPath usage could be extremely useful for filtering key parts in large web pages, like headers, div with key classes, footers, etc. 

### Use bottom-up tree automatas to perform complex probability computations:
* Select all links in the header, give them probabilities corresponding to how "deep" they appear in the XML db (See the `ExponentialDepthAutomaton` class for a more in-depth explanation):

`python surf.py --url https://docs.pola.rs/api/python/stable/reference/index.html --strategy automaton --automaton exponential_depth --xpath //header`

You will notice that some links get much higher probabilities, e.g. the home page & docs get the highest probabilities, and twitter / github links get lower probabilities.

* Assume the user is "lazy", and is inclined to choose one of the links appearing first:

`python surf.py --url https://docs.pola.rs/api/python/stable/reference/index.html --strategy automaton --automaton lazy_top_3 --xpath //header`

Compared with the exponential depth automaton, this automaton gives generally higher probabilities for links with probabilities greater than 0, and the probabilities are more varied (for example, unlinkely to see 300 links each with probability 0.00333333).

Although it's true the automata presented here are quite simple, they demonstrate the flexibility and expressive power provided with using bottom-up tree automata.


## Theoretical automata definition
In order to make bottom up tree automatas work in this project, we use a slightly different notation for them. We define a non-deterministic tree automaton as a set $(\Sigma, Q, \Delta)$ where $\Sigma$ is our fixed alphabet of all possible urls (represented as a string), $Q$ is a set of states defined by the automaton, and $\Delta: (\Sigma \times [Q, ...])\rightarrow Q$ is a state transition function for nodes, mapping a node with any given number of children states $[0, \infty)$ to a new state $Q$ in a non-deterministic manner (for leaves, this function is just called with 0 children states instead of defining another $\Delta_0$ or $\Delta$ _leaf function). For optimization purposes, the automaton actaully returns a list of possible output states instead of choosing one randomly.

Since the objective of the automatas is to return possible out link urls, the automatas have no notion of "accepting states", thus we have no need of defining a set of accepting states $F$. Furthermore, the most generic state set definition for url's is a basic string, we implement automata states via a simple string. This allows each automaton to choose whatever url state set it wants, without being restricted.

Because the automatas $\Delta$ returns a list of states instead of a single state in a non-deterministic manner, we can actually extract an exact url probability map by running the automaton only once. This is a big improvement over trivial Monte-Carlo sampling, since if we would implement MC, we would have to run the automaton a large number of times only to get an approximation for the url probabilities.

## Automatons implemented in this work
### **ExponentialDepthAutomaton**

The exponential depth automaton assumes links which appear in more global, "shallow" nodes in the XML tree are more likely to be surfed to. The automaton defines the state set $Q$ as all mappings between strings and floats, resembling link probabilities. It implements $\Delta$ by giving equal weights to its direct children, resulting in an exponential decay in probabilities for its descendents, depending on their relative depth from the root node.

### **LazyTop3Automaton**

The lazy top 3 automaton assumes the user is inclined to choose links which appear first, because he sees that first. Selects the first link with probability 0.5, the 2nd with 0.3, and 3rd with 0.2. Links appearing with children index 4+ have probability 0, since they are too far away. In case a given XML node has less than 3 children, the probabilities are normalized so that their sum is equal to 1. For example, with 2 children, the probabilities are normalized by 0.5+0.3=0.8.

## Implementation & usage of custom automatons:
1. To implement a new automaton, create a class that derives from `BottomUpTreeAutomaton` and implement the abstract `delta()` $\Delta: (\Sigma \times [Q, ...])\rightarrow Q$, the state transition method. See `ExponentialDepthAutomaton` for an example. After implementation, add an alias mapping to your automaton type in `automata/__init__.py`.
2. If you want to implement a custom state set $Q$ for your automaton, create a custom state class that derives from `AutomataNodeState`.
3. Run the automaton: (replace `exponential_depth` by your automaton alias)
`python surf.py --url https://en.wikipedia.org/wiki/Random_surfing_model --strategy automaton --automaton exponential_depth`

## Suggested URL list to test this project on:
```
https://en.wikipedia.org/wiki/Random_surfing_model
https://en.wikipedia.org/wiki/XPath
https://readspike.com/
https://lobste.rs/
https://www.nytimes.com/timeswire
https://www.newsinlevels.com/
https://docs.pola.rs/api/python/stable/reference/index.html
```