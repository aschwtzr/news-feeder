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

def get_custom_feeds():
    sources_ref = db.collection(u'customFeeds')
    docs = sources_ref.stream()
    res = {}
    for doc in docs:
        res[doc.id] = doc.to_dict()
    return res

def get_users():
    users_ref = db.collection(u'users')
    docs = users_ref.stream()
    res = {}
    for doc in docs:
        res[doc.id] = doc.to_dict()
    return res