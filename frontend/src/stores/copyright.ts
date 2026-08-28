import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api, type Blueprint, type FormInfo, type LayerCodeResult } from '../api/client'
import { ElMessage, ElNotification } from 'element-plus'

export const useCopyrightStore = defineStore('copyright', () => {
  // Wizard & Form Inputs
  const currentStep = ref(0)
  const softwareName = ref('')
  const version = ref('V1.0')
  const language = ref('Java')
  const features = ref('')

  // Generation States
  const blueprint = ref<Blueprint | null>(null)
  const isGeneratingBlueprint = ref(false)

  const isGeneratingCode = ref(false)
  const layerResults = ref<Record<string, LayerCodeResult>>({})
  const currentGeneratingLayer = ref<string>('')
  const fullCode = ref<string>('')

  const isGeneratingManual = ref(false)
  const currentGeneratingChapter = ref<string>('')
  const manualMarkdown = ref<string>('')
  const manualChapters = ref<Record<string, { title: string; content: string }>>({})
  const mockupsB64 = ref<Record<string, string>>({})

  const isGeneratingFormInfo = ref(false)
  const formInfo = ref<FormInfo | null>(null)

  const isExporting = ref(false)

  // Computed
  const totalCodeLines = computed(() => {
    if (!fullCode.value) return 0
    return fullCode.value.split('\n').length
  })

  const estimatedCodePages = computed(() => {
    return Math.ceil(totalCodeLines.value / 50)
  })

  const manualWordCount = computed(() => {
    return manualMarkdown.value?.length || 0
  })

  const estimatedManualPages = computed(() => {
    // Each formatted page in docx is ~350-400 characters + pictures
    const imgBonus = Object.keys(mockupsB64.value).length * 1.5
    return Math.max(1, Math.round(manualWordCount.value / 360) + Math.round(imgBonus))
  })

  const mockupCount = computed(() => {
    return Object.keys(mockupsB64.value).length
  })

  // Actions
  const createBlueprint = async () => {
    if (!softwareName.value.trim()) {
      ElMessage.warning('请填写软件全称')
      return false
    }
    try {
      isGeneratingBlueprint.value = true
      const res = await api.generateBlueprint({
        software_name: softwareName.value,
        language: language.value,
        features: features.value,
      })
      if (res.success && res.blueprint) {
        blueprint.value = res.blueprint
        currentStep.value = 1 // Move to blueprint review
        ElMessage.success('系统架构蓝图规划完成！')
        return true
      }
    } catch (e: any) {
      ElMessage.error(e.response?.data?.detail || '蓝图生成失败，请确认 API Key 配置')
      return false
    } finally {
      isGeneratingBlueprint.value = false
    }
  }

  const runLayeredCodePipeline = async () => {
    if (!blueprint.value) return
    isGeneratingCode.value = true
    layerResults.value = {}
    fullCode.value = ''

    const layers = blueprint.value.layers || []
    const combinedLines: string[] = []

    try {
      for (let i = 0; i < layers.length; i++) {
        const layer = layers[i]
        currentGeneratingLayer.value = layer.display_name

        const res = await api.generateLayerCode({
          software_name: softwareName.value,
          language: language.value,
          layer_name: layer.name,
          layer_display_name: layer.display_name,
          layer_files: layer.files,
          layer_description: layer.description,
          system_summary: blueprint.value.architecture_summary,
        })

        if (res.success) {
          layerResults.value[layer.name] = {
            display_name: res.display_name,
            lines_count: res.lines_count,
            code: res.code,
          }
          const lines = res.code.split('\n')
          combinedLines.push(...lines)
          combinedLines.push('')
          combinedLines.push(`// ==============================================================================`)
          combinedLines.push(`// End of ${layer.display_name}`)
          combinedLines.push(`// ==============================================================================`)
          combinedLines.push('')
          fullCode.value = combinedLines.join('\n')
        }
      }

      ElNotification({
        title: '代码生成完成',
        message: `成功合成 ${totalCodeLines.value} 行业务源码，严格符合 60 页排版！`,
        type: 'success',
      })
    } catch (e: any) {
      ElMessage.error(e.response?.data?.detail || '分层代码生成中途中断')
    } finally {
      isGeneratingCode.value = false
      currentGeneratingLayer.value = ''
    }
  }

  const runUserManualGeneration = async () => {
    if (!blueprint.value) return
    try {
      isGeneratingManual.value = true
      currentGeneratingChapter.value = '正在分章节深度扩写长文并合成高保真 UI 截图...'
      const res = await api.generateFullManualPipeline({
        software_name: softwareName.value,
        language: language.value,
        blueprint: blueprint.value,
      })
      if (res.success) {
        manualMarkdown.value = res.full_markdown
        manualChapters.value = res.chapters
        mockupsB64.value = res.mockups_b64
        ElNotification({
          title: '说明书与UI截图生成完成',
          message: `长文操作手册 (${res.total_words}字) 与 ${Object.keys(res.mockups_b64).length} 张高保真截图已就绪！`,
          type: 'success',
        })
      }
    } catch (e: any) {
      ElMessage.error(e.response?.data?.detail || '用户手册长文流水线生成失败')
    } finally {
      isGeneratingManual.value = false
      currentGeneratingChapter.value = ''
    }
  }

  const runFormInfoGeneration = async () => {
    try {
      isGeneratingFormInfo.value = true
      const res = await api.generateFormInfo({
        software_name: softwareName.value,
        language: language.value,
        features: features.value,
      })
      if (res.success) {
        formInfo.value = res.form_info
      }
    } catch (e: any) {
      ElMessage.error(e.response?.data?.detail || '申请表信息提取失败')
    } finally {
      isGeneratingFormInfo.value = false
    }
  }

  const runFullWorkflow = async () => {
    currentStep.value = 2 // Move to generating workspace
    // 1. Run Form info in background
    runFormInfoGeneration()
    // 2. Run Code pipeline
    await runLayeredCodePipeline()
    // 3. Run Long-form Manual & Mockup pipeline
    await runUserManualGeneration()
    currentStep.value = 3 // Move to overview & export
  }

  // File Download Helpers
  const triggerBlobDownload = (blobData: any, filename: string) => {
    const url = window.URL.createObjectURL(new Blob([blobData]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
  }

  const downloadCodeDocx = async () => {
    if (!fullCode.value) {
      ElMessage.warning('请先生成业务代码')
      return
    }
    try {
      isExporting.value = true
      const res = await api.downloadCodeDocx({
        software_name: softwareName.value,
        version: version.value,
        code_text: fullCode.value,
      })
      triggerBlobDownload(res.data, `${softwareName.value}_${version.value}_60页源码文档.docx`)
      ElMessage.success('60页源码文档 (.docx) 导出成功！')
    } catch (e: any) {
      ElMessage.error('导出代码文档失败')
    } finally {
      isExporting.value = false
    }
  }

  const downloadManualDocx = async () => {
    if (!manualMarkdown.value) {
      ElMessage.warning('请先生成用户手册')
      return
    }
    try {
      isExporting.value = true
      const res = await api.downloadManualDocx({
        software_name: softwareName.value,
        version: version.value,
        markdown_content: manualMarkdown.value,
        modules: blueprint.value?.modules || [],
        ui_mockup_data: (blueprint.value as any)?.ui_mockup_data,
      })
      triggerBlobDownload(res.data, `${softwareName.value}_${version.value}_用户操作手册(含截图).docx`)
      ElMessage.success('用户操作手册 (含高清截图 .docx) 导出成功！')
    } catch (e: any) {
      ElMessage.error('导出手册失败')
    } finally {
      isExporting.value = false
    }
  }

  const downloadFullPackageZip = async () => {
    if (!fullCode.value || !manualMarkdown.value) {
      ElMessage.warning('请先完成代码和操作手册生成')
      return
    }
    try {
      isExporting.value = true
      const res = await api.downloadFullZip({
        software_name: softwareName.value,
        version: version.value,
        code_text: fullCode.value,
        manual_markdown: manualMarkdown.value,
        form_info: formInfo.value || undefined,
        modules: blueprint.value?.modules || [],
        ui_mockup_data: (blueprint.value as any)?.ui_mockup_data,
      })
      triggerBlobDownload(res.data, `${softwareName.value}_${version.value}_全套软著申报材料(含截图).zip`)
      ElMessage.success('全套申报材料压缩包 (.zip) 打包下载完成！')
    } catch (e: any) {
      ElMessage.error('打包下载失败')
    } finally {
      isExporting.value = false
    }
  }

  return {
    currentStep,
    softwareName,
    version,
    language,
    features,
    blueprint,
    isGeneratingBlueprint,
    isGeneratingCode,
    currentGeneratingLayer,
    layerResults,
    fullCode,
    totalCodeLines,
    estimatedCodePages,
    isGeneratingManual,
    currentGeneratingChapter,
    manualMarkdown,
    manualChapters,
    mockupsB64,
    manualWordCount,
    estimatedManualPages,
    mockupCount,
    isGeneratingFormInfo,
    formInfo,
    isExporting,
    createBlueprint,
    runLayeredCodePipeline,
    runUserManualGeneration,
    runFormInfoGeneration,
    runFullWorkflow,
    downloadCodeDocx,
    downloadManualDocx,
    downloadFullPackageZip,
  }
})
