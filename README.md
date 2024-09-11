# probabilistic-random-surfer

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


### URLs list this project was tested on:
```
https://en.wikipedia.org/wiki/Random_surfing_model
https://en.wikipedia.org/wiki/XPath
https://readspike.com/
https://lobste.rs/
https://www.nytimes.com/timeswire
https://www.newsinlevels.com/
```