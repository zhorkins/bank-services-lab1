import { Container, Row, Col, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <Container className="mt-5 text-center">
      <Row>
        <Col>
          <h1>Добро пожаловать в систему банковских услуг</h1>
          <p className="lead">
            Оформляйте заявки на подключение банковских услуг онлайн.
            Выберите услуги, укажите свои данные, сформируйте заявку –
            а модератор проверит и завершит её.
          </p>
          <Link to="/services">
            <Button variant="primary" size="lg">Перейти к услугам</Button>
          </Link>
        </Col>
      </Row>
    </Container>
  );
};

export default HomePage;