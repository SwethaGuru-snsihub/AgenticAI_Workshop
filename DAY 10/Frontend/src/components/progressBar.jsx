import RBProgressBar from 'react-bootstrap/ProgressBar';

function ProgressBar({ percent }) {
  return (
    <RBProgressBar now={percent} label={`${percent}%`} />
  );
}

export default ProgressBar;
