export default defineEventHandler(async (event) => {
  const slug = getRouterParam(event, 'slug') || ''
  const path = slug || ''
  const query = getQuery(event)
  const qs = new URLSearchParams()
  for (const [k, v] of Object.entries(query)) {
    qs.set(k, String(v))
  }
  const target = `http://localhost:3001/api/${path}${qs.toString() ? '?' + qs.toString() : ''}`

  try {
    return await $fetch(target, {
      method: event.method,
      headers: getRequestHeaders(event),
      body: ['GET', 'HEAD'].includes(event.method) ? undefined : await readBody(event)
    })
  } catch (e) {
    const status = e?.response?.status || 502
    setResponseStatus(event, status)
    return e?.response?._data || { error: 'Backend unavailable' }
  }
})
