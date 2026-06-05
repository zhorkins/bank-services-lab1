import { Container, Table, Button, Alert } from 'react-bootstrap';
import Breadcrumbs from '../components/Breadcrumbs';
import { mockServices } from '../data/mockServices';

const MINIO_IMG_BASE = 'http://localhost:9002/bank/img/';

const DEFAULT_IMAGE = '/placeholder.png';

interface BankCartProps {
  cartItems: Set<number>;
  clearCart: () => void;
}

const BankCart = ({ cartItems, clearCart }: BankCartProps) => {
  const selectedServices = mockServices.filter((s) => cartItems.has(s.id));
  const totalPrice = selectedServices.reduce((sum, s) => sum + (s.price || 0), 0);

  const crumbs = [{ label: 'Корзина' }];
  const requestNumber = Math.floor(Math.random() * 1000);

  return (
    <Container className="mt-4">
      <Breadcrumbs crumbs={crumbs} />
      {selectedServices.length === 0 ? (
        <Alert variant="secondary">Корзина пуста. Добавьте услуги на главной странице.</Alert>
      ) : (
        <>
          <h3>Заявка №{requestNumber}</h3>
          <p>Клиент: Гость</p>
          <p>Стоимость обслуживания: {totalPrice} руб.</p>
          <Button variant="danger" size="sm" onClick={clearCart} className="mb-3">
            Удалить заявку
          </Button>
          <Table striped bordered hover>
            <thead>
              <tr>
                <th>Фото</th>
                <th>Услуга</th>
                <th>Балансовый счет</th>
                <th>Банковский счет</th>
                <th>Стоимость услуги</th>
              </tr>
            </thead>
            <tbody>
              {selectedServices.map((s) => {
                const imgUrl = s.image ? `${MINIO_IMG_BASE}${s.image}` : DEFAULT_IMAGE;
                return (
                  <tr key={s.id}>
                    <td style={{ width: '80px' }}>
                      <img
                        src={imgUrl}
                        alt={s.name}
                        style={{ width: '60px', height: '60px', objectFit: 'cover', borderRadius: '4px' }}
                        onError={(e) => (e.currentTarget.src = DEFAULT_IMAGE)}
                      />
                    </td>
                    <td>{s.name}</td>
                    <td>{s.balance_account}</td>
                    <td>—</td>
                    <td>{s.price} руб.</td>
                  </tr>
                );
              })}
            </tbody>
          </Table>
        </>
      )}
    </Container>
  );
};

export default BankCart;