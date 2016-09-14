# Travel Recommender System -- Prototype
|  City |  Passion |  Endorsement Count |
|---|---|---|
|  Amsterdam |Nightlife   | 24234  |
|   Amsterdam  |  Shopping |   25756|
|  Paris |Museums   | 84569  |
|   Paris  |  Sightseeing |   63457|
### Problem
  Given a data table such as above, find the top cities recommended for a set of passions.
  ### Demo
  ```sh
  $ python demo.py
  ```
  ### Example
  ```python
  from SearchEngine import SearchEngine

# Minimum endorsement count is 10
minimum_endorsement_count = 10
# Maximum results to fetch
maximum_results_number = 2
search_engine = SearchEngine('db.dat', minimum_endorsement_count)
test_cases = [['Museums'], ['Architecture', 'Wine'], ['Architecture', 'Wine', 'Museums']]

for test_number,test_case in enumerate(test_cases):
    print 'Test Case ', test_number + 1
    passions_to_search = test_case
    print 'Searching ... for cities reknowned for passions:', ', '.join(passions_to_search)
    print 'Top ', maximum_results_number, ' recommended cities with score and total endorsement: '
    # Maximum number of results is 10
    recommended_cities = search_engine.search(passions_to_search, maximum_results_number)
    print('---------------------------------------------------------------')
    print '%-20s%-20s%-20s' % ('City', 'Score', 'Endorsement Count')
    print('---------------------------------------------------------------')
    for d in recommended_cities:
        print '%-20s%-20s%-20s' % (d[0].title(), d[1]['score'], d[1]['total'])
    print('---------------------------------------------------------------\n\n')

  ```
  ### Output
```sh
Searching ... for cities renowned for passions: Architecture, Wine, Museums
Top  2  recommended cities with score and total endorsement:
--------------------------------------------
City       Score           Endorsement Count   
--------------------------------------------
Amsterdam  -16.2505820028  292170              
Paris      -17.1135017718  500121              
---------------------------------------------
```
### Algorithm Steps
- Remove entries having endorsement count less than defined threshold. This will discard premature and irrelevant entries such as users giving wrong endorsements as jokes.
- Sanitize city and passion strings
- Prepare a city-passion matrix that stores endorsement count per (city, passion) pair.
- Prepare total-endorsement-per-city matrix holding the total endorsement count so far of that city.
- For a set of passions, for each city, calculate the fraction of endorsement using city-passion matrix for each passion and multiply these values for all passion items in the set of given passions. To avoid zeroth bias add 1 in both the nominator and denominator. Also since the multiplication of fractions will produce very small number, change the calculation in log scale i.e., use sum of log values instead of product of original values. Thus a recommendation score will be calculated for each city having the given passions.
- Sort the cities according to decreasing values of recommendation score, if two cities have similar recommendation value take the one with larger endorsement count.
- Return the top n results
### Explanation
- For a combined search such as Architecture and Wine, simple approach like summing up the endorsement count will be biased to extreme values. Instead if we take the product of endorsement fractions it will rank the city that satisfies all required passions best not best on some passions. Taking the product is also meaningful if we consider the problem in a probabilistic perspective e.g., city Amsterdam is good for Nightlife with probability 0.7 and Museum with probability 0.6. Then the combination is naturally derived from the joint probability.
- Taking the fraction instead of endorsement counts also helps to avoid "Popularity Bias" and since we discarded premature entries having endorsement count less than minimum threshold, this ensures that (city, passion) pairs that do not have enough feedback will not corrupt cities with sufficient endorsements. Furthermore, if two cities have the same score then the city with more endorsements will be chosen first.
### Improvement
- If it is possible to partition endorsement counts into user specific endorsements, then we can get another user-passion matrix which can be used to run collaborative filtering approach. This will help to generate more relevant results. `scikit-learn` is a good choice as helping tool to build the collaborative filtering approach.
- Input passion strings should go through a transformation such that query strings of passions should be transformed to known words of the system thus allowing synonyms, typos and use of close representatives for missing passions. This code is written in python so `nltk` and `wordnet` will be two good choices for these NLP tasks.  
