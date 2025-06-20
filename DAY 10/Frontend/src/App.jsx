import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Header from './layouts/header.jsx'
import HomePage from './pages/homePage.jsx'
import TaskList from "./layouts/components/taskList.jsx";
import FeedbackForm from "./layouts/components/feedbackForm.jsx";
import InteractiveChatbot from "./layouts/components/interactiveChatbot.jsx";
import AdminPanel from "./layouts/components/adminPanel.jsx";
import './App.css'
import { Container } from 'react-bootstrap';

function App() {
  return (
    <Router>
      <Header />
      <Container className="mt-4">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/task-list" element={<TaskList />} />
          <Route path="/feedback-form" element={<FeedbackForm />} />
          <Route path="/interactiveChatbot" element={<InteractiveChatbot />} />
          <Route path="/adminPanel" element={<AdminPanel />} />
        </Routes>
      </Container>
    </Router>
  )
}

export default App
