import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

import { FinClient } from '../clients/FinClient';
import { useFinClient } from '../clients/FinClientContext';
import LaunchLink from './LaunchLink';

const HomePage: React.FC = () => {
  const params = useLocation();
  const userId = params.state?.userId;

  const [linkToken, setLinkToken] = useState<string | null>(null);
  const [institutionType, setInstitutionType] = useState<string>('not_specified');
  const finClient: FinClient = useFinClient();
  const navigate = useNavigate();

  const generateLinkToken = async (inputInstitutionType: string) => {
    setInstitutionType(inputInstitutionType);
    const token = await finClient.createLinkToken(userId, inputInstitutionType);
    setLinkToken(token);
  };

  if (userId === undefined) {
    return (
      <div>
        <h1>Need to sign in before accessing home page</h1>
        <button onClick={() => navigate('/signin')}>Sign In</button>
      </div>
    );
  }
  return (
    <div>
      <h1>Home Page</h1>
      <button onClick={() => generateLinkToken('cash')}>Add Bank Account</button>
      <button onClick={() => generateLinkToken('credit')}>Add Credit Card</button>
      <button onClick={() => generateLinkToken('investment')}>Add Investment Account</button>
      {linkToken && (
        <LaunchLink linkToken={linkToken} userId={userId} institutionType={institutionType} />
      )}
    </div>
  );
};

export default HomePage;
