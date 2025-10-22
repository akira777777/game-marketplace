import { apiClient } from './api';
import { Game, Category } from '../types';

export const gamesService = {
  async getGames(params?: {
    skip?: number;
    limit?: number;
    search?: string;
    category?: string;
  }): Promise<Game[]> {
    const response = await apiClient.get('/games/', { params });
    return response.data;
  },

  async getGame(id: number): Promise<Game> {
    const response = await apiClient.get(`/games/${id}`);
    return response.data;
  },

  async getCategories(): Promise<Category[]> {
    const response = await apiClient.get('/games/categories/');
    return response.data;
  },

  async createGame(gameData: {
    name: string;
    description?: string;
    category_id?: number;
    image_url?: string;
  }): Promise<Game> {
    const response = await apiClient.post('/games/', gameData);
    return response.data;
  },
};