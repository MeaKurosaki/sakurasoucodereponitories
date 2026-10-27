const express = require('express');
const router = express.Router();
const pool = require('../config/db');

router.get('/:id', async (req, res) => {
  try {
    const [episodes] = await pool.query(
      `SELECT e.*, a.title as anime_title, a.cover as anime_cover
       FROM episodes e
       JOIN animes a ON e.anime_id = a.id
       WHERE e.id = ?`,
      [req.params.id]
    );
    if (episodes.length === 0) {
      return res.status(404).json({ error: '未找到' });
    }

    await pool.query('UPDATE episodes SET views = views + 1 WHERE id = ?', [req.params.id]);
    res.json(episodes[0]);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: '服务器错误' });
  }
});

module.exports = router;
