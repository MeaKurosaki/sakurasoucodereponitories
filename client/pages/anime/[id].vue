<template>
  <div class="page">
    <div class="container" style="padding-top: 24px;">
      <NuxtLink to="/" class="back-link">← 返回首页</NuxtLink>
      <div v-if="loading" class="loading">🌸 加载中...</div>
      <template v-else-if="anime">
        <div class="anime-detail-header animate-in">
          <div class="anime-detail-cover">
            <img v-if="anime.cover" :src="anime.cover" :alt="anime.title" />
            <span v-else>🌸</span>
          </div>
          <div class="anime-detail-info">
            <h1>{{ anime.title }}</h1>
            <div v-if="anime.alias" class="anime-detail-alias">{{ anime.alias }}</div>
            <div class="anime-detail-meta">
              <span class="badge" :class="'badge-' + anime.status">{{ statusMap[anime.status] }}</span>
              <span class="meta-item">📅 {{ anime.year || '未知' }}</span>
              <span class="meta-item">⭐ {{ anime.rating }}</span>
              <span class="meta-item">🎬 {{ anime.type?.toUpperCase() }}</span>
              <span class="meta-item">🌍 {{ anime.region || '日本' }}</span>
              <span class="meta-item">👁️ {{ (anime.views || 0).toLocaleString() }}</span>
              <span v-if="anime.categories" class="meta-item">🏷️ {{ anime.categories }}</span>
            </div>
            <p class="anime-detail-desc">{{ anime.description || '暂无简介' }}</p>
          </div>
        </div>

        <section class="section animate-in">
          <h2 class="section-title" style="margin-bottom: 16px;">
            📺 全部剧集（共 {{ anime.episodes?.length || 0 }} 集）
          </h2>
          <div class="episode-grid">
            <div
              v-for="ep in anime.episodes"
              :key="ep.id"
              class="episode-btn"
              @click="play(ep.id)"
            >
              第{{ ep.number }}集
            </div>
          </div>
        </section>
      </template>
      <div v-else class="loading">未找到该番剧</div>
    </div>
  </div>
</template>

<script setup>
const route = useRoute()
const router = useRouter()
const anime = ref(null)
const loading = ref(true)

const statusMap = { ongoing: '连载中', completed: '已完结', upcoming: '即将上映' }

async function fetchAnime() {
  try {
    anime.value = await $fetch(`/api/anime/${route.params.id}`)
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function play(episodeId) {
  router.push(`/play/${episodeId}`)
}

fetchAnime()
</script>
