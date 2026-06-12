import { Navbar, Nav, Container } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const AppNavbar = () => {
  return (
    <Navbar style={{ backgroundColor: '#0047B3' }} variant="dark" expand="lg">
      <Container>
        <Navbar.Brand as={Link} to="/">Банк Услуг</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/services">Услуги</Nav.Link>
            <Nav.Link as={Link} to="/bank-cart">Корзина</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default AppNavbar;