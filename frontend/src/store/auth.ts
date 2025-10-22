import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User } from '@/types';
import { authService } from '../services/auth';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  
  // Actions
  login: (credentials: { email: string; password: string }) => Promise<void>;
  register: (userData: { username: string; email: string; password: string; display_name?: string }) => Promise<void>;
  logout: () => void;
  loadUser: () => Promise<void>;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (credentials) => {
        set({ isLoading: true });
        try {
          const response = await authService.login(credentials);
          const user = response.user;
          set({ 
            user, 
            isAuthenticated: true, 
            isLoading: false 
          });
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },

      register: async (userData) => {
        set({ isLoading: true });
        try {
          const response = await authService.register(userData);
          const user = response.user;
          set({ 
            user, 
            isAuthenticated: true, 
            isLoading: false 
          });
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },

      logout: () => {
        authService.logout();
        set({ 
          user: null, 
          isAuthenticated: false, 
          isLoading: false 
        });
      },

      loadUser: async () => {
        if (!get().user) {
          return;
        }

        set({ isLoading: true });
        try {
          const user = await authService.getProfile();
          set({ 
            user, 
            isAuthenticated: true, 
            isLoading: false 
          });
        } catch (error) {
          // Token is invalid, clear auth state
          authService.logout();
          set({ 
            user: null, 
            isAuthenticated: false, 
            isLoading: false 
          });
        }
      },

      clearError: () => {
        // Can be used to clear any error state if needed
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ 
        isAuthenticated: state.isAuthenticated,
        user: state.user 
      }),
    }
  )
);