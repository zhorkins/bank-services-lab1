import { useState, useMemo } from 'react';
import { Form, InputGroup, Button } from 'react-bootstrap';
import { FaShoppingCart, FaTrashAlt } from 'react-icons/fa';
import { Link } from 'react-router-dom';
import ServiceCard from '../components/ServiceCard';
import Breadcrumbs from '../components/Breadcrumbs';
import { mockServices } from '../data/mockServices';  // ← исправлено

interface ServicesListProps {
  cartItems: Set<number>;
  setCartItems: React.Dispatch<React.SetStateAction<Set<number>>>;
}

const ServicesList = ({ cartItems, setCartItems }: ServicesListProps) => {
  const [searchName, setSearchName] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  const itemsCount = cartItems.size;

  const handleAddToCart = (id: number) => {
    if (cartItems.has(id)) {
      alert('Эта услуга уже добавлена в заявку!');
      return;
    }
    setCartItems((prev) => new Set(prev).add(id));
    alert(`Услуга ${id} добавлена в заявку`);
  };

  const handleClearCart = () => {
    if (cartItems.size === 0) return;
    setCartItems(new Set());
    alert('Заявка очищена');
  };

  // Нормализация дат для фильтра
  const normalizeToDayStart = (dateInput: string): number => {
    const d = new Date(dateInput);
    if (isNaN(d.getTime())) return -Infinity;
    return Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate());
  };

  const filteredServices = useMemo(() => {
    return mockServices.filter((service) => {
      const nameMatch = service.name.toLowerCase().includes(searchName.toLowerCase());

      let dateMatch = true;
      const serviceTimestamp = normalizeToDayStart(service.created_at);
      if (startDate && endDate) {
        const startTs = normalizeToDayStart(startDate);
        const endTs = normalizeToDayStart(endDate);
        dateMatch = serviceTimestamp >= startTs && serviceTimestamp <= endTs;
      } else if (startDate) {
        dateMatch = serviceTimestamp >= normalizeToDayStart(startDate);
      } else if (endDate) {
        dateMatch = serviceTimestamp <= normalizeToDayStart(endDate);
      }
  // Внутри ServicesList, до useMemo или внутри него
console.log('Все услуги с датами:',
  mockServices.map(s => ({
    name: s.name,
    created_at: s.created_at,
    normalized: new Date(s.created_at).toISOString().split('T')[0]
  }))
);
      return nameMatch && dateMatch;
    });
  }, [searchName, startDate, endDate]);

  const crumbs = [{ label: 'Услуги' }];

  return (
    <div className="space">
      <div className="d-flex justify-content-between align-items-center">
        <h1>Услуги</h1>
        <div className="d-flex align-items-center gap-3">
          {/* Иконка корзины – серая и неактивная, если пуста */}
          <Link
            to="/bank-cart"
            className="position-relative"
            style={{
              opacity: itemsCount === 0 ? 0.4 : 1,
              pointerEvents: itemsCount === 0 ? 'none' : 'auto',
              transition: 'opacity 0.2s',
            }}
          >
            <FaShoppingCart size={28} color={itemsCount === 0 ? '#6c757d' : '#000'} />
            {itemsCount > 0 && (
              <span className="badge bg-danger rounded-circle position-absolute top-0 start-100 translate-middle">
                {itemsCount}
              </span>
            )}
          </Link>
          {itemsCount > 0 && (
            <Button variant="outline-danger" size="sm" onClick={handleClearCart}>
              <FaTrashAlt /> Очистить заявку
            </Button>
          )}
        </div>
      </div>
      <Breadcrumbs crumbs={crumbs} />

      {/* Фильтры */}
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
        <InputGroup style={{ width: '300px' }}>
          <Form.Control
            type="text"
            placeholder="Поиск по названию..."
            value={searchName}
            onChange={(e) => setSearchName(e.target.value)}
          />
        </InputGroup>
        <InputGroup style={{ width: '180px' }}>
          <Form.Control
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            placeholder="С даты"
          />
        </InputGroup>
        <InputGroup style={{ width: '180px' }}>
          <Form.Control
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            placeholder="По дату"
          />
        </InputGroup>
      </div>

      <div className="services-grid">
        {filteredServices.map((service) => (
          <ServiceCard key={service.id} service={service} onAddToCart={handleAddToCart} />
        ))}
      </div>
    </div>
  );
};

export default ServicesList;