import { Card, Row, Col, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div>
      <h2 className="mb-4">Welcome to the HR Dashboard👋</h2>
      <Row xs={1} md={2} className="g-4">
        <Col>
          <Card>
            <Card.Body>
              <Card.Title>Task List</Card.Title>
              <Card.Text>View and complete your onboarding tasks.</Card.Text>
              <Button as={Link} to="/task-list" variant="primary">Go to Task List</Button>
            </Card.Body>
          </Card>
        </Col>
        <Col>
          <Card>
            <Card.Body>
              <Card.Title>Feedback Form</Card.Title>
              <Card.Text>Send feedback or suggestions to HR.</Card.Text>
              <Button as={Link} to="/feedback-form" variant="primary">Give Feedback</Button>
            </Card.Body>
          </Card>
        </Col>
        <Col>
          <Card>
            <Card.Body>
              <Card.Title>Interactive Chatbot</Card.Title>
              <Card.Text>Ask questions and get instant answers.</Card.Text>
              <Button as={Link} to="/interactiveChatbot" variant="primary">Chat Now</Button>
            </Card.Body>
          </Card>
        </Col>
        <Col>
          <Card>
            <Card.Body>
              <Card.Title>Admin Panel</Card.Title>
              <Card.Text>HR admin actions and approvals.</Card.Text>
              <Button as={Link} to="/adminPanel" variant="primary">Go to Admin Panel</Button>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
}

export default HomePage;