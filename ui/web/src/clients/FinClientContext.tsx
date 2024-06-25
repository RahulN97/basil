import React, { createContext, useContext } from 'react';

import { FinClient } from '../clients/FinClient';
import { AppConfig } from '../config/AppConfig';
import { useAppConfig } from '../config/AppConfigContext';

const FinClientContext = createContext<FinClient | null>(null);

export const FinClientProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const appConfig: AppConfig = useAppConfig();
  const serviceUrl = `http://${appConfig.finServingLayerHost}:${appConfig.finServingLayerPort}`;
  const finClient = new FinClient(serviceUrl);

  return <FinClientContext.Provider value={finClient}>{children}</FinClientContext.Provider>;
};

export const useFinClient = (): FinClient => {
  const context = useContext(FinClientContext);
  if (!context) {
    throw new Error('useFinClient must be used within a FinClientProvider');
  }
  return context;
};
