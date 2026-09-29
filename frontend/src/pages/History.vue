<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'

const items = ref([])
const err = ref('')

onMounted(async () => {
  try {
    items.value = (await getJSON('/api/runs')).items
  } catch (e) {
    err.value = String(e.message || e)
  }
})
</script>

<template>
  <div class="page">
    <h1>用纸档</h1>
    <p class="lede">算纸页「写入用纸档」后的落库结果，按次保留盒名与外／里两路面积。</p>
    <p v-if="err" class="bad">{{ err }}</p>
    <p v-else-if="!items.length" class="empty">还没有写入过。先去算纸试一单。</p>
    <ul v-else class="item-list">
      <li v-for="r in items" :key="r.id">
        <router-link class="run-link" :to="`/runs/${r.id}`">
          <span>
            {{ r.box_name }}
            <span v-if="r.result?.double_layer" class="pill">双层</span>
          </span>
          <span class="meta">
            外 {{ r.result?.outer_paper_m2 ?? r.result?.paper_m2 ?? '—' }}
            ／ 里 {{ r.result?.inner_paper_m2 ?? 0 }}
            ／ 合计 {{ r.result?.total_paper_m2 ?? r.result?.paper_m2 ?? '—' }} m²
          </span>
        </router-link>
      </li>
    </ul>
  </div>
</template>
