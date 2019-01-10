from solr_admin.models.restricted_word import RestrictedWord
from solr_admin.models.restricted_word_condition import RestrictedWordCondition


def replace_word_condition(session, cnd_id, rc_words):
    try:
        result = session.query(RestrictedWordCondition.word_id).filter_by(cnd_id=cnd_id).all()
        for row in result:
            (word_id, ) = row
            session.query(RestrictedWord).filter_by(word_id=word_id).delete()
        session.query(RestrictedWordCondition).filter_by(cnd_id=cnd_id).delete()

        words = rc_words.split(',')
        for word in words:
            session.begin_nested()
            restricted_word = RestrictedWord(word_phrase=word.strip())
            session.add(restricted_word)
            session.commit()
            word_id = restricted_word.word_id

            session.add(RestrictedWordCondition(cnd_id=cnd_id, word_id=word_id))

        session.commit()
    except Exception:
        session.rollback()