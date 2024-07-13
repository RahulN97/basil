import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';

import logger from '../utils/logger';
import { ApiError } from './ApiError';

export interface CreateUserParams {
  userId: string;
  name: string;
  email: string;
}

export class FinClient {
  private apiUrl: string;
  private readonly HEADERS: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  constructor(apiUrl: string) {
    this.apiUrl = apiUrl;
  }

  private async get(endpoint: string): Promise<AxiosResponse> {
    const url: string = this.apiUrl + endpoint;
    const requestConfig: AxiosRequestConfig = {
      headers: this.HEADERS,
    };
    logger.info(`Issuing GET ${url}`);
    const response: AxiosResponse = await axios.get(url, requestConfig);
    return response;
  }

  private async post(endpoint: string, data: any): Promise<AxiosResponse> {
    const url: string = this.apiUrl + endpoint;
    const requestConfig: AxiosRequestConfig = {
      headers: this.HEADERS,
    };
    logger.info(`Issuing POST ${url}`);
    const response: AxiosResponse = await axios.post(url, data, requestConfig);
    return response;
  }

  public async createUser({ userId, name, email }: CreateUserParams): Promise<string> {
    const endpoint = '/users/';
    const data: Record<string, string> = {
      user_id: userId,
      name: name,
      email: email,
    };
    try {
      const response: AxiosResponse = await this.post(endpoint, data);
      return response.data.creation_time;
    } catch (error: any) {
      throw new ApiError(error.message);
    }
  }

  public async createLinkToken(userId: string, institutionType: string): Promise<string> {
    const endpoint = '/fin-data/link_token';
    const data: Record<string, string> = {
      user_id: userId,
      institution_type: institutionType,
    };
    try {
      const response: AxiosResponse = await this.post(endpoint, data);
      return response.data.token;
    } catch (error: any) {
      throw new ApiError(error.message);
    }
  }

  public async exchangeToken(userId: string, publicToken: string): Promise<void> {
    const endpoint = '/fin-data/item_access';
    const data: Record<string, string> = {
      user_id: userId,
      public_token: publicToken,
    };
    try {
      const response: AxiosResponse = await this.post(endpoint, data);
      // TODO: store response data
    } catch (error: any) {
      throw new ApiError(error.message);
    }
  }

  public async getHealthStatus(): Promise<string> {
    const endpoint = '/health';
    try {
      const response: AxiosResponse = await this.get(endpoint);
      return response.data.status;
    } catch (error: any) {
      throw new ApiError(error.message);
    }
  }
}
