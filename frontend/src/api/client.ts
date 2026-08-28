import axios from 'axios'

const apiClient = axios.create({
  baseURL: '/api',
  timeout: 400000, // 6.5 minutes timeout for multi-stage chapter generation
})

export interface LLMSettings {
  provider: string
  api_key: string
  base_url: string
  model: string
  temperature: number
  max_tokens: number
}

export interface LayerItem {
  name: string
  display_name: string
  files: string[]
  description: string
}

export interface ModuleItem {
  code: string
  name: string
  description: string
}

export interface Blueprint {
  system_name: string
  version: string
  language: string
  architecture_summary: string
  layers: LayerItem[]
  modules: ModuleItem[]
}

export interface LayerCodeResult {
  display_name: string
  lines_count: number
  code: string
}

export interface FullCodeResult {
  total_lines: number
  layers: Record<string, LayerCodeResult>
  full_code: string
  lines_list: string[]
}

export interface FormInfo {
  software_full_name: string
  software_short_name: string
  version: string
  classification_number: string
  development_completion_date: string
  first_published_status: string
  development_mode: string
  programming_language: string
  lines_of_code: number
  hardware_env_dev: string
  hardware_env_run: string
  software_env_dev: string
  software_env_run: string
  main_functions: string
  technical_features: string
}

export const api = {
  // Settings
  getSettings: () => apiClient.get<LLMSettings>('/settings').then(res => res.data),
  updateSettings: (data: LLMSettings) => apiClient.post('/settings', data).then(res => res.data),
  testSettings: (data: LLMSettings) => apiClient.post('/settings/test', data).then(res => res.data),

  // Blueprint
  generateBlueprint: (data: { software_name: string; language: string; features?: string }) =>
    apiClient.post<{ success: boolean; blueprint: Blueprint }>('/blueprint/generate', data).then(res => res.data),

  // Code Generation
  generateLayerCode: (data: {
    software_name: string
    language: string
    layer_name: string
    layer_display_name: string
    layer_files: string[]
    layer_description: string
    system_summary: string
  }) => apiClient.post<{ success: boolean; layer_name: string; display_name: string; lines_count: number; code: string }>('/code/generate-layer', data).then(res => res.data),

  generateFullCode: (data: { software_name: string; language: string; blueprint: Blueprint }) =>
    apiClient.post<{ success: boolean; result: FullCodeResult }>('/code/generate-full', data).then(res => res.data),

  // Manual Chapter Pipeline
  generateFullManualPipeline: (data: { software_name: string; language: string; blueprint: Blueprint }) =>
    apiClient.post<{
      success: boolean
      total_words: number
      chapters: Record<string, { title: string; content: string }>
      full_markdown: string
      mockups_b64: Record<string, string>
    }>('/manual/generate-full-pipeline', data).then(res => res.data),

  // Form Info
  generateFormInfo: (data: { software_name: string; language: string; features?: string }) =>
    apiClient.post<{ success: boolean; form_info: FormInfo }>('/form-info/generate', data).then(res => res.data),

  // Exports (File downloads)
  downloadCodeDocx: (data: { software_name: string; version: string; code_text: string; lines_per_page?: number; target_pages?: number }) =>
    apiClient.post('/export/code-doc', data, { responseType: 'blob' }),

  downloadManualDocx: (data: { software_name: string; version: string; markdown_content: string; modules?: any[]; ui_mockup_data?: any }) =>
    apiClient.post('/export/manual-doc', data, { responseType: 'blob' }),

  downloadFullZip: (data: { software_name: string; version: string; code_text: string; manual_markdown: string; form_info?: FormInfo; modules?: any[]; ui_mockup_data?: any }) =>
    apiClient.post('/export/full-zip', data, { responseType: 'blob' }),
}
