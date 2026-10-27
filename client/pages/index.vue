<template>
  <div class="index-page">
    <div ref="entryRef" class="entry-section">
      <video
        class="entry-video"
        src="http://localhost:3001/static/enterpage1.mp4"
        autoplay
        muted
        loop
        playsinline
      />
      <div class="entry-overlay" />
      <div class="entry-content">
        <div class="entry-title">
          <h1>🌸 樱花庄</h1>
          <p>Sakurasou</p>
        </div>
        <div class="scroll-hint" @click="scrollDown">
          <span class="scroll-text">上滑进入</span>
          <span class="scroll-arrow">↓</span>
        </div>
      </div>
    </div>

    <div class="main-section">
      <div class="page-bg" style="background-image: url('http://localhost:3001/assets/page2.png');" />
      <div class="page">
        <div class="container" style="padding-top: 20px;">
          <div class="categories-bar">
            <NuxtLink
              v-for="cat in categories"
              :key="cat.slug"
              :to="`/category/${cat.slug}`"
              class="category-chip"
            >
              {{ cat.name }}
            </NuxtLink>
          </div>

          <section class="section">
            <div class="section-header">
              <h2 class="section-title">🔥 热门推荐</h2>
              <NuxtLink to="/category/action" class="see-all">查看全部 →</NuxtLink>
            </div>
            <div v-if="loading" class="loading">🌸 加载中...</div>
            <div v-else class="anime-grid">
              <div v-for="anime in animeList" :key="anime.id" class="anime-card animate-in" @click="goAnime(anime.id)">
                <div class="anime-card-cover">
                  <img v-if="anime.cover" :src="anime.cover" :alt="anime.title" loading="lazy" />
                  <span v-else>🌸</span>
                </div>
                <div class="anime-card-body">
                  <div class="anime-card-title">{{ anime.title }}</div>
                  <div class="anime-card-meta">
                    <span :class="['anime-card-badge', anime.status]">{{ getStatusBadge(anime.status) }}</span>
                    <span>{{ anime.year }}</span>
                    <span>⭐ {{ anime.rating }}</span>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <section class="section">
            <div class="section-header">
              <h2 class="section-title">📺 正在连载</h2>
            </div>
            <div v-if="loadingOngoing" class="loading">🌸 加载中...</div>
            <div v-else class="anime-grid">
              <div v-for="anime in ongoingList" :key="anime.id" class="anime-card animate-in" @click="goAnime(anime.id)">
                <div class="anime-card-cover">
                  <img v-if="anime.cover" :src="anime.cover" :alt="anime.title" loading="lazy" />
                  <span v-else>🌸</span>
                </div>
                <div class="anime-card-body">
                  <div class="anime-card-title">{{ anime.title }}</div>
                  <div class="anime-card-meta">
                    <span :class="['anime-card-badge', anime.status]">{{ getStatusBadge(anime.status) }}</span>
                    <span>⭐ {{ anime.rating }}</span>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const router = useRouter()
const entryRef = ref(null)
const animeList = ref([])
const ongoingList = ref([])
const categories = ref([])
const loading = ref(true)
const loadingOngoing = ref(true)

function scrollDown() {
  window.scrollTo({ top: window.innerHeight, behavior: 'smooth' })
}

async function fetchData() {
  try {
    const [animeRes, ongoingRes, catRes] = await Promise.all([
      $fetch('/api/anime?sort=views&limit=24'),
      $fetch('/api/anime?status=ongoing&sort=created_at&limit=12'),
      $fetch('/api/categories')
    ])
    animeList.value = animeRes.data || []
    ongoingList.value = ongoingRes.data || []
    categories.value = catRes || []
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
    loadingOngoing.value = false
  }
}

function getStatusBadge(status) {
  const map = { ongoing: '连载中', completed: '已完结', upcoming: '即将上映' }
  return map[status] || status
}

function goAnime(id) {
  router.push(`/anime/${id}`)
}

fetchData()
</script>

<style scoped>
.index-page {
  position: relative;
}

.entry-section {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.entry-video {
  position: absolute;
  top: 50%;
  left: 50%;
  min-width: 100%;
  min-height: 100%;
  width: auto;
  height: auto;
  transform: translate(-50%, -50%);
  object-fit: cover;
}

.entry-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.35);
}

.entry-content {
  position: relative;
  z-index: 2;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  height: 60vh;
  padding: 80px 24px 40px;
}

.entry-title h1 {
  font-size: 52px;
  font-weight: 800;
  color: #fff;
  text-shadow: 0 2px 20px rgba(0,0,0,0.3);
  letter-spacing: -1px;
}

.entry-title p {
  font-size: 16px;
  color: rgba(255,255,255,0.7);
  letter-spacing: 4px;
  text-transform: uppercase;
  margin-top: 4px;
}

.scroll-hint {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  animation: fadeUpDown 2s ease-in-out infinite;
}

.scroll-text {
  font-size: 14px;
  color: rgba(255,255,255,0.6);
  letter-spacing: 2px;
}

.scroll-arrow {
  font-size: 28px;
  color: rgba(255,255,255,0.8);
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(10px); }
}

@keyframes fadeUpDown {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}

.main-section {
  position: relative;
  min-height: 100vh;
}

.page-bg {
  position: fixed;
  inset: 0;
  z-index: -1;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  opacity: 0.3;
  pointer-events: none;
}

.page {
  position: relative;
  z-index: 1;
  flex: 1;
  padding-bottom: 48px;
}
</style>
