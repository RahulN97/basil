import React, { useCallback, useEffect } from 'react';
import {
  PlaidLinkError,
  PlaidLinkOnEventMetadata,
  PlaidLinkOnExit,
  PlaidLinkOnExitMetadata,
  PlaidLinkOnSuccess,
  PlaidLinkOnSuccessMetadata,
  PlaidLinkOptions,
  PlaidLinkStableEvent,
  usePlaidLink,
} from 'react-plaid-link';

import { FinClient } from '../clients/FinClient';
import { useFinClient } from '../clients/FinClientContext';
import logger from '../utils/logger';

interface LaunchLinkProps {
  linkToken: string;
  userId: string;
  institutionType: string;
}

const LaunchLink: React.FC<LaunchLinkProps> = ({
  linkToken,
  userId,
  institutionType,
}: LaunchLinkProps) => {
  const finClient: FinClient = useFinClient();

  const onSuccess = useCallback<PlaidLinkOnSuccess>(
    async (publicToken: string, metadata: PlaidLinkOnSuccessMetadata) => {
      try {
        await finClient.exchangeToken(userId, publicToken);
        logger.info('Exchanged public token for item access');
      } catch (error) {
        logger.error('Error exchanging public token');
        throw error;
      }
    },
    [finClient],
  );

  const onExit = useCallback<PlaidLinkOnExit>(
    async (error: PlaidLinkError | null, metadata: PlaidLinkOnExitMetadata) => {
      logger.info('Exiting link');
      if (error != null && error.error_code == 'INVALID_LINK_TOKEN') {
        logger.info('Received invalid link token. Attempting to recreate link token');
        linkToken = await finClient.createLinkToken(userId, institutionType);
      }
      if (error != null) {
        logger.error(`Link exited due to error ${error.error_message}`);
        throw error;
      }
    },
    [finClient],
  );

  const onEvent = async (
    eventName: PlaidLinkStableEvent | string,
    metadata: PlaidLinkOnEventMetadata,
  ) => {
    logger.info(`Link event: ${eventName}`);
    if (eventName === 'ERROR' && metadata.error_code != null) {
      logger.error(`Event error: ${metadata.error_message}`);
    }
  };

  const config: PlaidLinkOptions = {
    onSuccess: onSuccess,
    onExit: onExit,
    onEvent: onEvent,
    token: linkToken,
  };
  const { open, exit, ready } = usePlaidLink(config);

  useEffect(() => {
    if (ready) {
      open();
    }
  }, [open, exit, ready]);

  return <></>;
};

export default LaunchLink;
