from hamcrest import *
from solr_admin.services.get_stems import get_stems, get_stems_url


def test_explore_stem_url():
    synonym_list = 'construction, constructing, development'
    url = get_stems_url(synonym_list)

    assert_that(url, equal_to('https://namex-solr-dev.pathfinder.gov.bc.ca/solr/possible.conflicts/analysis/field?analysis.fieldvalue=construction,%20constructing,%20development&analysis.fieldname=name&wt=json&indent=true'))


def test_stem_several_worlds():
    synonym_list = 'construction, constructing, development'
    stems = get_stems(synonym_list)

    assert_that(stems, equal_to('construct, develop'))