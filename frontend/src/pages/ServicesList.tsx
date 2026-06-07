import { useState, useMemo, useEffect, useRef } from 'react';
import { Form, InputGroup, Button, Alert, Spinner, ProgressBar } from 'react-bootstrap';
import { FaShoppingCart, FaTrashAlt } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import ServiceCard from '../components/ServiceCard';
import Breadcrumbs from '../components/Breadcrumbs';
import { fetchServices, fetchCartItemsCount } from '../api/api';
import { useBankServiceSearch, type IProcessedBankService } from '../hooks/useBankServiceSearch';
import type { BankService } from '../data/mockServices';

interface ServicesListProps {
  cartItems: Set<number>;
  setCartItems: React.Dispatch<React.SetStateAction<Set<number>>>;
}

const ServicesList = ({ cartItems, setCartItems }: ServicesListProps) => {
  const [searchName, setSearchName] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const [services, setServices] = useState<BankService[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const localCartCount = cartItems.size;

  const {
    items: clipItems,
    ready: clipReady,
    progress: clipProgress,
    imageEmbedding,
    searchByImage,
    resetSearch,
  } = useBankServiceSearch(services);

  // Загрузка услуг с бэкенда с параметрами фильтрации
  const loadServices = async () => {
    setLoading(true);
    setError(null);
    try {
      const filters: { search?: string; start_date?: string; end_date?: string } = {};
      if (searchName) filters.search = searchName;
      if (startDate) filters.start_date = startDate;
      if (endDate) filters.end_date = endDate;
      const data = await fetchServices(filters);
      if (data && data.length > 0) {
        setServices(data);
      } else {
        // fallback на моки, если бэкенд вернул пустой массив
        const { mockServices } = await import('../data/mockServices');
        setServices(mockServices);
      }
    } catch (err) {
      console.error('Ошибка загрузки, используем mockServices', err);
      const { mockServices } = await import('../data/mockServices');
      setServices(mockServices);
    } finally {
      setLoading(false);
    }
  };

  const loadCartCount = async () => {
    try {
      const count = await fetchCartItemsCount();
      console.log('Cart count from backend:', count);
    } catch (err) {
      console.error('Cart count error:', err);
    }
  };

  // При изменении фильтров перезагружаем данные с бэкенда
  useEffect(() => {
    loadServices();
  }, [searchName, startDate, endDate]);

  useEffect(() => {
    loadCartCount();
  }, []);

  const isClipActive = imageEmbedding !== null;

  const displayItems = useMemo(() => {
    if (isClipActive) {
      return clipItems.filter(item => item.isVisible);
    } else {
      // Данные уже отфильтрованы бэкендом, просто показываем
      return clipItems;
    }
  }, [isClipActive, clipItems]);

  const handleAddToCart = (id: number) => {
    if (cartItems.has(id)) {
      alert('Эта услуга уже добавлена в заявку!');
      return;
    }
    setCartItems(prev => new Set(prev).add(id));
  };

  const handleClearCart = () => {
    setCartItems(new Set());
  };

  const fileInputRef = useRef<HTMLInputElement>(null);
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) searchByImage(file);
    e.target.value = '';
  };

  const crumbs = [{ label: 'Услуги' }];

  return (
    <div className="space">
      <div className="d-flex justify-content-between align-items-center">
        <h1>Услуги банка</h1>
        <div className="d-flex align-items-center gap-3">
          <Link to="/bank-cart" className="position-relative" style={{ opacity: localCartCount === 0 ? 0.4 : 1 }}>
            <FaShoppingCart size={28} />
            {localCartCount > 0 && (
              <span className="badge bg-danger rounded-circle position-absolute top-0 start-100 translate-middle">
                {localCartCount}
              </span>
            )}
          </Link>
          {localCartCount > 0 && (
            <Button variant="outline-danger" size="sm" onClick={handleClearCart}>
              <FaTrashAlt /> Очистить заявку
            </Button>
          )}
        </div>
      </div>

      <Breadcrumbs crumbs={crumbs} />

      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem', flexWrap: 'wrap', alignItems: 'flex-start' }}>
        <InputGroup style={{ width: '250px' }}>
          <Form.Control
            type="text"
            placeholder="Поиск по названию..."
            value={searchName}
            onChange={(e) => setSearchName(e.target.value)}
            disabled={isClipActive}
          />
        </InputGroup>
        <InputGroup style={{ width: '160px' }}>
          <Form.Control
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            disabled={isClipActive}
          />
        </InputGroup>
        <InputGroup style={{ width: '160px' }}>
          <Form.Control
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            disabled={isClipActive}
          />
        </InputGroup>

        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
          <Button variant="primary" onClick={() => fileInputRef.current?.click()} disabled={!clipReady}>
            {clipReady ? 'Загрузить фото' : 'Загрузка нейросети...'}
          </Button>
          {!clipReady && clipProgress > 0 && (
            <ProgressBar now={clipProgress} label={`${Math.round(clipProgress)}%`} animated style={{ width: '150px' }} />
          )}
          {imageEmbedding && (
            <Button variant="outline-danger" onClick={resetSearch}>
              Сбросить поиск
            </Button>
          )}
          <input
            type="file"
            accept="image/*"
            ref={fileInputRef}
            style={{ display: 'none' }}
            onChange={handleFileChange}
          />
        </div>
      </div>

      {isClipActive && (
        <Alert variant="info" className="mt-2">
          <strong>Поиск по изображению</strong> – показаны услуги, наиболее соответствующие загруженному фото.
        </Alert>
      )}

      {error && <Alert variant="danger" className="mt-2">{error}</Alert>}

      {loading ? (
        <div style={{ textAlign: 'center', margin: '40px 0' }}>
          <Spinner animation="border" />
          <p className="mt-2">Загрузка услуг...</p>
        </div>
      ) : (
        <div className="services-grid">
          {displayItems.map((service) => (
            <ServiceCard key={service.id} service={service} onAddToCart={handleAddToCart} />
          ))}
        </div>
      )}

      {!loading && displayItems.length === 0 && !error && (
        <Alert variant="warning" className="mt-3">
          Ничего не найдено. Попробуйте изменить параметры поиска.
        </Alert>
      )}
    </div>
  );
};

export default ServicesList;