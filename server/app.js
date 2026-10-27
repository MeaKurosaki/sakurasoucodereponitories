const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
require('dotenv').config();

const animeRoutes = require('./routes/anime');
const episodeRoutes = require('./routes/episode');
const categoriesRoutes = require('./routes/categories');
const searchRoutes = require('./routes/search');
const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(morgan('dev'));
app.use(express.json());

app.use('/api/anime/search', searchRoutes);
app.use('/api/anime', animeRoutes);
app.use('/api/episode', episodeRoutes);
app.use('/api/categories', categoriesRoutes);

app.use('/static', express.static('D:\\Videos'));
app.use('/assets', express.static('D:\\Pictures'));

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', time: new Date().toISOString() });
});

app.listen(PORT, () => {
  console.log(`🌸 Sakurasou server running on http://localhost:${PORT}`);
});
