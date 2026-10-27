<template>
  <div class="page">
    <div class="container" style="padding-top: 24px;">
      <NuxtLink to="/" class="back-link">← 返回首页</NuxtLink>
      <h1 class="section-title" style="margin-bottom: 20px;">
        🔍 搜索结果：{{ query }}
      </h1>
      <div v-if="loading" class="loading">🌸 搜索中...</div>
      <div v-else-if="animeList.length === 0" class="loading">未找到相关结果</div>
      <div v-else class="anime-grid">
        <div v-for="anime in animeList" :key="anime.id" class="anime-card animate-in" @click="goAnime(anime.id)">
          <div class="anime-card-cover">
            <img v-if="anime.cover" :src="anime.cover" :alt="anime.title" loading="lazy" />
            <span v-else>🌸</span>
          </div>
          <div class="anime-card-body">
            <div class="anime-card-title">{{ anime.title }}</div>
            <div class="anime-card-meta">
              <span>⭐ {{ anime.rating }}</span>
              <span>{{ anime.year }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const route = useRoute()
const router = useRouter()
const animeList = ref([])
const loading = ref(true)

const query = computed(() => route.query.q || '')

async function search() {
  if (!query.value) return
  loading.value = true
  try {
    animeList.value = await $fetch(`/api/anime/search?q=${encodeURIComponent(query.value)}`)
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function goAnime(id) {
  router.push(`/anime/${id}`)
}

watch(() => route.query.q, search)
search()
</script>
