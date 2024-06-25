import React, { ReactNode, createContext, useContext } from 'react';

import { AppConfig } from './AppConfig';

const AppConfigContext = createContext<AppConfig | null>(null);

interface AppConfigProviderProps {
  children: ReactNode;
}

export const AppConfigProvider: React.FC<AppConfigProviderProps> = ({ children }) => {
  const appConfig = new AppConfig();
  return <AppConfigContext.Provider value={appConfig}>{children}</AppConfigContext.Provider>;
};

export const useAppConfig = (): AppConfig => {
  const context = useContext(AppConfigContext);
  if (!context) {
    throw new Error('useAppConfig must be used within an AppConfigProvider');
  }
  return context;
};
