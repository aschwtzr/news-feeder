import firebase from 'firebase';

export const setUserSources = (sources, userId) => {
  const db = firebase.firestore();
  const userRef = db.collection('users').doc(userId);

  return db.runTransaction((transaction) => {
    return transaction.get(userRef).then((userDoc) => {
      if (!userDoc.exists) {
        console.log('user does not exist.');
      }
      console.log(sources);
      transaction.update(userRef, { sources });
    });
  }).then(() => {
    console.log('Transaction successfully committed!');
  }).catch((error) => {
    console.log('Transaction failed: ', error);
  });
};

export const setBriefingIsActive = (briefingIsActive, userId) => {
  const db = firebase.firestore();
  const userRef = db.collection('users').doc(userId);

  return db.runTransaction((transaction) => {
    return transaction.get(userRef).then((userDoc) => {
      if (!userDoc.exists) {
        console.log('user does not exist.');
      }
      transaction.update(userRef, { briefingIsActive });
    });
  }).then(() => {
    console.log('Transaction successfully committed!');
  }).catch((error) => {
    console.log('Transaction failed: ', error);
  });
};

export const setBriefingFrequency = (briefingFrequency, userId) => {
  const db = firebase.firestore();
  const userRef = db.collection('users').doc(userId);

  return db.runTransaction((transaction) => {
    return transaction.get(userRef).then((userDoc) => {
      if (!userDoc.exists) {
        console.log('user does not exist.');
      }
      transaction.update(userRef, { briefingFrequency });
    });
  }).then(() => {
    console.log('Transaction successfully committed!');
  }).catch((error) => {
    console.log('Transaction failed: ', error);
  });
};

export const setArticleLimit = (articleLimit, userId) => {
  const db = firebase.firestore();
  const userRef = db.collection('users').doc(userId);
  return db.runTransaction((transaction) => {
    return transaction.get(userRef).then((userDoc) => {
      if (!userDoc.exists) {
        console.log('user does not exist.');
      }
      transaction.update(userRef, { articleLimit });
    });
  }).then(() => {
    console.log('Transaction successfully committed!');
  }).catch((error) => {
    console.log('Transaction failed: ', error);
  });
};

export const setAlternateEmail = (alternateEmail, userId) => {
  const db = firebase.firestore();
  const userRef = db.collection('users').doc(userId);
  return db.runTransaction((transaction) => {
    return transaction.get(userRef).then((userDoc) => {
      if (!userDoc.exists) {
        console.log('user does not exist.');
      }
      transaction.update(userRef, { alternateEmail });
    });
  }).then(() => {
    console.log('Transaction successfully committed!');
  }).catch((error) => {
    console.log('Transaction failed: ', error);
  });
};

export const setShowKeywords = (showKeywords, userId) => {
  const db = firebase.firestore();
  const userRef = db.collection('users').doc(userId);

  return db.runTransaction((transaction) => {
    return transaction.get(userRef).then((userDoc) => {
      if (!userDoc.exists) {
        console.log('user does not exist.');
      }
      transaction.update(userRef, { showKeywords });
    });
  }).then(() => {
    console.log('Transaction successfully committed!');
  }).catch((error) => {
    console.log('Transaction failed: ', error);
  });
};

export const createCustomFeed = (feedDescription, feedKeywords, userId) => {
  const db = firebase.firestore();
  const batch = db.batch();
  return new Promise((resolve, reject) => {
    const feedRef = db.collection('customFeeds').doc();
    batch.set(feedRef, {
      description: feedDescription,
      keywords: feedKeywords,
    });
    const userRef = db.collection('users').doc(userId);
    batch.update(userRef, { customFeeds: firebase.firestore.FieldValue.arrayUnion(feedRef.id) });
    batch.commit().then(resolve(feedRef)).catch(error => reject(error));
  });
};
