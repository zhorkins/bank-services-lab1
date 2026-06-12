import type { BankService } from '../data/mockServices';
import { mockServices } from '../data/mockServices';

// Вспомогательная функция для фильтрации мок-данных (fallback)
const filterMockServices = (filters: { search?: string; start_date?: string; end_date?: string }) => {
  let filtered = [...mockServices];
  if (filters.search) {
    filtered = filtered.filter(s => s.name.toLowerCase().includes(filters.search!.toLowerCase()));
  }
  if (filters.start_date) {
    filtered = filtered.filter(s => new Date(s.created_at) >= new Date(filters.start_date!));
  }
  if (filters.end_date) {
    filtered = filtered.filter(s => new Date(s.created_at) <= new Date(filters.end_date!));
  }
  return filtered;
};

export const fetchServices = async (filters?: { search?: string; start_date?: string; end_date?: string }): Promise<BankService[]> => {
  const params = new URLSearchParams();
  if (filters?.search) params.append('name', filters.search);
  if (filters?.start_date) params.append('start_date', filters.start_date);
  if (filters?.end_date) params.append('end_date', filters.end_date);
  const url = `/api/bank_services/${params.toString() ? `?${params.toString()}` : ''}`;
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    // Проверяем, что данные – массив
    return Array.isArray(data) ? data : data.results || [];
  } catch (error) {
    console.warn('Бэкенд недоступен, используем мок-данные', error);
    return filterMockServices(filters || {});
  }
};

export const fetchServiceById = async (id: number): Promise<BankService> => {
  try {
    const response = await fetch(`/api/bank_services/${id}/`);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.warn('Бэкенд недоступен, используем мок', error);
    const mock = mockServices.find(s => s.id === id);
    if (!mock) throw new Error('Услуга не найдена');
    return mock;
  }
};

export const fetchCartItemsCount = async (): Promise<number> => {
  try {
    const response = await fetch('/api/bank_requests/cart/');
    if (!response.ok) {
      // Если 401 или другая ошибка, возвращаем 0
      return 0;
    }
    const data = await response.json();
    return data.items_count ?? 0;
  } catch (error) {
    console.warn('Не удалось получить количество корзины', error);
    return 0;
  }
};