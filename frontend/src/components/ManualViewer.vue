<script setup lang="ts">
import { ref, computed } from 'vue'
import { useCopyrightStore } from '../stores/copyright'
import { 
  BookOpen, 
  Download, 
  Copy, 
  Image as ImageIcon, 
  CheckCircle2, 
  Layers,
  Sparkles,
  ExternalLink
} from 'lucide-vue-next'
import { ElMessage } from 'element-plus'

const copyrightStore = useCopyrightStore()
const activeTab = ref<'preview' | 'gallery'>('preview')
const selectedMockup = ref<string | null>(null)

const mockupTitles: Record<string, string> = {
  login: '图 3-1 系统统一身份认证与安全登录界面',
  dashboard: '图 1-1 系统总体运行监控与大屏看板',
  module_1: '图 4-1 核心业务数据列表与操作工作台',
  module_2: '图 5-1 二级业务流转与处理列表',
  module_3: '图 6-1 数据详情与链路追溯看板',
  module_4: '图 7-1 综合统计报表与多维分析',
  config_modal: '图 4-2 核心业务参数与告警阈值配置弹窗',
}

const handleCopy = async () => {
  if (!copyrightStore.manualMarkdown) return
  try {
    await navigator.clipboard.writeText(copyrightStore.manualMarkdown)
    ElMessage.success('操作手册 Markdown 已复制')
  } catch (e) {
    ElMessage.error('复制失败')
  }
}

