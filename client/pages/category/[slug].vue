<template>
  <div class="page">
    <div class="container" style="padding-top: 24px;">
      <NuxtLink to="/" class="back-link">← 返回首页</NuxtLink>
      <h1 class="section-title" style="margin-bottom: 20px;">
        {{ categoryName || '分类浏览' }}
      </h1>

      <div class="categories-bar" style="justify-content: flex-start;">
        <NuxtLink
          v-for="cat in categories"
          :key="cat.slug"
          :to="`/category/${cat.slug}`"
          class="category-chip"
          :class="{ active: cat.slug === route.params.slug }"
        >
          {{ cat.name }}
        </NuxtLink>
      </div>

      <div v-if="loading" class="loading">🌸 加载中...</div>
      <div v-else-if="animeList.length === 0" class="loading">暂无内容</div>
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

      <div v-if="totalPages > 1" class="pagination">
        <button :disabled="page <= 1" @click="changePage(page - 1)">上一页</button>
        <button :disabled="page >= totalPages" @click="changePage(page + 1)">下一页</button>
      </div>
    </div>
  </div>
</template>

<script setup>
const route = useRoute()
const router = useRouter()
const animeList = ref([])
const categories = ref([])
const categoryName = ref('')
const loading = ref(true)
const page = ref(1)
const totalPages = ref(1)

async function fetchData() {
  loading.value = true
  try {
    const [animeRes, catRes] = await Promise.all([
      $fetch(`/api/anime?category=${route.params.slug}&page=${page.value}&limit=30`),
      $fetch('/api/categories')
    ])
    animeList.value = animeRes.data || []
    categories.value = catRes || []
    const cat = categories.value.find(c => c.slug === route.params.slug)
    categoryName.value = cat?.name || route.params.slug
    totalPages.value = Math.ceil((animeRes.total || 0) / (animeRes.limit || 30))
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function changePage(p) {
  page.value = p
  fetchData()
}

function goAnime(id) {
  router.push(`/anime/${id}`)
}

watch(() => route.params.slug, fetchData)
fetchData()
</script>
