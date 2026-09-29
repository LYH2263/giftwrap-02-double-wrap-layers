<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'

const props = defineProps({ id: { type: String, required: true } })
const run = ref(null)
const err = ref('')

onMounted(async () => {
  try {
    run.value = await getJSON(`/api/runs/${props.id}`)
  } catch (e) {
    err.value = String(e.message || e)
  }
})
</script>

<template>
  <div class="page">
    <h1>用纸档 #{{ id }}</h1>
    <p class="lede">以下为写入当时的落库快照；之后修改全局系数不会改变本单。</p>
    <p v-if="err" class="bad">{{ err }}</p>
    <template v-else-if="run">
      <div class="row">
        <strong>{{ run.box_name }}</strong>
        <span class="pill">
          {{ run.result?.double_layer ? '双层用纸' : '单层用纸' }}
        </span>
        <span class="meta">{{ run.created_at }}</span>
      </div>
      <div class="result-board">
        <div class="layer-grid">
          <div class="layer">
            <p class="layer-tag">外层纸</p>
            <p class="layer-val">{{ run.result?.outer_paper_m2 }}<small> m²</small></p>
            <p class="meta">六面 × 折边系数 ×{{ run.result?.overlap ?? run.overlap }}</p>
          </div>
          <div class="layer" :class="{ muted: !run.result?.double_layer }">
            <p class="layer-tag">里衬纸</p>
            <p class="layer-val">{{ run.result?.inner_paper_m2 }}<small> m²</small></p>
            <p class="meta">
              {{ run.result?.double_layer ? `六面表面积 × 系数 ×${run.result?.lining_coefficient}` : '未启用' }}
            </p>
          </div>
        </div>
        <div class="figure">{{ run.result?.total_paper_m2 }}<span>m² 合计</span></div>
        <p class="stat-line" v-if="run.result?.ribbon">
          十字丝带约 {{ run.result.ribbon.ribbon_m ?? run.result.ribbon }} m（仅外层三边）
        </p>
      </div>
      <p v-if="run.note" class="stat-line">备注：{{ run.note }}</p>
      <div class="row" style="margin-top: 1.25rem;">
        <router-link class="btn ghost" to="/history">返回用纸档</router-link>
        <router-link class="btn" to="/bench">去算纸台同参复算</router-link>
      </div>
    </template>
  </div>
</template>
