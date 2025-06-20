import { useState } from 'react';
import { Form, Button, Alert } from 'react-bootstrap';

function FeedbackForm() {
  const [form, setForm] = useState({ name: '', email: '', feedback: '' });
  const [submitted, setSubmitted] = useState(false);

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = e => {
    e.preventDefault();
    setSubmitted(true);
    // Normally, send to backend here
  };

  return (
    <div>
      <h3>Feedback Form</h3>
      {submitted && <Alert variant="success">Thank you for your feedback!</Alert>}
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="feedbackName">
          <Form.Label>Name</Form.Label>
          <Form.Control type="text" name="name" value={form.name} onChange={handleChange} required />
        </Form.Group>
        <Form.Group className="mb-3" controlId="feedbackEmail">
          <Form.Label>Email</Form.Label>
          <Form.Control type="email" name="email" value={form.email} onChange={handleChange} required />
        </Form.Group>
        <Form.Group className="mb-3" controlId="feedbackText">
          <Form.Label>Feedback</Form.Label>
          <Form.Control as="textarea" rows={3} name="feedback" value={form.feedback} onChange={handleChange} required />
        </Form.Group>
        <Button type="submit" variant="primary">Submit</Button>
      </Form>
    </div>
  );
}

export default FeedbackForm;
