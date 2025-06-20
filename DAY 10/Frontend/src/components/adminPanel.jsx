import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/Button';

const users = [
  { id: 1, name: 'Swetha', role: 'Employee', status: 'Active' },
  { id: 2, name: 'Afrin', role: 'Manager', status: 'Pending' },
  { id: 3, name: 'Maddy', role: 'Employee', status: 'Active' },
];

function AdminPanel() {
  return (
    <div>
      <h3>Admin Panel for HR</h3>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>#</th>
            <th>Name</th>
            <th>Role</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.name}</td>
              <td>{user.role}</td>
              <td>{user.status}</td>
              <td>
                <Button variant="outline-primary" size="sm" disabled={user.status === 'Active'}>
                  Approve
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
}

export default AdminPanel;
