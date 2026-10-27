export default defineNuxtConfig({
  compatibilityDate: '2026-05-12',
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  app: {
    head: {
      title: '樱花庄 - Sakurasou',
      meta: [
        { name: 'description', content: '樱花庄动漫 - 免费在线动漫观看' }
      ]
    }
  }
})
