import { Navbar, Container } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const AppNavbar = () => {
  return (
    <Navbar style={{ backgroundColor: '#0047B3' }} variant="dark" expand="lg">
      <Container>
        <Navbar.Brand as={Link} to="/">Договоры банка</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          {/* можно оставить пустым */}
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default AppNavbar;