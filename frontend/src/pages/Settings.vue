<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'

const s = ref({})
const drafts = ref({ overlap: '', lining_coefficient: '' })
const err = ref('')
const saved = ref(false)
const busy = ref(false)

onMounted(async () => {
  try {
    s.value = await getJSON('/api/settings')
    drafts.value.overlap = s.value.overlap
    drafts.value.lining_coefficient = s.value.lining_coefficient
  } catch (e) {
    err.value = String(e.message || e)
  }
})

async function save() {
  err.value = ''
  saved.value = false
  busy.value = true
  try {
    const keys = ['overlap', 'lining_coefficient']
    for (const k of keys) {
      if (String(drafts.value[k]) !== String(s.value[k])) {
        s.value = await putJSON(`/api/settings/${k}`, { value: parseFloat(drafts.value[k]) })
      }
    }
    drafts.value.overlap = s.value.overlap
    drafts.value.lining_coefficient = s.value.lining_coefficient
    saved.value = true
  } catch (e) {
    err.value = String(e.message || e)
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="page">
    <h1>设置</h1>
    <p class="lede">
      全局系数对新试算生效；已写入用纸档的记录为当时快照，修改默认不会改变历史单。
    </p>
    <p v-if="err" class="bad">{{ err }}</p>
    <div class="row">
      <label class="coeff-row" style="margin: 0;">
        折边系数 overlap
        <input v-model="drafts.overlap" type="number" step="0.05" min="0" />
      </label>
      <label class="coeff-row" style="margin: 0;">
        里衬系数 lining
        <input v-model="drafts.lining_coefficient" type="number" step="0.05" min="0" />
      </label>
      <button :disabled="busy" @click="save">保存</button>
      <span v-if="saved" class="pill">已保存</span>
    </div>
  </div>
</template>
