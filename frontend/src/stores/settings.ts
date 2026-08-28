import { defineStore } from 'pinia'
import { ref } from 'vue'
import { api, type LLMSettings } from '../api/client'
import { ElMessage } from 'element-plus'

export const useSettingsStore = defineStore('settings', () => {
  const settings = ref<LLMSettings>({
    provider: 'deepseek',
    api_key: '',
    base_url: 'https://api.deepseek.com/v1',
    model: 'deepseek-chat',
    temperature: 0.7,
    max_tokens: 4096,
  })

  const loading = ref(false)
  const testing = ref(false)

  const fetchSettings = async () => {
    try {
      loading.value = true
      const data = await api.getSettings()
      settings.value = data
    } catch (e: any) {
      console.warn('Load settings failed, using defaults')
    } finally {
      loading.value = false
    }
  }

  const saveSettings = async (newSettings: LLMSettings) => {
    try {
      loading.value = true
      await api.updateSettings(newSettings)
      settings.value = { ...newSettings }
      ElMessage.success('模型设置保存成功')
      return true
    } catch (e: any) {
      ElMessage.error(e.response?.data?.detail || '保存失败')
      return false
    } finally {
      loading.value = false
    }
  }

  const testConnection = async (testConfig: LLMSettings) => {
    try {
      testing.value = true
      const res = await api.testSettings(testConfig)
      ElMessage.success(res.message || 'API 连接测试通过！')
      return true
    } catch (e: any) {
      ElMessage.error(e.response?.data?.detail || 'API 连接失败，请检查 Base URL、Key 或网络')
      return false
    } finally {
      testing.value = false
    }
  }

  return {
    settings,
    loading,
    testing,
    fetchSettings,
    saveSettings,
    testConnection,
  }
})
