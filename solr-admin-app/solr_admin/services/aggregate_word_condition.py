from solr_admin.models.virtual_word_condition import VirtualWordCondition


def aggregate(query):
    data = list()
    previous_word_condition = None
    for row in query:
        rwc, rc, rw = row
        word_condition = VirtualWordCondition(
            cnd_id=rwc.cnd_id,
            word_id=rwc.word_id,
            rc_consenting_body=rc.consenting_body,
            rc_words=rw.word_phrase,
            rc_condition_text=rc.cnd_text,
            rc_instructions=rc.instructions
        )
        if previous_word_condition is None or word_condition.cnd_id != previous_word_condition.cnd_id:
            data.append(word_condition)
            previous_word_condition = word_condition
        else:
            previous_word_condition.rc_words += ', ' + rw.word_phrase

    return data
