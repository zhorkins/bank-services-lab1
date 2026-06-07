// src/api/api.ts
import { mockServices } from '../data/mockServices';
import type { BankService } from '../data/mockServices';

const API_BASE_URL = '/api';

// Тип для ответа (если используется пагинация)
export interface ApiServicesResponse {
  results?: BankService[];
  total?: number;
}

// Обработка ответа
const handleResponse = async <T>(response: Response): Promise<T> => {
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Ошибка HTTP ${response.status}: ${errorText}`);
  }
  if (response.status === 204) {
    return {} as T;
  }
  return response.json();
};

// GET 1: Список услуг с фильтрацией
export const fetchServices = async (filters: {
  search?: string;
  start_date?: string;
  end_date?: string;
}): Promise<BankService[]> => {
  const params = new URLSearchParams();
  if (filters.search) params.append('name', filters.search);
  if (filters.start_date) params.append('start_date', filters.start_date);
  if (filters.end_date) params.append('end_date', filters.end_date);

  // ← исправленный URL
  const url = `${API_BASE_URL}/bank_services/${params.toString() ? `?${params.toString()}` : ''}`;

  try {
    const response = await fetch(url);
    const data = await handleResponse<any>(response);
    // Если ответ — массив, берём его; если объект с полем results — берём results
    const services = Array.isArray(data) ? data : data.results || [];
    return services;
  } catch (error) {
    console.error('Ошибка при загрузке услуг с бэкенда:', error);
    console.warn('Используем mock-данные');
    return filterMockServices(filters);
  }
};

// GET 2: Одна услуга по ID
export const fetchServiceById = async (id: number): Promise<BankService | null> => {
  try {
    // ← исправленный URL
    const response = await fetch(`${API_BASE_URL}/bank_services/${id}/`);
    return await handleResponse<BankService>(response);
  } catch (error) {
    console.error(`Ошибка при загрузке услуги ${id}:`, error);
    console.warn('Используем mock-данные');
    const mockService = mockServices.find(s => s.id === id);
    return mockService || null;
  }
};

// GET 3: Иконка корзины (количество услуг в черновике)
export const fetchCartItemsCount = async (): Promise<number> => {
  try {
    // ← исправленный URL
    const response = await fetch(`${API_BASE_URL}/bank_requests/cart/`);
    const data = await handleResponse<{ bank_request_id?: number; items_count?: number }>(response);
    return data.items_count ?? 0;
  } catch (error) {
    console.error('Ошибка при загрузке количества товаров в корзине:', error);
    return 0;
  }
};

// Фильтрация mock-данных (без изменений)
const filterMockServices = (filters: {
  search?: string;
  start_date?: string;
  end_date?: string;
}): BankService[] => {
  let filtered = [...mockServices];
  if (filters.search) {
    filtered = filtered.filter(s => s.name.toLowerCase().includes(filters.search!.toLowerCase()));
  }
  if (filters.start_date && filters.end_date) {
    filtered = filtered.filter(s => s.created_at >= filters.start_date! && s.created_at <= filters.end_date!);
  } else if (filters.start_date) {
    filtered = filtered.filter(s => s.created_at >= filters.start_date!);
  } else if (filters.end_date) {
    filtered = filtered.filter(s => s.created_at <= filters.end_date!);
  }
  return filtered;
};