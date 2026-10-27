<template>
  <div class="page">
    <div class="container" style="padding-top: 24px;">
      <NuxtLink to="/" class="back-link">← 返回首页</NuxtLink>
      <div v-if="loading" class="loading">🌸 加载中...</div>
      <template v-else-if="episode">
        <h1 style="font-size: 22px; font-weight: 700; margin-bottom: 4px;">{{ animeTitle }}</h1>
        <p style="color: var(--text-muted); margin-bottom: 20px;">第{{ episode.number }}集</p>

        <div class="player-wrapper">
          <span style="font-size: 48px;">🌸</span>
          <p>视频播放区域</p>
          <p style="font-size: 13px;">（片源待添加）</p>
        </div>

        <div style="display: flex; gap: 10px; margin-top: 16px;">
          <button v-if="prevEp" class="episode-btn" style="padding: 10px 24px;" @click="goEpisode(prevEp)">
            ← 上一集
          </button>
          <button v-if="nextEp" class="episode-btn" style="padding: 10px 24px;" @click="goEpisode(nextEp)">
            下一集 →
          </button>
        </div>
      </template>
      <div v-else class="loading">未找到该集</div>
    </div>
  </div>
</template>

<script setup>
const route = useRoute()
const router = useRouter()
const episode = ref(null)
const loading = ref(true)
const animeTitle = ref('')
const prevEp = ref(null)
const nextEp = ref(null)

async function fetchEpisode() {
  try {
    episode.value = await $fetch(`/api/episode/${route.params.id}`)
    if (!episode.value) return
    animeTitle.value = episode.value.anime_title || ''
    if (episode.value.anime_id) {
      const eps = await $fetch(`/api/anime/${episode.value.anime_id}/episodes`)
      const idx = eps.findIndex(e => e.id === episode.value.id)
      if (idx > 0) prevEp.value = eps[idx - 1]
      if (idx < eps.length - 1) nextEp.value = eps[idx + 1]
    }
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function goEpisode(ep) {
  router.push(`/play/${ep.id}`)
}

fetchEpisode()
</script>
