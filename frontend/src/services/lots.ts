import { apiClient } from './api';
import { Lot } from '../types';

export const lotsService = {
  async getLots(params?: {
    skip?: number;
    limit?: number;
    game_id?: number;
    seller_id?: number;
    status?: string;
    search?: string;
  }): Promise<Lot[]> {
    const response = await apiClient.get('/lots/', { params });
    return response.data;
  },

  async getLot(id: number): Promise<Lot> {
    const response = await apiClient.get(`/lots/${id}`);
    return response.data;
  },

  async createLot(lotData: {
    title: string;
    description: string;
    price: number;
    game_id: number;
  }): Promise<Lot> {
    const response = await apiClient.post('/lots/', lotData);
    return response.data;
  },

  async updateLot(id: number, lotData: Partial<{
    title: string;
    description: string;
    price: number;
    status: string;
  }>): Promise<Lot> {
    const response = await apiClient.put(`/lots/${id}`, lotData);
    return response.data;
  },

  async deleteLot(id: number): Promise<void> {
    await apiClient.delete(`/lots/${id}`);
  },
};