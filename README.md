# AutoCopyright-AI | 软件著作权资料一键生成系统

> **严格遵循中国版权保护中心（CPCC）软著审核规范的 AI 全套申报资料合成系统**
>
> 零现有代码也能一键生成：**3500+行工业级业务源代码**、**严格 60 页（每页50行+标准页眉页脚）Word 文档**、**25+页图文并茂用户操作手册**、**合规申请表填报信息**。

---

## 🌟 核心特性

1. **分层代码合成流水线 (Synthetic Code Pipeline)**
   - 解决单次大模型调用截断和偷懒问题，采用“配置层 $\rightarrow$ 实体模型层 $\rightarrow$ 业务服务与算法层 $\rightarrow$ 控制器路由层 $\rightarrow$ 工具层”分步高保真合成。
   - 支持 Java (SpringBoot), Python (FastAPI/Django), Vue 3/TS, Go, C#, C++ 等主流技术栈。
   - 自动清除开源协议头与多余空行，确保语法连贯、命名与业务 100% 契合。

2. **版权局级 60 页 Word 排版引擎 (CPCC-Compliant Docx Engine)**
   - 算法精准控制**每页严格 50 行**，单倍行距，等宽代码字体（Consolas/Courier New）。
   - 自动生成符合 CPCC 规范的页眉（《软件全称》版本号 源程序代码文档）与页码（第 1 页 至 第 60 页）。
   - 自动切取前 30 页（第 1~1500 行）与后 30 页（后 1500 行，以完整模块闭合结尾）。

3. **长文用户操作手册生成**
   - 自动生成涵盖系统概述、运行环境、安装部署、核心模块操作指引、维护与 FAQ 的完整体系。
   - 内置流程图与界面占位规范，一键导出带样式的 `.docx` 格式文档。

4. **申请表合规信息快速填报卡**
   - 软件全称、简称、版本号、分类号规范化。
   - 精准控制在 **250~300 字**内的《主要功能简介》与《技术特点》（一键复制直填 CPCC 系统）。

5. **多模型生态支持**
   - 支持 **DeepSeek-V3 / DeepSeek-Coder**、**OpenAI (GPT-4o)**、**阿里通义千问 (Qwen)**、**本地 Ollama** 以及任何兼容 OpenAI 协议的大模型。

---

## 🚀 快速启动指南

### 方式一：双击一键启动 (Windows)
直接双击根目录下的 `start.bat` 即可同时启动后端和前端服务。

### 方式二：手动分步启动

#### 1. 启动后端 (Python FastAPI)
```bash
cd backend
pip install -r requirements.txt
python run.py
```
- 后端服务地址：`http://localhost:8000`
- API Swagger 文档：`http://localhost:8000/docs`

#### 2. 启动前端 (Vue 3 + Vite)
```bash
cd frontend
npm install
npm run dev
```
- 前端访问地址：`http://localhost:5173`

---

## 📁 项目工程架构

```
sw-copyright/
├── backend/                  # Python FastAPI 后端
│   ├── app/
│   │   ├── main.py           # FastAPI 入口与 CORS 中间件
│   │   ├── config.py         # 模型配置与持久化
│   │   ├── core/             # 核心引擎
│   │   │   ├── llm.py        # 统一大模型调用服务
│   │   │   ├── docx_engine.py# 严格 60 页 Word (50行/页) 与手册排版引擎
│   │   │   ├── code_engine.py# 分层代码合成与清洗流水线
│   │   │   └── prompts.py    # 软著专用 Prompt 工程库
│   │   └── api/              # 业务路由网关
│   │       ├── settings.py   # 模型 API Key 配置与测试
│   │       ├── blueprint.py  # 蓝图规划
│   │       ├── code.py       # 分层代码生成
│   │       ├── manual.py     # 操作手册生成
│   │       ├── form_info.py  # 申请表信息生成
│   │       └── export.py     # 60页Word/手册/ZIP 一键导出
│   ├── requirements.txt      # 后端依赖
│   └── run.py                # 快速启动入口
│
├── frontend/                 # Vue 3 + Vite 前端
│   ├── src/
│   │   ├── components/       # UI 组件
│   │   │   ├── Header.vue    # 顶部导航与状态栏
│   │   │   ├── SettingsModal.vue # 模型配置弹窗
│   │   │   ├── CodeViewer.vue# 代码与 60 页预览卡片
│   │   │   ├── ManualViewer.vue  # 用户手册 Markdown/Word 预览
│   │   │   └── FormSummary.vue   # 申请表信息填报卡
│   │   ├── views/
│   │   │   └── WorkflowView.vue  # 4步向导式生成主工作台
│   │   ├── stores/           # Pinia 状态管理
│   │   ├── api/client.ts     # Axios 接口层
│   │   └── main.ts           # Vue 入口
│   ├── package.json
│   └── vite.config.ts
│
├── start.bat                 # Windows 一键启动脚本
└── README.md
```
