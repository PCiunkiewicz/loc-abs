// services/api.ts
import axios from "axios";
import type { AxiosInstance, AxiosResponse } from "axios";

export class GenericAPI {
  private url: string;
  private session: AxiosInstance;

  constructor(endpoint: string = "") {
    const baseUrl = "http://api:8000/api/v1";
    this.url = endpoint ? `${baseUrl}/${endpoint}` : baseUrl;
    this.session = axios.create();
  }

  async post(data: Record<string, any>): Promise<AxiosResponse> {
    return this.session.post(`${this.url}/`, data, { timeout: 10000 });
  }

  async get(objId?: number): Promise<AxiosResponse> {
    const fullUrl = objId ? `${this.url}/${objId}` : this.url;
    return this.session.get(fullUrl);
  }
}
