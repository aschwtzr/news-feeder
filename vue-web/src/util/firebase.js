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

export const addSource = (source) => {
  return firebase.database().ref('sources/').set({
    description: source.description,
    id: source.id,
  });
};

// export default { getSources, addSource };
