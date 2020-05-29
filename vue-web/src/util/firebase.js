import firebase from 'firebase';

const db = firebase.firestore();

// function writeUserData(userId, name, email, imageUrl) {
//     firebase.database().ref('users/' + userId).set({
//       username: name,
//       email: email,
//       profile_picture : imageUrl
//     });
//   }

export const createUser = (user) => {
  db.collection('users').doc(user.uid).set({
    name: user.displayName,
    email: user.email,
  });
};

export const getUserProfile = (user) => {
  // const db = firebase.firestore();
  const userRef = db.collection('users').doc(user.uid);
  userRef.get().then((doc) => {
    if (doc.exists) {
      console.log('user exists');
    } else {
      createUser(user);
    }
  });
};

export const getUserPreferences = (userId) => {
  // const db = firebase.firestore();
  return new Promise((resolve, reject) => {
    const preferencesRef = db.collection('users').doc(userId).collection('preferences');
    preferencesRef.get().then((preferences) => {
      if (preferences.exists) {
        resolve(preferences);
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
