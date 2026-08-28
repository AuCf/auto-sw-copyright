<script setup lang="ts">
import { useCopyrightStore } from '../stores/copyright'
import { FileSpreadsheet, Copy, Check, Info } from 'lucide-vue-next'
import { ElMessage } from 'element-plus'

const copyrightStore = useCopyrightStore()

const copyField = async (label: string, text: string) => {
  if (!text) return
  try {
    await navigator.clipboard.writeText(text)
    ElMessage.success(`已复制 ${label}`)
  } catch (e) {
    ElMessage.error('复制失败')
  }
}
</script>

<template>
  <div class="bg-white rounded-xl border border-slate-200 shadow-sm p-6 space-y-6">
    <div class="flex items-center justify-between border-b border-slate-100 pb-4">
      <div class="flex items-center space-x-2">
        <FileSpreadsheet class="w-5 h-5 text-emerald-600" />
        <h3 class="text-base font-semibold text-slate-800">中国版权保护中心（CPCC）申报表快速填报卡</h3>
      </div>
      <span class="text-xs text-slate-500 bg-slate-100 px-2.5 py-1 rounded-md">
        已自动匹配版权局最新审核规范
      </span>
    </div>

    <div v-if="!copyrightStore.formInfo" class="py-12 text-center text-slate-400 text-sm">
      申报表信息尚未生成
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
      <!-- Software Full Name -->
      <div class="p-3 bg-slate-50 rounded-lg border border-slate-200/80">
        <div class="flex items-center justify-between mb-1">
          <span class="font-medium text-slate-500">软件全称</span>
          <button @click="copyField('软件全称', copyrightStore.formInfo.software_full_name)" class="text-sky-600 hover:text-sky-700 flex items-center space-x-0.5">
            <Copy class="w-3 h-3" />
            <span>复制</span>
          </button>
        </div>
        <div class="font-semibold text-slate-800 text-sm">{{ copyrightStore.formInfo.software_full_name }}</div>
      </div>

      <!-- Software Short Name & Version -->
      <div class="p-3 bg-slate-50 rounded-lg border border-slate-200/80">
        <div class="flex items-center justify-between mb-1">
          <span class="font-medium text-slate-500">软件简称 / 版本号</span>
          <button @click="copyField('软件简称', copyrightStore.formInfo.software_short_name)" class="text-sky-600 hover:text-sky-700 flex items-center space-x-0.5">
            <Copy class="w-3 h-3" />
            <span>复制简称</span>
          </button>
        </div>
        <div class="font-semibold text-slate-800 text-sm">
          {{ copyrightStore.formInfo.software_short_name || '无' }} / {{ copyrightStore.formInfo.version }}
        </div>
      </div>

      <!-- Dev Env: Hardware & Software -->
      <div class="p-3 bg-slate-50 rounded-lg border border-slate-200/80 space-y-2">
        <div>
          <div class="flex items-center justify-between mb-1">
            <span class="font-medium text-slate-500">开发硬件环境</span>
            <button @click="copyField('开发硬件环境', copyrightStore.formInfo.hardware_env_dev)" class="text-sky-600 hover:text-sky-700">复制</button>
          </div>
          <div class="text-slate-700 leading-normal">{{ copyrightStore.formInfo.hardware_env_dev }}</div>
        </div>
        <div class="pt-2 border-t border-slate-200">
          <div class="flex items-center justify-between mb-1">
            <span class="font-medium text-slate-500">开发软件环境 / 工具</span>
            <button @click="copyField('开发软件环境', copyrightStore.formInfo.software_env_dev)" class="text-sky-600 hover:text-sky-700">复制</button>
          </div>
          <div class="text-slate-700 leading-normal">{{ copyrightStore.formInfo.software_env_dev }}</div>
        </div>
      </div>

      <!-- Run Env: Hardware & Software -->
      <div class="p-3 bg-slate-50 rounded-lg border border-slate-200/80 space-y-2">
        <div>
          <div class="flex items-center justify-between mb-1">
            <span class="font-medium text-slate-500">运行硬件环境</span>
            <button @click="copyField('运行硬件环境', copyrightStore.formInfo.hardware_env_run)" class="text-sky-600 hover:text-sky-700">复制</button>
          </div>
          <div class="text-slate-700 leading-normal">{{ copyrightStore.formInfo.hardware_env_run }}</div>
        </div>
        <div class="pt-2 border-t border-slate-200">
          <div class="flex items-center justify-between mb-1">
            <span class="font-medium text-slate-500">运行软件环境 / 支撑中间件</span>
            <button @click="copyField('运行软件环境', copyrightStore.formInfo.software_env_run)" class="text-sky-600 hover:text-sky-700">复制</button>
          </div>
          <div class="text-slate-700 leading-normal">{{ copyrightStore.formInfo.software_env_run }}</div>
        </div>
      </div>

      <!-- Main Functions (300 words) -->
      <div class="p-3 bg-slate-50 rounded-lg border border-slate-200/80 md:col-span-2">
        <div class="flex items-center justify-between mb-1">
          <div class="flex items-center space-x-2">
            <span class="font-medium text-slate-600">主要功能简介</span>
            <span class="text-[10px] px-1.5 py-0.5 rounded bg-sky-100 text-sky-700">字数: {{ copyrightStore.formInfo.main_functions?.length }} / 300字限制</span>
          </div>
          <button @click="copyField('主要功能', copyrightStore.formInfo.main_functions)" class="text-sky-600 hover:text-sky-700 flex items-center space-x-0.5">
            <Copy class="w-3 h-3" />
            <span>复制</span>
          </button>
        </div>
        <div class="text-slate-800 leading-relaxed font-sans text-xs bg-white p-3 rounded border border-slate-200">
          {{ copyrightStore.formInfo.main_functions }}
        </div>
      </div>

      <!-- Technical Features (300 words) -->
      <div class="p-3 bg-slate-50 rounded-lg border border-slate-200/80 md:col-span-2">
        <div class="flex items-center justify-between mb-1">
          <div class="flex items-center space-x-2">
            <span class="font-medium text-slate-600">技术特点</span>
            <span class="text-[10px] px-1.5 py-0.5 rounded bg-indigo-100 text-indigo-700">字数: {{ copyrightStore.formInfo.technical_features?.length }} / 300字限制</span>
          </div>
          <button @click="copyField('技术特点', copyrightStore.formInfo.technical_features)" class="text-sky-600 hover:text-sky-700 flex items-center space-x-0.5">
            <Copy class="w-3 h-3" />
            <span>复制</span>
          </button>
        </div>
        <div class="text-slate-800 leading-relaxed font-sans text-xs bg-white p-3 rounded border border-slate-200">
          {{ copyrightStore.formInfo.technical_features }}
        </div>
      </div>
    </div>
  </div>
</template>
