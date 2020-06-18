import firebase from 'firebase';

export const createUser = (user) => {
  const db = firebase.firestore();
  db.collection('users').doc(user.uid).set({
    name: user.displayName,
    email: user.email,
  });
};

export const getUserProfile = (userId) => {
  const db = firebase.firestore();
  return new Promise((resolve, reject) => {
    const preferencesRef = db.collection('users').doc(userId);
    preferencesRef.get().then((user) => {
      if (user.exists) {
        resolve(user.data());
      } else reject(new Error('No preferences'));
    }).catch((error) => {
      reject(error);
    });
  });
};

export const getSources = () => {
  return firebase.database().ref('/sources/').once('value').then((snapshot) => {
    console.log(snapshot);
  });
};

export const updateUserSources = (sources, userId) => {
  const db = firebase.firestore();
  const userSourcesRef = db.collection('users').doc(userId);

  return db.runTransaction((transaction) => {
    debugger;
    return transaction.get(userSourcesRef).then((userDoc) => {
      if (!userDoc.exists) {
        console.log('user does not exist.');
      }
      console.log(sources);
      transaction.update(userSourcesRef, { sources });
    });
  }).then(() => {
    console.log('Transaction successfully committed!');
  }).catch((error) => {
    console.log('Transaction failed: ', error);
  });
};

// export default { getSources, addSource };