// Convert Markdown to clean rich HTML with inline image rendering
const renderedHtml = computed(() => {
  const md = copyrightStore.manualMarkdown
  if (!md) return ''

  const lines = md.split('\n')
  const htmlParts: string[] = []
  let inTable = false
  let tableRows: string[][] = []

  let currentModImgIdx = 1
  const inserted = {
    login: false,
    dashboard: false,
    config: false,
  }

  const flushTable = () => {
    if (!tableRows.length) return
    let tHtml = '<div class="my-4 overflow-x-auto"><table class="min-w-full text-xs border border-slate-200 rounded-lg overflow-hidden">'
    tableRows.forEach((row, rIdx) => {
      const isHeader = rIdx === 0
      tHtml += `<tr class="${isHeader ? 'bg-slate-100 font-bold text-slate-800' : 'border-t border-slate-200 hover:bg-slate-50'}">`
      row.forEach((cell) => {
        tHtml += `<${isHeader ? 'th' : 'td'} class="px-3 py-2 text-left border-r border-slate-200 last:border-r-0">${parseInline(cell)}</${isHeader ? 'th' : 'td'}>`
      })
      tHtml += '</tr>'
    })
    tHtml += '</table></div>'
    htmlParts.push(tHtml)
    tableRows = []
    inTable = false
  }

  const parseInline = (text: string) => {
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold text-slate-900">$1</strong>')
      .replace(/`([^`]+)`/g, '<code class="bg-slate-100 text-sky-700 px-1 py-0.5 rounded font-mono text-[11px]">$1</code>')
  }

  const renderImageBlock = (imgSrc: string, caption: string) => {
    return `
      <div class="my-5 p-2 bg-slate-50 border border-slate-200 rounded-xl shadow-sm">
        <img src="${imgSrc}" alt="${caption}" class="w-full rounded-lg border border-slate-200/80 shadow-sm" />
        <div class="text-center text-[11px] font-semibold text-slate-500 mt-2">${caption}</div>
      </div>
    `
  }

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim()

    if (!line) {
      if (inTable) flushTable()
      continue
    }

    // Markdown Table
    if (line.startsWith('|') && line.endsWith('|')) {
      inTable = true
      if (/^\|(\s*:?-+:?\s*\|)+$/.test(line)) {
        continue
      }
      const cells = line.split('|').slice(1, -1).map(c => c.trim())
      tableRows.push(cells)
      continue
    } else if (inTable) {
      flushTable()
    }

    // Headings
    if (line.startsWith('# ') && !line.startsWith('## ')) {
      htmlParts.push(`<h1 class="text-2xl font-bold text-slate-900 mt-6 mb-3 pb-2 border-b border-slate-200">${parseInline(line.slice(2))}</h1>`)
    } else if (line.startsWith('## ')) {
      const hText = line.slice(3).trim()
      htmlParts.push(`<h2 class="text-lg font-bold text-sky-900 mt-6 mb-2">${parseInline(hText)}</h2>`)

      if ((hText.includes('系统概述') || hText.includes('总体架构')) && !inserted.dashboard && copyrightStore.mockupsB64['dashboard']) {
        htmlParts.push(renderImageBlock(copyrightStore.mockupsB64['dashboard'], '图 1-1 系统总体运行监控与大屏看板示意图'))
        inserted.dashboard = true
      } else if ((hText.includes('系统登录') || hText.includes('身份认证')) && !inserted.login && copyrightStore.mockupsB64['login']) {
        htmlParts.push(renderImageBlock(copyrightStore.mockupsB64['login'], '图 3-1 系统统一身份认证与安全登录界面示意图'))
        inserted.login = true
      }
    } else if (line.startsWith('### ')) {
      const h3Text = line.slice(4).trim()
      htmlParts.push(`<h3 class="text-sm font-semibold text-slate-800 mt-4 mb-1.5">${parseInline(h3Text)}</h3>`)

      if ((h3Text.includes('操作界面') || h3Text.includes('界面布局') || h3Text.includes('数据列表')) && currentModImgIdx <= 4) {
        const mKey = `module_${currentModImgIdx}`
        if (copyrightStore.mockupsB64[mKey]) {
          htmlParts.push(renderImageBlock(copyrightStore.mockupsB64[mKey], mockupTitles[mKey] || `图 ${currentModImgIdx+3}-1 业务数据列表与操作工作台`))
          currentModImgIdx++
        } else if (!inserted.config && copyrightStore.mockupsB64['config_modal']) {
          htmlParts.push(renderImageBlock(copyrightStore.mockupsB64['config_modal'], '图 4-2 核心业务参数与告警阈值配置弹窗示意图'))
          inserted.config = true
        }
      }
    } else if (line.startsWith('- ') || line.startsWith('* ')) {
      htmlParts.push(`<li class="ml-5 list-disc text-xs text-slate-700 my-0.5 leading-relaxed">${parseInline(line.slice(2))}</li>`)
    } else if (/^\d+\.\s+/.test(line)) {
      const match = line.match(/^(\d+\.)\s+(.*)/)
      if (match) {
        htmlParts.push(`<div class="flex items-start space-x-2 text-xs text-slate-700 my-1 leading-relaxed"><span class="font-bold text-sky-600">${match[1]}</span><span>${parseInline(match[2])}</span></div>`)
      }
    } else if (line.startsWith('```mermaid')) {
      if (!inserted.dashboard && copyrightStore.mockupsB64['dashboard']) {
        htmlParts.push(renderImageBlock(copyrightStore.mockupsB64['dashboard'], '图 1-1 系统总体架构拓扑图'))
        inserted.dashboard = true
      }
    } else if (line.startsWith('```')) {
      // ignore
    } else {
      htmlParts.push(`<p class="text-xs text-slate-700 my-2 leading-relaxed">${parseInline(line)}</p>`)
    }
  }

  if (inTable) flushTable()
  return htmlParts.join('')
})
</script>

