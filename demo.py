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
    print 'Searching ... for cities renowned for passions:', ', '.join(passions_to_search)
    print 'Top ', maximum_results_number, ' recommended cities with score and total endorsement: '
    # Maximum number of results is 10
    recommended_cities = search_engine.search(passions_to_search, maximum_results_number)
    print('---------------------------------------------------------------')
    print '%-20s%-20s%-20s' % ('City', 'Score', 'Endorsement Count')
    print('---------------------------------------------------------------')
    for d in recommended_cities:
        print '%-20s%-20s%-20s' % (d[0].title(), d[1]['score'], d[1]['total'])
    print('---------------------------------------------------------------\n\n')
