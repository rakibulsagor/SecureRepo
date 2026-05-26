import React, { createContext, useContext, useState, useEffect } from 'react';
import { 
  signInWithEmailAndPassword, 
  createUserWithEmailAndPassword, 
  GoogleAuthProvider,
  signInWithPopup,
  signOut, 
  onAuthStateChanged,
  updateProfile
} from 'firebase/auth';
import { auth, isMockAuth } from '../firebase/firebaseConfig';

const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Helper for mock user actions
  const getMockUserFromStorage = () => {
    const user = localStorage.getItem('securerepo_mock_user');
    return user ? JSON.parse(user) : null;
  };

  useEffect(() => {
    if (!isMockAuth && auth) {
      const unsubscribe = onAuthStateChanged(auth, (user) => {
        if (user) {
          setCurrentUser({
            uid: user.uid,
            email: user.email,
            displayName: user.displayName || user.email.split('@')[0],
          });
        } else {
          setCurrentUser(null);
        }
        setLoading(false);
      });
      return unsubscribe;
    } else {
      // Mock mode initialization
      const mockUser = getMockUserFromStorage();
      setCurrentUser(mockUser);
      setLoading(false);
    }
  }, []);

  const signup = async (email, password, displayName) => {
    if (!isMockAuth && auth) {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      await updateProfile(userCredential.user, { displayName });
      setCurrentUser({
        uid: userCredential.user.uid,
        email: userCredential.user.email,
        displayName: displayName,
      });
      return userCredential.user;
    } else {
      // Mock signup
      const newMockUser = {
        uid: `mock-uid-${Date.now()}`,
        email,
        displayName: displayName || email.split('@')[0],
      };
      localStorage.setItem('securerepo_mock_user', JSON.stringify(newMockUser));
      setCurrentUser(newMockUser);
      return newMockUser;
    }
  };

  const login = async (email, password) => {
    if (!isMockAuth && auth) {
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      setCurrentUser({
        uid: userCredential.user.uid,
        email: userCredential.user.email,
        displayName: userCredential.user.displayName || email.split('@')[0],
      });
      return userCredential.user;
    } else {
      // Mock login
      const mockUser = {
        uid: 'mock-uid-default',
        email: email,
        displayName: email.split('@')[0],
      };
      localStorage.setItem('securerepo_mock_user', JSON.stringify(mockUser));
      setCurrentUser(mockUser);
      return mockUser;
    }
  };

  const loginWithGoogle = async () => {
    if (!isMockAuth && auth) {
      const provider = new GoogleAuthProvider();
      provider.setCustomParameters({ prompt: 'select_account' });
      const userCredential = await signInWithPopup(auth, provider);
      const displayName = userCredential.user.displayName || userCredential.user.email?.split('@')[0] || 'Google User';
      setCurrentUser({
        uid: userCredential.user.uid,
        email: userCredential.user.email,
        displayName,
      });
      return userCredential.user;
    } else {
      const mockUser = {
        uid: 'mock-google-uid-default',
        email: 'google.demo@securerepo.local',
        displayName: 'Google Demo User',
      };
      localStorage.setItem('securerepo_mock_user', JSON.stringify(mockUser));
      setCurrentUser(mockUser);
      return mockUser;
    }
  };

  const logout = async () => {
    if (!isMockAuth && auth) {
      await signOut(auth);
    } else {
      localStorage.removeItem('securerepo_mock_user');
    }
    setCurrentUser(null);
  };

  const value = {
    currentUser,
    isMockAuth,
    signup,
    login,
    loginWithGoogle,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}
