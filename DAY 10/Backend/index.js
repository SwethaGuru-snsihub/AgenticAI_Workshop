const express = require('express');
const cors = require('cors');
const app = express();
const aiRoutes = require('./routes/aiRoutes');

// app.listen (5000, () => {
//     console.log('Server is running on port 5000 Successfully');
// });

app.use(cors());
app.use(express.json());
app.use('/api', aiRoutes);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
