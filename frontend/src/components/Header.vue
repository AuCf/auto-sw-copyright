<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSettingsStore } from '../stores/settings'
import SettingsModal from './SettingsModal.vue'
import { 
  FileCode2, 
  Settings, 
  Sparkles, 
} from 'lucide-vue-next'

const settingsStore = useSettingsStore()
const showSettings = ref(false)

onMounted(() => {
  settingsStore.fetchSettings()
})
</script>

<template>
  <header class="bg-white border-b border-slate-200 sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <!-- Left: Logo & Title -->
      <div class="flex items-center space-x-3">
        <div class="w-9 h-9 rounded-lg bg-slate-900 flex items-center justify-center text-white shadow-sm">
          <FileCode2 class="w-4 h-4 text-slate-100" />
        </div>
        <div>
          <div class="flex items-center space-x-2">
            <h1 class="text-base font-semibold text-slate-900 tracking-tight">AutoCopyright-AI</h1>
            <span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-medium bg-slate-100 text-slate-700 border border-slate-200">
              <Sparkles class="w-2.5 h-2.5 mr-1 text-slate-500" />
              CPCC 申报过审版
            </span>
          </div>
          <p class="text-[11px] text-slate-500 hidden sm:block">中国软件著作权全套申报资料一键生成系统</p>
        </div>
      </div>

      <!-- Right: Model indicator & Action Buttons -->
      <div class="flex items-center space-x-3">
        <div class="hidden md:flex items-center space-x-2 px-2.5 py-1 rounded-md bg-slate-50 border border-slate-200 text-xs text-slate-600">
          <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
          <span>模型: <strong class="text-slate-800 font-medium font-mono">{{ settingsStore.settings.model }}</strong></span>
        </div>

        <button
          @click="showSettings = true"
          class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-700 bg-white hover:bg-slate-50 border border-slate-200 shadow-sm transition-all"
        >
          <Settings class="w-3.5 h-3.5 text-slate-500" />
          <span>模型与 API 配置</span>
        </button>
      </div>
    </div>

    <!-- Settings Dialog Modal -->
    <SettingsModal v-model="showSettings" />
  </header>
</template>
