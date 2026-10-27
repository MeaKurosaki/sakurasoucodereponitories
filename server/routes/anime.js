const express = require('express');
const router = express.Router();
const pool = require('../config/db');

router.get('/', async (req, res) => {
  try {
    const { page = 1, limit = 20, category, status, sort = 'created_at', order = 'DESC' } = req.query;
    const offset = (page - 1) * limit;
    let sql = `SELECT a.*, GROUP_CONCAT(c.name SEPARATOR ', ') as categories
               FROM animes a
               LEFT JOIN anime_categories ac ON a.id = ac.anime_id
               LEFT JOIN categories c ON ac.category_id = c.id`;
    const params = [];
    const where = [];

    if (category) {
      where.push('c.slug = ?');
      params.push(category);
    }
    if (status) {
      where.push('a.status = ?');
      params.push(status);
    }

    if (where.length > 0) {
      sql += ' WHERE ' + where.join(' AND ');
    }

    sql += ' GROUP BY a.id';
    sql += ` ORDER BY a.${sort} ${order}`;
    sql += ' LIMIT ? OFFSET ?';
    params.push(Number(limit), offset);

    const [rows] = await pool.query(sql, params);

    const [countResult] = await pool.query('SELECT COUNT(*) as total FROM animes');
    res.json({
      data: rows,
      total: countResult[0].total,
      page: Number(page),
      limit: Number(limit)
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: '服务器错误' });
  }
});

router.get('/:id', async (req, res) => {
  try {
    const [animes] = await pool.query(
      `SELECT a.*, GROUP_CONCAT(c.name SEPARATOR ', ') as categories
       FROM animes a
       LEFT JOIN anime_categories ac ON a.id = ac.anime_id
       LEFT JOIN categories c ON ac.category_id = c.id
       WHERE a.id = ?
       GROUP BY a.id`,
      [req.params.id]
    );
    if (animes.length === 0) {
      return res.status(404).json({ error: '未找到' });
    }
    const [episodes] = await pool.query(
      'SELECT id, number, title, duration, views, created_at FROM episodes WHERE anime_id = ? ORDER BY number ASC',
      [req.params.id]
    );
    res.json({ ...animes[0], episodes });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: '服务器错误' });
  }
});

router.get('/:id/episodes', async (req, res) => {
  try {
    const [episodes] = await pool.query(
      'SELECT id, number, title, duration, views, created_at FROM episodes WHERE anime_id = ? ORDER BY number ASC',
      [req.params.id]
    );
    res.json(episodes);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: '服务器错误' });
  }
});

module.exports = router;
