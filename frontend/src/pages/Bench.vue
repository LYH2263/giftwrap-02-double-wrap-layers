<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
import BoxUnfold from '../components/BoxUnfold.vue'

const boxes = ref([])
const bid = ref(1)
const doubleLayer = ref(false)
const lining = ref('')
const defaults = ref({ lining_coefficient: '1.0' })
const out = ref(null)
const err = ref('')
const busy = ref(false)

onMounted(async () => {
  try {
    boxes.value = (await getJSON('/api/boxes')).items.filter((b) => b.data_quality === 'clean')
    if (boxes.value.length) bid.value = boxes.value[0].id
    defaults.value = await getJSON('/api/settings')
  } catch (e) {
    err.value = String(e.message || e)
  }
})

function buildParams(forSave) {
  const params = { box_id: bid.value, double_layer: doubleLayer.value }
  if (doubleLayer.value && lining.value !== '') {
    params.lining_coefficient = parseFloat(lining.value)
  }
  if (forSave) params.save = true
  return params
}

async function go(save) {
  err.value = ''
  out.value = null
  busy.value = true
  try {
    if (save) {
      out.value = await postJSON('/api/estimate', buildParams(true))
    } else {
      const q = new URLSearchParams()
      Object.entries(buildParams(false)).forEach(([k, v]) => q.set(k, String(v)))
      out.value = await getJSON(`/api/estimate?${q.toString()}`)
    }
  } catch (e) {
    err.value = String(e.message || e)
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="page">
    <h1>算纸</h1>
    <p class="lede">先试算看面积与展开，确认后再写入用纸档。双层时里衬按六面表面积 × 里衬系数另计一列。</p>
    <div class="row">
      <select v-model.number="bid">
        <option v-for="b in boxes" :key="b.id" :value="b.id">{{ b.name }}</option>
      </select>
      <button :disabled="busy" @click="go(false)">试算</button>
      <button class="ribbon" :disabled="busy" @click="go(true)">写入用纸档</button>
    </div>
    <label class="toggle-row">
      <input v-model="doubleLayer" type="checkbox" />
      双层用纸（外层纸 ＋ 里衬纸）
    </label>
    <label v-if="doubleLayer" class="coeff-row">
      里衬系数
      <input v-model="lining" type="number" step="0.05" min="0" placeholder="留空用全局默认" />
      <span class="meta">
        默认 {{ defaults.lining_coefficient }}；须 &gt; 0；里衬面积 ＝ 六面表面积 × 系数
      </span>
    </label>
    <p v-if="err" class="bad">{{ err }}</p>
    <div v-if="out" class="result-board">
      <div class="layer-grid">
        <div class="layer">
          <p class="layer-tag">外层纸</p>
          <p class="layer-val">{{ out.outer_paper_m2 ?? out.paper_m2 }}<small> m²</small></p>
          <p class="meta">六面 × 折边系数 ×{{ out.overlap }}</p>
        </div>
        <div class="layer" :class="{ muted: !out.double_layer }">
          <p class="layer-tag">里衬纸</p>
          <p class="layer-val">{{ out.inner_paper_m2 }}<small> m²</small></p>
          <p class="meta">
            {{ out.double_layer ? `六面表面积 × 系数 ×${out.lining_coefficient}` : '未启用' }}
          </p>
        </div>
      </div>
      <div class="figure">{{ out.total_paper_m2 }}<span>m² 合计</span></div>
      <p class="stat-line" v-if="out.ribbon">
        十字丝带约 {{ out.ribbon.ribbon_m ?? out.ribbon }} m（仅外层三边）
      </p>
      <BoxUnfold
        :l="out.box.length"
        :w="out.box.width"
        :h="out.box.height"
        :paper-m2="out.outer_paper_m2 ?? out.paper_m2"
      />
    </div>
  </div>
</template>
