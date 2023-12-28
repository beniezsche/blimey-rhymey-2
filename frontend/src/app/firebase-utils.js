


export function setupFirebase() {
  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
  const firebaseConfig = {
    apiKey: "AIzaSyB3NvCixw8j3Vn5mOk8UxyNGMSQv0E1TuA",
    authDomain: "comini-assignment.firebaseapp.com",
    projectId: "comini-assignment",
    storageBucket: "comini-assignment.appspot.com",
    messagingSenderId: "487637604188",
    appId: "1:487637604188:web:deb884d5cd66c312469399",
    measurementId: "G-FF62VBGFQK"
  };

  const app = initializeApp(firebaseConfig);

  const auth = getAuth(app);

}
