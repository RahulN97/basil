import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { FinClient } from '../clients/FinClient';
import { useFinClient } from '../clients/FinClientContext';
import logger from '../utils/logger';

const Landing: React.FC = () => {
  const finClient: FinClient = useFinClient();
  const [healthStatus, setHealthStatus] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const checkHealthStatus = async () => {
      try {
        const health: string = await finClient.getHealthStatus();
        setHealthStatus(health);
      } catch (error) {
        logger.error('Error fetching health status');
        setHealthStatus('unhealthy');
      }
    };

    checkHealthStatus();
    const periodicHealthCheck = setInterval(checkHealthStatus, 1e4);
    return () => {
      clearInterval(periodicHealthCheck);
    };
  }, [finClient]);

  return (
    <div>
      <h1>Welcome to Basil</h1>
      <div style={{ position: 'absolute', top: 10, right: 10 }}>
        <span
          style={{
            height: '10px',
            width: '10px',
            backgroundColor: healthStatus === 'healthy' ? 'green' : 'red',
            borderRadius: '50%',
            display: 'inline-block',
          }}
        ></span>
      </div>
      <button
        onClick={() => {
          navigate('/signin');
        }}
      >
        Sign In
      </button>
    </div>
  );
};

export default Landing;
