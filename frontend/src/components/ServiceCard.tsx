import { useNavigate } from 'react-router-dom';
import type { BankService } from '../data/mockServices';

const MINIO_IMG_BASE = 'http://localhost:9002/bank/img/';

const DEFAULT_IMAGE = '/placeholder.png';

interface ServiceCardProps {
  service: BankService;
  onAddToCart: (id: number) => void;
}

const ServiceCard = ({ service, onAddToCart }: ServiceCardProps) => {
  const navigate = useNavigate();

  const imageUrl = service.image
    ? `${MINIO_IMG_BASE}${service.image}`
    : DEFAULT_IMAGE;

  const handleCardClick = () => {
    navigate(`/service/${service.id}`);
  };

  const handleAddClick = (e: React.MouseEvent) => {
    e.stopPropagation(); // не даём карточке перейти на страницу
    onAddToCart(service.id);
  };

  return (
    <div className="card" onClick={handleCardClick} style={{ cursor: 'pointer' }}>
      <img
        src={imageUrl}
        className="card-image"
        alt={service.name}
        onError={(e) => (e.currentTarget.src = DEFAULT_IMAGE)}
      />
      <div className="title">{service.name}</div>
      <div className="short-description">Балансовый счёт: {service.balance_account}</div>
      <button className="card-button" onClick={handleAddClick}>
        Добавить в заявку
      </button>
    </div>
  );
};

export default ServiceCard;