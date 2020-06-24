from google.cloud import firestore

# Project ID is determined by the GCLOUD_PROJECT environment variable
db = firestore.Client()
def get_default_sources():
    sources_ref = db.collection(u'sources')
    docs = sources_ref.stream()
    res = {}
    for doc in docs:
        res[doc.id] = doc.to_dict()
    return res

def get_user_sources():
    sources_ref = db.collection(u'userSources')
    docs = sources_ref.stream()
    res = {}
    for doc in docs:
        res[doc.id] = doc.to_dict()
    return res
