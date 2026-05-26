import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID
};

let app;
let auth;
let isMockAuth = true;

// Check if variables are configured and not placeholders
const hasConfig = 
  firebaseConfig.apiKey && 
  firebaseConfig.apiKey !== 'your_key' &&
  firebaseConfig.authDomain && 
  firebaseConfig.projectId;

if (hasConfig) {
  try {
    app = initializeApp(firebaseConfig);
    auth = getAuth(app);
    isMockAuth = false;
    console.log("Firebase Client SDK initialized successfully.");
  } catch (error) {
    console.warn("Failed to initialize Firebase Client SDK: ", error);
    isMockAuth = true;
  }
} else {
  console.log("Firebase client keys missing. Running in Mock Authentication mode.");
  isMockAuth = true;
}

export { auth, isMockAuth };
export default app;
