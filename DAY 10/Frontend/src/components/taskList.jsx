import { useState } from 'react';
import ListGroup from 'react-bootstrap/ListGroup';
import Form from 'react-bootstrap/Form';
import ProgressBar from './progressBar';

const initialTasks = [
  { id: 1, text: 'Complete onboarding documents', done: false },
  { id: 2, text: 'Setup work email', done: false },
  { id: 3, text: 'Read HR policies', done: false },
  { id: 4, text: 'Submit ID proof', done: false },
];

function TaskList() {
  const [tasks, setTasks] = useState(initialTasks);
  const completed = tasks.filter(t => t.done).length;
  const percent = Math.round((completed / tasks.length) * 100);

  const toggleTask = (id) => {
    setTasks(tasks.map(task =>
      task.id === id ? { ...task, done: !task.done } : task
    ));
  };

  return (
    <div>
      <h3>Onboarding Task List</h3>
      <ListGroup className="mb-3">
        {tasks.map(task => (
          <ListGroup.Item key={task.id}>
            <Form.Check
              type="checkbox"
              checked={task.done}
              onChange={() => toggleTask(task.id)}
              label={task.text}
            />
          </ListGroup.Item>
        ))}
      </ListGroup>
      <ProgressBar percent={percent} />
      <div className="mt-2">{completed} of {tasks.length} tasks completed</div>
    </div>
  );
}

export default TaskList;
