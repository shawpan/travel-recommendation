from __future__ import division
import operator
import math

class SearchEngine:
   """ Search engine class for getting recommended destinations

   Attributes:
        db_path: file path where the databse is
        city_passion_matrix: endorsement count of any (city, passion) pair
        theshold: Minimum endorsement count for any entry to be considered
   """

   def __init__(self, db_path, theshold):
      """ Initialize SearchEngine with preprocessing.

      Construct city_passion_matrix from databse and minimum endorsement count.
      Then calculate and store total endorsement count per city

      Args:
        db_path: Path to databse file
        theshold: Minimum endorsement count for any entry to be considered
      """
      self.db_path = db_path
      self.city_passion_matrix = {}
      self.theshold = theshold

      with open(self.db_path, 'r') as db:
          for line in db:
              [d, p, c] = line.split(' ')
              # Sanitize city, passion and endorsement count values
              d = d.lower().replace(' ', '_')
              p = p.lower().replace(' ', '_')
              c = int(c)
              # If endorsement count is less than threshold then discard
              if c < self.theshold:
                  continue

              if d.lower() in self.city_passion_matrix:
                  self.city_passion_matrix[d.lower()][p.lower()] = c
              else:
                  self.city_passion_matrix[d.lower()] = {p.lower():c}

      # Calculate total endorsement count per city
      self.total_endorsement_per_city = {}
      for d in self.city_passion_matrix:
          self.total_endorsement_per_city[d] = 0
          for p in self.city_passion_matrix[d]:
              self.total_endorsement_per_city[d] += self.city_passion_matrix[d][p]

   def search(self, passions, number_of_results):
       """ Search for cities matching passions.

       Find the cities that can be recommended for the intended passions

       Args:
            passions: List of passions
            number_of_results: Maximum number of recommended cities
       Returns:
            A list of dict of the recommended cities with scores. For
           example:
           [('amsterdam', {'total': 229764, 'score': 0.04536310939409803}), ('lisboa', {'total': 157659, 'score': 0.011013345324424639})]
       """

       # Sanitize spaces with -
       passions = [p.lower().replace(' ', '_') for p in passions]
       cities_with_scores = {}

       for d in self.city_passion_matrix:
           # Initialize score of cities for the passions
           cities_with_scores[d] = { 'score': 0.0, 'total': self.total_endorsement_per_city[d]};
           # Score of d for given passions is the multiplication of individual values
           for p in passions:
               # If passion does not exist then endorsement_count is 1 to avoid zeroth bias,
               # otherwise stored value
               if p in self.city_passion_matrix[d]:
                   endorsement_count = self.city_passion_matrix[d][p]
               else:
                   endorsement_count = 1
               cities_with_scores[d]['score'] += math.log((endorsement_count / (self.total_endorsement_per_city[d] + 1.0)) )

       # Sort the cities in descending order of relavency score; use total endorsement count to break tie
       sorted_cities_with_scores = sorted(cities_with_scores.items(), key= lambda x: (x[1]['score'], x[1]['total']), reverse=True)

       return sorted_cities_with_scores[:number_of_results]
