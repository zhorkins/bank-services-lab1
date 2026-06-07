import { useState, useEffect } from 'react';
import { useParams, Navigate } from 'react-router-dom';
import { Container, Card, Spinner } from 'react-bootstrap';
import Breadcrumbs from '../components/Breadcrumbs';
import { fetchServiceById } from '../api/api';
import type { BankService } from '../data/mockServices';

const MINIO_IMG_BASE = 'http://localhost:9002/bank/img/';
const MINIO_VIDEO_BASE = 'http://localhost:9002/bank/video/';
const DEFAULT_IMAGE = '/placeholder.png';

const ServiceDetail = () => {
  const { id } = useParams();
  const [service, setService] = useState<BankService | null>(null);
  const [loading, setLoading] = useState(true);
  const [videoError, setVideoError] = useState(false);

  useEffect(() => {
    const load = async () => {
      const data = await fetchServiceById(Number(id));
      setService(data);
      setLoading(false);
    };
    load();
  }, [id]);

  if (loading) return <div className="text-center mt-5"><Spinner animation="border" /></div>;
  if (!service) return <Navigate to="/" />;

  const imageUrl = service.image ? `${MINIO_IMG_BASE}${service.image}` : DEFAULT_IMAGE;
  const videoUrl = service.video ? `${MINIO_VIDEO_BASE}${service.video}` : null;
  const crumbs = [{ label: 'Услуги', path: '/' }, { label: service.name }];

  return (
    <Container className="mt-4">
      <Breadcrumbs crumbs={crumbs} />
      <Card className="mt-3">
        <Card.Body>
          <Card.Title>{service.name}</Card.Title>
          <Card.Text>Балансовый счёт: {service.balance_account}</Card.Text>
          <Card.Text>{service.description}</Card.Text>
        </Card.Body>
        <div className="video-wrapper" style={{ padding: '1rem', background: '#000', textAlign: 'center' }}>
          {videoUrl && !videoError ? (
            <video src={videoUrl} autoPlay loop muted playsInline style={{ width: '100%', maxHeight: '500px' }} onError={() => setVideoError(true)} />
          ) : (
            <img src={imageUrl} alt={service.name} style={{ width: '100%', maxHeight: '500px', objectFit: 'contain' }} onError={(e) => (e.currentTarget.src = DEFAULT_IMAGE)} />
          )}
        </div>
      </Card>
    </Container>
  );
};

export default ServiceDetail;