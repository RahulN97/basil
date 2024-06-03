import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import logger from './../logger';


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
        }
        logger.info(`Issuing GET ${url}`)
        const response: AxiosResponse = await axios.get(
            url,
            requestConfig
        );
        return response;
    }

    private async post(endpoint: string, data: any): Promise<AxiosResponse> {
        const url: string = this.apiUrl + endpoint;
        const requestConfig: AxiosRequestConfig = {
            headers: this.HEADERS,
        };
        logger.info(`Issuing POST ${url}`)
        const response: AxiosResponse = await axios.post(
            url,
            data,
            requestConfig
        );
        return response;
    }

    public async createLinkToken(user_id: string, institution_type: string): Promise<string> {
        const endpoint: string = '/create/link/token'
        const data: Record<string, string> = {
            "user_id": user_id,
            "institution_type": institution_type,
        };
        try {
            const response: AxiosResponse = await this.post(endpoint, data);
            return response.data.link_token;
        } catch (error: any) {
            throw new Error(`Error: ${error.message}`);
        }
    }

    public async getHealthStatus(): Promise<string> {
        const endpoint: string = '/health'
        try {
            const response: AxiosResponse = await this.get(endpoint);
            return response.data.status;
        } catch (error: any) {
            logger.info(`Error fetching health status: ${error.message}`);
            throw new Error(`Error: ${error.message}`);
        }
    }
}
