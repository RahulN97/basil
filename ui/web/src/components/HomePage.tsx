import React, { useState } from 'react';

import { FinClient } from '../clients/FinClient';
import { useFinClient } from '../clients/FinClientContext';
import LaunchLink from './LaunchLink';

const HomePage: React.FC = () => {
  const [linkToken, setLinkToken] = useState<string | null>(null);
  const finClient: FinClient = useFinClient();
  const userId = window.location.pathname.split('/')[2];

  // TODO: get institutionType
  const institutionType = 'test';

  const generateLinkToken = async () => {
    const token = await finClient.createLinkToken(userId, institutionType);
    setLinkToken(token);
  };

  return (
    <div>
      <h1>Home Page</h1>
      <button onClick={generateLinkToken}>Add Bank Account</button>
      {linkToken && <LaunchLink linkToken={linkToken} userId={userId} />}
    </div>
  );
};

export default HomePage;
