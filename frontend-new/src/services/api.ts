import axios from "axios";
import type { AxiosResponse } from "axios";

export class GenericAPI {
  private url: string;

  constructor(endpoint: string = "") {
    const baseUrl = "/api/v1"; 
    this.url = endpoint ? `${baseUrl}/${endpoint}` : baseUrl;
  }

  async get(objId?: number): Promise<AxiosResponse> {
    const fullUrl = objId ? `${this.url}/${objId}/` : `${this.url}/`;
    console.log("GET request to:", fullUrl);
    return axios.get(fullUrl, {
      timeout: 10000,
      headers: { Accept: "application/json" },
    });
  }

  async post(data: Record<string, any>): Promise<AxiosResponse> {
    const fullUrl = `${this.url}/`;
    console.log("POST request to:", fullUrl, data);
    return axios.post(fullUrl, data, {
      timeout: 10000,
      headers: { Accept: "application/json" },
    });
  }

  async patch(objId: number, data: Record<string, any>): Promise<AxiosResponse> {
    const fullUrl = `${this.url}/${objId}/`;
    console.log("PATCH request to:", fullUrl, data);
    return axios.patch(fullUrl, data, {
      timeout: 10000,
      headers: { Accept: "application/json" },
    });
  }

  async delete(objId: number): Promise<AxiosResponse> {
    const fullUrl = `${this.url}/${objId}/`;
    console.log("DELETE request to:", fullUrl);
    return axios.delete(fullUrl, {
      timeout: 10000,
      headers: { Accept: "application/json" },
    });
  }
}
