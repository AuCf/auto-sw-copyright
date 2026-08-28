<script setup lang="ts">
import { ref, watch } from 'vue'
import { useSettingsStore } from '../stores/settings'
import { type LLMSettings } from '../api/client'
import { CheckCircle2, AlertCircle, RefreshCw, Key, Globe, Cpu } from 'lucide-vue-next'

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: boolean): void
}>()

const settingsStore = useSettingsStore()
const form = ref<LLMSettings>({ ...settingsStore.settings })

// Sync when dialog opens
watch(() => props.modelValue, (val) => {
  if (val) {
    form.value = { ...settingsStore.settings }
  }
})

const handleProviderChange = (provider: string) => {
  form.value.provider = provider
  if (provider === 'deepseek') {
    form.value.base_url = 'https://api.deepseek.com/v1'
    form.value.model = 'deepseek-chat'
  } else if (provider === 'openai') {
    form.value.base_url = 'https://api.openai.com/v1'
    form.value.model = 'gpt-4o'
  } else if (provider === 'ollama') {
    form.value.base_url = 'http://127.0.0.1:11434/v1'
    form.value.model = 'qwen2.5-coder:7b'
    form.value.api_key = 'ollama'
  } else if (provider === 'qwen') {
    form.value.base_url = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
    form.value.model = 'qwen-plus'
  }
}

const handleSave = async () => {
  const success = await settingsStore.saveSettings(form.value)
  if (success) {
    emit('update:modelValue', false)
  }
}

const handleTest = async () => {
  await settingsStore.testConnection(form.value)
}
</script>

<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="emit('update:modelValue', $event)"
    title="大语言模型 (LLM) 配置"
    width="560px"
    destroy-on-close
    :append-to-body="true"
    top="12vh"
    class="custom-settings-dialog"
  >
    <div class="space-y-4 py-1">
      <div class="bg-sky-50 border border-sky-100 rounded-lg p-3 text-xs text-sky-800 flex items-start space-x-2">
        <AlertCircle class="w-4 h-4 text-sky-600 mt-0.5 flex-shrink-0" />
        <div>
          推荐使用 <strong>DeepSeek-V3 / DeepSeek-Coder</strong> 或 <strong>GPT-4o</strong>，单次可生成丰富真实的工业级代码与详尽的操作手册。
        </div>
      </div>

      <!-- Quick Preset Providers -->
      <div>
        <label class="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-2">快速选择服务商</label>
        <div class="grid grid-cols-4 gap-2">
          <button
            type="button"
            @click="handleProviderChange('deepseek')"
            :class="[
              'py-2 px-3 rounded-lg text-xs font-medium border text-center transition-all',
              form.provider === 'deepseek'
                ? 'bg-sky-50 border-sky-500 text-sky-700 ring-1 ring-sky-500'
                : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
            ]"
          >
            DeepSeek
          </button>
          <button
            type="button"
            @click="handleProviderChange('openai')"
            :class="[
              'py-2 px-3 rounded-lg text-xs font-medium border text-center transition-all',
              form.provider === 'openai'
                ? 'bg-sky-50 border-sky-500 text-sky-700 ring-1 ring-sky-500'
                : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
            ]"
          >
            OpenAI
          </button>
          <button
            type="button"
            @click="handleProviderChange('qwen')"
            :class="[
              'py-2 px-3 rounded-lg text-xs font-medium border text-center transition-all',
              form.provider === 'qwen'
                ? 'bg-sky-50 border-sky-500 text-sky-700 ring-1 ring-sky-500'
                : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
            ]"
          >
            通义千问
          </button>
          <button
            type="button"
            @click="handleProviderChange('ollama')"
            :class="[
              'py-2 px-3 rounded-lg text-xs font-medium border text-center transition-all',
              form.provider === 'ollama'
                ? 'bg-sky-50 border-sky-500 text-sky-700 ring-1 ring-sky-500'
                : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
            ]"
          >
            本地 Ollama
          </button>
        </div>
      </div>

      <!-- API Key -->
      <div>
        <label class="block text-xs font-medium text-slate-700 mb-1 flex items-center">
          <Key class="w-3.5 h-3.5 mr-1 text-slate-400" />
          API Key
        </label>
        <el-input
          v-model="form.api_key"
          type="password"
          show-password
          placeholder="sk-..."
          clearable
        />
      </div>

      <!-- Base URL -->
      <div>
        <label class="block text-xs font-medium text-slate-700 mb-1 flex items-center">
          <Globe class="w-3.5 h-3.5 mr-1 text-slate-400" />
          API Base URL (OpenAI 兼容接口)
        </label>
        <el-input
          v-model="form.base_url"
          placeholder="https://api.deepseek.com/v1"
          clearable
        />
      </div>

      <!-- Model Name -->
      <div>
        <label class="block text-xs font-medium text-slate-700 mb-1 flex items-center">
          <Cpu class="w-3.5 h-3.5 mr-1 text-slate-400" />
          模型名称 (Model)
        </label>
        <el-input
          v-model="form.model"
          placeholder="deepseek-chat / gpt-4o / qwen-plus"
          clearable
        />
      </div>
    </div>

    <template #footer>
      <div class="flex items-center justify-between pt-2 border-t border-slate-100">
        <el-button
          @click="handleTest"
          :loading="settingsStore.testing"
          type="info"
          plain
        >
          <RefreshCw class="w-3.5 h-3.5 mr-1" />
          测试连接
        </el-button>
        <div class="space-x-2">
          <el-button @click="emit('update:modelValue', false)">取消</el-button>
          <el-button
            type="primary"
            @click="handleSave"
            :loading="settingsStore.loading"
          >
            保存并应用
          </el-button>
        </div>
      </div>
    </template>
  </el-dialog>
</template>
