from google.cloud import firestore

# Project ID is determined by the GCLOUD_PROJECT environment variable
db = firestore.Client()
def get_default_sources():
    sources_ref = db.collection(u'sources')
    docs = sources_ref.stream()
    res = []
    for doc in docs:
        if doc.id != 'custom-google':
            source = {
                "id": doc.id,
            }
            source.update(doc.to_dict())
            res.append(source)
    return res