<template>
  <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col h-[760px]">
    <!-- Top Bar -->
    <div class="p-4 border-b border-slate-200 bg-slate-50/50 flex flex-wrap items-center justify-between gap-3">
      <div class="flex items-center space-x-3">
        <div class="flex items-center space-x-2">
          <BookOpen class="w-5 h-5 text-indigo-600" />
          <span class="text-sm font-semibold text-slate-800">用户操作手册 / 设计说明书</span>
        </div>

        <div class="flex items-center space-x-2 text-xs">
          <span class="px-2.5 py-1 rounded-md bg-slate-100 border border-slate-200 text-slate-700 font-mono">
            字数: <strong class="text-indigo-600 font-bold">{{ copyrightStore.manualWordCount }}</strong> 字
          </span>
          <span class="px-2.5 py-1 rounded-md bg-sky-50 border border-sky-200 text-sky-700 flex items-center space-x-1 font-mono">
            <ImageIcon class="w-3.5 h-3.5 text-sky-600" />
            <span>UI配图: <strong>{{ copyrightStore.mockupCount }}</strong> 张</span>
          </span>
          <span class="px-2.5 py-1 rounded-md bg-emerald-50 border border-emerald-200 text-emerald-700 flex items-center space-x-1">
            <CheckCircle2 class="w-3.5 h-3.5 text-emerald-600" />
            <span>约 <strong>{{ copyrightStore.estimatedManualPages }}</strong> 页 (图文并茂)</span>
          </span>
        </div>
      </div>

      <!-- Right Action & Tabs -->
      <div class="flex items-center space-x-2">
        <div class="flex rounded-lg bg-slate-200 p-0.5 text-xs mr-2">
          <button
            @click="activeTab = 'preview'"
            :class="[
              'px-2.5 py-1 rounded-md font-medium transition-all',
              activeTab === 'preview' ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-600 hover:text-slate-900'
            ]"
          >
            📖 图文排版预览
          </button>
          <button
            @click="activeTab = 'gallery'"
            :class="[
              'px-2.5 py-1 rounded-md font-medium transition-all flex items-center space-x-1',
              activeTab === 'gallery' ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-600 hover:text-slate-900'
            ]"
          >
            <ImageIcon class="w-3.5 h-3.5" />
            <span>系统截图画廊 ({{ copyrightStore.mockupCount }})</span>
          </button>
        </div>

        <button
          @click="handleCopy"
          class="inline-flex items-center space-x-1 px-3 py-1.5 rounded-lg text-xs font-medium text-slate-700 bg-white hover:bg-slate-50 border border-slate-300 shadow-sm transition-all"
        >
          <Copy class="w-3.5 h-3.5 text-slate-500" />
          <span>复制全文</span>
        </button>

        <button
          @click="copyrightStore.downloadManualDocx"
          :disabled="copyrightStore.isExporting || !copyrightStore.manualMarkdown"
          class="inline-flex items-center space-x-1 px-3.5 py-1.5 rounded-lg text-xs font-medium text-white bg-indigo-600 hover:bg-indigo-700 shadow-sm transition-all disabled:opacity-50"
        >
          <Download class="w-3.5 h-3.5" />
          <span>导出说明书 (.docx 含截图)</span>
        </button>
      </div>
    </div>

    <!-- Main Content Area (Tab 1: Rich Document Preview) -->
    <div v-show="activeTab === 'preview'" class="flex-1 overflow-auto p-6 bg-slate-50/50">
      <div v-if="!copyrightStore.manualMarkdown" class="h-full flex items-center justify-center text-slate-400 text-sm">
        暂无操作手册内容，请启动生成流水线
      </div>
      <div v-else class="max-w-4xl mx-auto bg-white p-8 sm:p-12 rounded-xl border border-slate-200 shadow-sm">
        <div v-html="renderedHtml"></div>
      </div>
    </div>

    <!-- Main Content Area (Tab 2: Screenshot Gallery) -->
    <div v-show="activeTab === 'gallery'" class="flex-1 overflow-auto p-6 bg-slate-100/60">
      <div v-if="copyrightStore.mockupCount === 0" class="h-full flex items-center justify-center text-slate-400 text-sm">
        暂无系统截图，启动流水线后将自动生成
      </div>
      <div v-else class="max-w-6xl mx-auto space-y-6">
        <div class="bg-white p-4 rounded-xl border border-slate-200 text-xs text-slate-600 flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <Sparkles class="w-4 h-4 text-sky-600" />
            <span>系统已根据您的软件功能自动渲染出 <strong>{{ copyrightStore.mockupCount }}</strong> 张高清系统界面图，导出 Word 或 Zip 时将自动包含。</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div
            v-for="(imgSrc, key) in copyrightStore.mockupsB64"
            :key="key"
            class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col group hover:shadow-md transition-all"
          >
            <div class="relative overflow-hidden bg-slate-950 aspect-[16/10]">
              <img :src="imgSrc" :alt="mockupTitles[key as string] || key" class="w-full h-full object-cover group-hover:scale-105 transition-all duration-300" />
            </div>
            <div class="p-3.5 bg-white border-t border-slate-100 flex items-center justify-between">
              <div>
                <div class="text-xs font-bold text-slate-800">{{ mockupTitles[key as string] || key }}</div>
                <div class="text-[10px] text-slate-400">1400 × 800 HD 渲染</div>
              </div>
              <a
                :href="imgSrc"
                :download="`${mockupTitles[key as string] || key}.png`"
                class="px-2.5 py-1 rounded bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] font-medium transition-all"
              >
                下载原图
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
