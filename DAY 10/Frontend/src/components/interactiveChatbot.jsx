import { useState } from 'react';
import { Card, Form, Button, ListGroup } from 'react-bootstrap';

function InteractiveChatbot() {
  const [messages, setMessages] = useState([
    { from: 'bot', text: 'Hello! How can I help you today?' }
  ]);
  const [input, setInput] = useState('');

  const handleSend = e => {
    e.preventDefault();
    if (!input.trim()) return;
    setMessages([...messages, { from: 'user', text: input }]);
    setInput('');
    // Simulate bot reply
    setTimeout(() => {
      setMessages(msgs => [...msgs, { from: 'bot', text: "I'm just a demo bot!" }]);
    }, 500);
  };

  return (
    <Card style={{ maxWidth: 500, margin: '0 auto' }}>
      <Card.Header>Interactive Chatbot</Card.Header>
      <ListGroup variant="flush" style={{ minHeight: 200 }}>
        {messages.map((msg, idx) => (
          <ListGroup.Item key={idx} className={msg.from === 'user' ? 'text-end' : ''}>
            <strong>{msg.from === 'bot' ? 'Bot' : 'You'}:</strong> {msg.text}
          </ListGroup.Item>
        ))}
      </ListGroup>
      <Card.Body>
        <Form onSubmit={handleSend} className="d-flex">
          <Form.Control
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Type your message..."
          />
          <Button type="submit" variant="primary" className="ms-2">Send</Button>
        </Form>
      </Card.Body>
    </Card>
  );
}

export default InteractiveChatbot;
