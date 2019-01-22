import json
from urllib import request


def get_stems(synonym_list):

    query = get_stems_url(synonym_list)

    processed_words = json.load(request.urlopen(query))
    count = 0
    for item in processed_words['analysis']['field_names']['name']['index']:
        if item == 'org.apache.lucene.analysis.snowball.SnowballFilter':
            count += 1
            break
        count += 1

    processed_list = []
    for text in processed_words['analysis']['field_names']['name']['index'][count]:
        processed_list.append(text['text'])

    stems_without_duplicates = list(set(processed_list))
    stems_without_duplicates.sort()

    return ', '.join(stems_without_duplicates)


def get_stems_url(synonym_list):
    solr_base_url = 'https://namex-solr-dev.pathfinder.gov.bc.ca/solr/possible.conflicts/analysis/field?analysis.fieldvalue='
    query = solr_base_url + '{words}&analysis.fieldname=name&wt=json&indent=true'.format(words=synonym_list.strip()).replace(' ', '%20')

    return query