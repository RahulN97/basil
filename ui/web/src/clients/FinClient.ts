import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';

import logger from '../utils/logger';
import { ApiError } from './ApiError';

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

  public async createLinkToken(userId: string, institutionType: string): Promise<string> {
    const endpoint = '/create/link/token';
    const data: Record<string, string> = {
      user_id: userId,
      institution_type: institutionType,
    };
    try {
      const response: AxiosResponse = await this.post(endpoint, data);
      return response.data.link_token;
    } catch (error: any) {
      throw new ApiError(error.message);
    }
  }

  public async exchangeToken(publicToken: string): Promise<string> {
    return 'some_access_token';
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
