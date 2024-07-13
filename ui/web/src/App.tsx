import React from 'react';
import { RouterProvider, createBrowserRouter } from 'react-router-dom';

import './App.css';
import { FinClientProvider } from './clients/FinClientContext';
import HomePage from './components/HomePage';
import Landing from './components/Landing';
import SignIn from './components/SignIn';
import { AppConfigProvider } from './config/AppConfigContext';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Landing />,
  },
  {
    path: '/signin',
    element: <SignIn />,
  },
  {
    path: '/home',
    element: <HomePage />,
  },
]);

function App() {
  return (
    <div className="App">
      <AppConfigProvider>
        <FinClientProvider>
          <RouterProvider router={router} />
        </FinClientProvider>
      </AppConfigProvider>
    </div>
  );
}

export default App;
