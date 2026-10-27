CREATE DATABASE IF NOT EXISTS sakurasou DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE sakurasou;

-- 动漫分类
CREATE TABLE IF NOT EXISTS categories (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  slug VARCHAR(50) NOT NULL UNIQUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 动漫番剧
CREATE TABLE IF NOT EXISTS animes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  alias VARCHAR(255) DEFAULT '',
  cover VARCHAR(500) DEFAULT '',
  description TEXT,
  rating DECIMAL(3,1) DEFAULT 0.0,
  year INT DEFAULT NULL,
  status ENUM('ongoing', 'completed', 'upcoming') DEFAULT 'ongoing',
  region VARCHAR(50) DEFAULT '日本',
  type ENUM('tv', 'movie', 'ova', 'ona', 'special') DEFAULT 'tv',
  episodes_total INT DEFAULT 0,
  views INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_status (status),
  INDEX idx_views (views DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 动漫-分类关联
CREATE TABLE IF NOT EXISTS anime_categories (
  anime_id INT NOT NULL,
  category_id INT NOT NULL,
  PRIMARY KEY (anime_id, category_id),
  FOREIGN KEY (anime_id) REFERENCES animes(id) ON DELETE CASCADE,
  FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 分集
CREATE TABLE IF NOT EXISTS episodes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  anime_id INT NOT NULL,
  number INT NOT NULL,
  title VARCHAR(255) DEFAULT '',
  video_url VARCHAR(1000) DEFAULT '',
  duration INT DEFAULT 0,
  views INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (anime_id) REFERENCES animes(id) ON DELETE CASCADE,
  INDEX idx_anime_number (anime_id, number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 用户
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  email VARCHAR(100) DEFAULT NULL,
  avatar VARCHAR(500) DEFAULT '',
  role ENUM('user', 'admin') DEFAULT 'user',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 观看历史
CREATE TABLE IF NOT EXISTS watch_history (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  anime_id INT NOT NULL,
  episode_id INT NOT NULL,
  progress INT DEFAULT 0,
  completed BOOLEAN DEFAULT FALSE,
  watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (anime_id) REFERENCES animes(id) ON DELETE CASCADE,
  FOREIGN KEY (episode_id) REFERENCES episodes(id) ON DELETE CASCADE,
  INDEX idx_user (user_id),
  INDEX idx_user_anime (user_id, anime_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 收藏
CREATE TABLE IF NOT EXISTS favorites (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  anime_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (anime_id) REFERENCES animes(id) ON DELETE CASCADE,
  UNIQUE KEY uk_user_anime (user_id, anime_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入默认分类
INSERT INTO categories (name, slug) VALUES
('热血', 'action'),
('恋爱', 'romance'),
('搞笑', 'comedy'),
('奇幻', 'fantasy'),
('科幻', 'sci-fi'),
('悬疑', 'mystery'),
('日常', 'slice-of-life'),
('校园', 'school'),
('冒险', 'adventure'),
('后宫', 'harem'),
('百合', 'yuri'),
('耽美', 'yaoi'),
('机战', 'mecha'),
('运动', 'sports'),
('音乐', 'music')
ON DUPLICATE KEY UPDATE name=VALUES(name);
