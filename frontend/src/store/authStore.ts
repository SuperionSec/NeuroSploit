import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { getToken, setToken, removeToken, getStoredUser, setStoredUser } from '../services/apiClient';

export interface User {
  id: string;
  username: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

interface AuthState {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  setAuth: (token: string, user: User) => void;
  setUser: (user: User) => void;
  logout: () => void;
  checkAuth: () => boolean;
  initAuth: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      isAuthenticated: false,
      isLoading: true,

      setAuth: (token: string, user: User) => {
        setToken(token);
        setStoredUser(user);
        set({ token, user, isAuthenticated: true });
      },

      setUser: (user: User) => {
        setStoredUser(user);
        set({ user });
      },

      logout: () => {
        removeToken();
        set({ token: null, user: null, isAuthenticated: false });
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
      },

      checkAuth: () => {
        const token = getToken();
        const user = getStoredUser();
        if (token && user) {
          set({ token, user, isAuthenticated: true, isLoading: false });
          return true;
        }
        set({ isLoading: false });
        return false;
      },

      initAuth: () => {
        const token = getToken();
        const user = getStoredUser();
        if (token && user) {
          set({ token, user, isAuthenticated: true, isLoading: false });
        } else {
          set({ isLoading: false });
        }
      },
    }),
    {
      name: 'neurosploit-auth',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        token: state.token,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);

export const isAdmin = () => {
  const user = useAuthStore.getState().user;
  return user?.role === 'admin';
};

export const isUser = () => {
  const user = useAuthStore.getState().user;
  return user?.role === 'user';
};
