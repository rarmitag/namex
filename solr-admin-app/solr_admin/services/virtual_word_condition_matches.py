def record_matches(virtual_word_condition_record, search):
    keep_candidate = False
    terms = search.split(' ')
    for term in terms:
        keep_candidate = keep_candidate or term in virtual_word_condition_record.rc_consenting_body
        keep_candidate = keep_candidate or term in virtual_word_condition_record.rc_words

    return keep_candidate
