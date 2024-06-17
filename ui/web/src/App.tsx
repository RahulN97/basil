import React from 'react';
import logo from './logo.svg';

// import { usePlaidLink } from "react-plaid-link";

import './App.css';

function App() {
  return (

    // const config: PlaidLinkOptions = {
    //   onSuccess: (public_token, metadata) => {}
    //   onExit: (err, metadata) => {}
    //   onEvent: (eventName, metadata) => {}
    //   token: 'GENERATED_LINK_TOKEN',
    // };
    // const { open, exit, ready } = usePlaidLink(config);

    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
