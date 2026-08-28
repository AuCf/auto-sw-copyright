<script setup lang="ts">
import { ref, computed } from 'vue'
import { useCopyrightStore } from '../stores/copyright'
import { 
  FileText, 
  Download, 
  Copy, 
  Check, 
  Code2, 
  Layers, 
  CheckCircle2, 
  AlertTriangle 
} from 'lucide-vue-next'
import { ElMessage } from 'element-plus'

const copyrightStore = useCopyrightStore()
const activeTab = ref('all')
const copied = ref(false)

const currentCodeText = computed(() => {
  if (activeTab.value === 'all') {
    return copyrightStore.fullCode
  }
  return copyrightStore.layerResults[activeTab.value]?.code || ''
})

const handleCopy = async () => {
  if (!currentCodeText.value) return
  try {
    await navigator.clipboard.writeText(currentCodeText.value)
    copied.value = true
    ElMessage.success('代码已复制到剪贴板')
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (e) {
    ElMessage.error('复制失败')
  }
}
</script>

<template>
  <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col h-[700px]">
    <!-- Top Bar with Stats & Actions -->
    <div class="p-4 border-b border-slate-200 bg-slate-50/50 flex flex-wrap items-center justify-between gap-3">
      <!-- Left: Stats -->
      <div class="flex items-center space-x-4">
        <div class="flex items-center space-x-2">
          <Code2 class="w-5 h-5 text-sky-600" />
          <span class="text-sm font-semibold text-slate-800">业务源代码预览</span>
        </div>

        <div class="flex items-center space-x-3 text-xs">
          <span class="px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 text-slate-700 font-mono">
            总行数: <strong class="text-sky-600 font-bold">{{ copyrightStore.totalCodeLines }}</strong> 行
          </span>

          <span 
            :class="[
              'px-2.5 py-1 rounded-md border flex items-center space-x-1',
              copyrightStore.totalCodeLines >= 3000
                ? 'bg-emerald-50 border-emerald-200 text-emerald-700'
                : 'bg-amber-50 border-amber-200 text-amber-700'
            ]"
          >
            <CheckCircle2 v-if="copyrightStore.totalCodeLines >= 3000" class="w-3.5 h-3.5 text-emerald-600" />
            <AlertTriangle v-else class="w-3.5 h-3.5 text-amber-600" />
            <span>{{ copyrightStore.totalCodeLines >= 3000 ? '已达标 60 页 (>=3000行)' : `约 ${copyrightStore.estimatedCodePages} 页 (建议>=3000行)` }}</span>
          </span>
        </div>
      </div>

      <!-- Right: Action Buttons -->
      <div class="flex items-center space-x-2">
        <button
          @click="handleCopy"
          class="inline-flex items-center space-x-1 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-700 bg-white hover:bg-slate-50 border border-slate-300 shadow-sm transition-all"
        >
          <Check v-if="copied" class="w-3.5 h-3.5 text-emerald-600" />
          <Copy v-else class="w-3.5 h-3.5 text-slate-500" />
          <span>{{ copied ? '已复制' : '复制代码' }}</span>
        </button>

        <button
          @click="copyrightStore.downloadCodeDocx"
          :disabled="copyrightStore.isExporting || !copyrightStore.fullCode"
          class="inline-flex items-center space-x-1 px-3.5 py-1.5 rounded-lg text-xs font-medium text-white bg-sky-600 hover:bg-sky-700 shadow-sm transition-all disabled:opacity-50"
        >
          <Download class="w-3.5 h-3.5" />
          <span>导出 60 页代码 (.docx)</span>
        </button>
      </div>
    </div>

    <!-- Layer Switcher Tabs -->
    <div class="px-4 py-2 border-b border-slate-100 bg-white flex items-center space-x-2 overflow-x-auto text-xs">
      <button
        @click="activeTab = 'all'"
        :class="[
          'px-3 py-1.5 rounded-lg font-medium transition-all flex items-center space-x-1.5',
          activeTab === 'all'
            ? 'bg-sky-50 text-sky-700 border border-sky-200'
            : 'text-slate-600 hover:bg-slate-100 border border-transparent'
        ]"
      >
        <Layers class="w-3.5 h-3.5" />
        <span>全部代码流 (完整 3500+ 行)</span>
      </button>

      <button
        v-for="(layer, key) in copyrightStore.layerResults"
        :key="key"
        @click="activeTab = key as string"
        :class="[
          'px-3 py-1.5 rounded-lg font-medium transition-all flex items-center space-x-1.5',
          activeTab === key
            ? 'bg-sky-50 text-sky-700 border border-sky-200'
            : 'text-slate-600 hover:bg-slate-100 border border-transparent'
        ]"
      >
        <span>{{ layer.display_name }}</span>
        <span class="text-[10px] px-1.5 py-0.2 rounded bg-slate-200 text-slate-600">{{ layer.lines_count }}行</span>
      </button>
    </div>

    <!-- Code Editor / Box -->
    <div class="flex-1 bg-slate-900 overflow-auto p-4 font-mono text-xs leading-relaxed text-slate-300">
      <pre class="whitespace-pre"><code>{{ currentCodeText || '// 暂无代码，请先点击流水线生成' }}</code></pre>
    </div>
  </div>
</template>
