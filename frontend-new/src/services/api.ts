import axios from "axios";
import type { AxiosResponse } from "axios";

export class GenericAPI {
  private url: string;

  constructor(endpoint: string = "") {
    const baseUrl = "/api/v1"; // Vite proxy will handle routing
    this.url = endpoint ? `${baseUrl}/${endpoint}` : baseUrl;
  }

  async post(data: Record<string, any>): Promise<AxiosResponse> {
    return axios.post(`${this.url}/`, data, {
      timeout: 10000,
      headers: {
        Accept: "application/json",
      },
    });
  }

  async get(objId?: number): Promise<AxiosResponse> {
    const fullUrl = objId ? `${this.url}/${objId}/` : `${this.url}/`; // force trailing slash
    console.log("GET request to:", fullUrl); // ← logging added
    return axios.get(fullUrl, {
      timeout: 10000,
      headers: {
        Accept: "application/json",
      },
    });
  }
}
