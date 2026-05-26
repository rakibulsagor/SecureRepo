// Exposed Firebase Client Keys - Insecure Hardcoded Configuration
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyDummyKeyForFirebaseDemo123456",
  authDomain: "demo-vulnerable-repo.firebaseapp.com",
  projectId: "demo-vulnerable-repo",
  storageBucket: "demo-vulnerable-repo.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:a1b2c3d4e5f6g7"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
