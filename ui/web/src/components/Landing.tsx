import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { FinClient } from '../clients/FinClient';
import { useFinClient } from '../clients/FinClientContext';

const Landing: React.FC = () => {
  const finClient: FinClient = useFinClient();
  const [userId, setUserId] = useState('');
  const [healthStatus, setHealthStatus] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setUserId(event.target.value);
  };

  const handleButtonClick = () => {
    if (userId) {
      navigate(`/user/${userId}`);
    }
  };

  const handleHealthButtonClick = async () => {
    try {
      const health: string = await finClient.getHealthStatus();
      setHealthStatus(health);
    } catch (error) {
      console.log('Error fetching health status');
    }
  };

  return (
    <div>
      <h1>Welcome to Basil</h1>
      <button onClick={handleHealthButtonClick}>Check Service Health</button>
      {healthStatus && <p>Health Status: {healthStatus}</p>}
      <input type="text" placeholder="Enter User ID" value={userId} onChange={handleInputChange} />
      <button onClick={handleButtonClick}>Go to HomePage</button>
    </div>
  );
};

export default Landing;
