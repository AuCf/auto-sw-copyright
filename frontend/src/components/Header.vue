<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSettingsStore } from '../stores/settings'
import SettingsModal from './SettingsModal.vue'
import { 
  FileCode2, 
  Settings, 
  Sparkles, 
  ShieldCheck, 
  ExternalLink,
  Github
} from 'lucide-vue-next'

const settingsStore = useSettingsStore()
const showSettings = ref(false)

onMounted(() => {
  settingsStore.fetchSettings()
})
</script>

<template>
  <header class="bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <!-- Left: Logo & Title -->
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-600 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-sky-500/20">
          <FileCode2 class="w-5 h-5" />
        </div>
        <div>
          <div class="flex items-center space-x-2">
            <h1 class="text-lg font-bold text-slate-900 tracking-tight">AutoCopyright-AI</h1>
            <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold bg-sky-100 text-sky-700 border border-sky-200">
              <Sparkles class="w-3 h-3 mr-1 text-sky-500" />
              CPCC 智能过审版
            </span>
          </div>
          <p class="text-xs text-slate-500 hidden sm:block">中国软件著作权全套材料一键流水线合成系统</p>
        </div>
      </div>

      <!-- Right: Model indicator & Action Buttons -->
      <div class="flex items-center space-x-3">
        <div class="hidden md:flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-100/80 border border-slate-200/60 text-xs text-slate-600">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>当前模型: <strong class="text-slate-800 font-medium">{{ settingsStore.settings.model }}</strong></span>
        </div>

        <button
          @click="showSettings = true"
          class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-sm font-medium text-slate-700 bg-white hover:bg-slate-50 border border-slate-300 shadow-sm transition-all hover:border-slate-400"
        >
          <Settings class="w-4 h-4 text-slate-500" />
          <span>模型配置</span>
        </button>
      </div>
    </div>

    <!-- Settings Dialog Modal -->
    <SettingsModal v-model="showSettings" />
  </header>
</template>
