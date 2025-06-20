import { Navbar, Nav, Container } from 'react-bootstrap';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <Navbar bg="light" expand="lg" className="mb-4">
      <Container>
        <Navbar.Brand as={Link} to="/">Onboarding Dashboard</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="me-auto">
            <Nav.Link as={Link} to="/">Dashboard</Nav.Link>
            <Nav.Link as={Link} to="/task-list">Task List</Nav.Link>
            <Nav.Link as={Link} to="/feedback-form">Feedback Form</Nav.Link>
            <Nav.Link as={Link} to="/interactiveChatbot">Interactive Chatbot</Nav.Link>
            <Nav.Link as={Link} to="/adminPanel">Admin Panel for HR</Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default Header

//task list
