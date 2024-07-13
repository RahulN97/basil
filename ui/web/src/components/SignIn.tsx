import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { Auth, getAuth, onAuthStateChanged } from 'firebase/auth';
import firebase from 'firebase/compat/app';
import * as firebaseui from 'firebaseui';
import 'firebaseui/dist/firebaseui.css';

import { CreateUserParams, FinClient } from '../clients/FinClient';
import { useFinClient } from '../clients/FinClientContext';
import { AppConfig } from '../config/AppConfig';
import { useAppConfig } from '../config/AppConfigContext';
import logger from '../utils/logger';

const SignIn: React.FC = () => {
  const appConfig: AppConfig = useAppConfig();
  const firebaseConfig = {
    apiKey: appConfig.firebaseApiKey,
    authDomain: appConfig.firebaseAuthDomain,
  };
  if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig);
  }

  const [isSignedIn, setIsSignedIn] = useState(false);
  const [userId, setUserId] = useState<string | null>(null);
  const finClient: FinClient = useFinClient();
  const navigate = useNavigate();

  const signInSuccess = (authResult: any, redirectUrl: string) => {
    setUserId(authResult.user.uid);
    setIsSignedIn(true);

    if (authResult.additionalUserInfo.isNewUser) {
      const createUserParams: CreateUserParams = {
        userId: authResult.user.uid,
        name: authResult.user.displayName,
        email: authResult.user.email,
      };
      finClient
        .createUser(createUserParams)
        .then(creationTime => {
          logger.info(`Signed in successfully at ${creationTime}`);
        })
        .catch(error => {
          logger.error(`Error when attempting to create user ${error}`);
          return false;
        });
    }
    return true;
  };

  const handleSignOut = () => {
    firebase.auth().signOut();
    setUserId(null);
    setIsSignedIn(false);
    navigate('/');
  };

  const authConfig: firebaseui.auth.Config = {
    signInFlow: 'popup',
    signInOptions: [
      {
        provider: firebase.auth.GoogleAuthProvider.PROVIDER_ID,
        customParameters: {
          prompt: 'select_account',
        },
      },
      {
        provider: firebase.auth.EmailAuthProvider.PROVIDER_ID,
        requireDisplayName: true,
      },
    ],
    callbacks: {
      signInSuccessWithAuthResult: signInSuccess,
    },
  };

  useEffect(() => {
    const auth: Auth = getAuth();
    const ui = firebaseui.auth.AuthUI.getInstance() || new firebaseui.auth.AuthUI(auth);

    const unregisterAuthObserver = onAuthStateChanged(auth, user => {
      if (!user && isSignedIn) {
        ui.reset();
      }
      setIsSignedIn(!!user);
      setUserId(user ? user.uid : null);
    });

    if (document.getElementById('firebaseui-auth-container')) {
      ui.start('#firebaseui-auth-container', authConfig);
    }

    return () => {
      unregisterAuthObserver();
      ui.reset();
    };
  }, [authConfig, isSignedIn]);

  if (!isSignedIn) {
    return (
      <div>
        <h1>Basil</h1>
        <p>Please sign-in:</p>
        <div id="firebaseui-auth-container"></div>
      </div>
    );
  }

  return (
    <div>
      <h1>Basil</h1>
      <p>Welcome {firebase.auth().currentUser?.displayName}! You are now signed-in!</p>
      <button
        onClick={() => {
          navigate('/home', { replace: true, state: { userId: userId } });
        }}
      >
        Home Page
      </button>
      <button onClick={handleSignOut}>Sign-out</button>
    </div>
  );
};

export default SignIn;
