export interface User {
  id: number;
  username: string;
  email: string;
  display_name?: string;
  avatar_url?: string;
  bio?: string;
  is_active: boolean;
  is_verified: boolean;
  role: 'user' | 'seller' | 'moderator' | 'admin';
  rating: number;
  total_reviews: number;
  total_sales: number;
  total_purchases: number;
  created_at: string;
  updated_at?: string;
  last_online?: string;
}

export interface Game {
  id: number;
  name: string;
  slug: string;
  description?: string;
  image_url?: string;
  icon_url?: string;
  developer?: string;
  publisher?: string;
  release_date?: string;
  genres?: string[];
  platforms?: string[];
  total_lots: number;
  is_popular: boolean;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
  category?: Category;
}

export interface GameCategory extends Category {
  // Псевдоним для совместимости
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description?: string;
  icon?: string;
  game_id: number;
  parent_id?: number;
  total_lots: number;
  is_active: boolean;
  sort_order: number;
  created_at: string;
  game?: Game;
  parent?: Category;
  children?: Category[];
}

export interface Lot {
  id: number;
  title: string;
  description: string;
  price: number;
  seller_id: number;
  game_id: number;
  category_id: number;
  item_details?: Record<string, any>;
  images?: string[];
  status: 'active' | 'sold' | 'inactive' | 'moderation';
  is_auto_delivery: boolean;
  delivery_time?: string;
  requirements?: string;
  views: number;
  favorites: number;
  created_at: string;
  updated_at?: string;
  seller?: User;
  game?: Game;
  category?: Category;
}

export interface Order {
  id: number;
  order_number: string;
  buyer_id: number;
  seller_id: number;
  lot_id: number;
  price: number;
  status: 'pending' | 'paid' | 'in_progress' | 'completed' | 'cancelled' | 'disputed';
  buyer_message?: string;
  seller_response?: string;
  escrow_id?: string;
  payment_method?: string;
  created_at: string;
  updated_at?: string;
  completed_at?: string;
  buyer?: User;
  seller?: User;
  lot?: Lot;
}

export interface Message {
  id: number;
  content: string;
  sender_id: number;
  receiver_id: number;
  order_id?: number;
  is_read: boolean;
  is_system: boolean;
  attachments?: string[];
  created_at: string;
  sender?: User;
  receiver?: User;
}

export interface Review {
  id: number;
  rating: number;
  comment?: string;
  reviewer_id: number;
  reviewed_id: number;
  order_id: number;
  is_visible: boolean;
  created_at: string;
  reviewer?: User;
  reviewed?: User;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  skip: number;
  limit: number;
}

// Auth types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

// API Error
export interface ApiError {
  detail: string | { msg: string; type: string }[];
}

// Filters and sorting
export interface LotFilters {
  game_id?: number;
  category_id?: number;
  min_price?: number;
  max_price?: number;
  search?: string;
  seller_id?: number;
  status?: string;
}

export interface SortOption {
  value: string;
  label: string;
}