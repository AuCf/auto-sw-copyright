"""
Code Engine Module: Handles blueprint generation, stratified code synthesis,
chapter-by-chapter long-form manual generation, and UI mockup generation.
"""

import re
import base64
import asyncio
from typing import Dict, Any, List, Optional
from app.core.llm import LLMService
from app.core.ui_renderer import UIMockupRenderer
from app.core.prompts import (
    BLUEPRINT_SYSTEM_PROMPT,
    CODE_LAYER_SYSTEM_PROMPT,
    FORM_INFO_SYSTEM_PROMPT,
    USER_MANUAL_SYSTEM_PROMPT
)

def sanitize_code_text(raw_text: str) -> List[str]:
    """Cleans up LLM raw code output."""
    lines = raw_text.splitlines()
    clean_lines = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```") or stripped == "```":
            continue
        if re.search(r"copyright\s*\(c\).*(oracle|apache|google|microsoft|meta)", line, re.IGNORECASE):
            continue
        clean_lines.append(line)
        
    condensed = []
    prev_empty = False
    for line in clean_lines:
        is_empty = not line.strip()
        if is_empty:
            if not prev_empty:
                condensed.append("")
                prev_empty = True
        else:
            condensed.append(line)
            prev_empty = False
            
    return condensed


class CodeSynthesisEngine:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    async def generate_blueprint(
        self,
        software_name: str,
        language: str = "Java",
        features: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate system architecture blueprint and module plan."""
        user_prompt = f"""请为以下软件设计系统架构蓝图：
- 软件全称：{software_name}
- 编程语言/技术栈：{language}
- 核心功能特性：{features or '标准企业级完整业务模块，包含数据采集、处理分析、业务调度、权限控制、报表统计等'}
"""
        messages = [
            {"role": "system", "content": BLUEPRINT_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        
        raw_output = await self.llm.chat(messages, temperature=0.7)
        return self.llm.extract_json(raw_output)

    async def generate_layer_code(
        self,
        software_name: str,
        language: str,
        layer_name: str,
        layer_display_name: str,
        layer_files: List[str],
        layer_description: str,
        system_summary: str
    ) -> str:
        """Generate real business code for a specific architectural layer."""
        user_prompt = f"""系统背景：{software_name} ({language})
系统概述：{system_summary}

当前生成任务：【{layer_display_name} ({layer_name})】
本层职责：{layer_description}
包含核心文件列表：{', '.join(layer_files)}

请为本层编写全部完整的、工业级业务源码：
1. 语言必须为：{language}；
2. 必须包含完整的方法体实现、真实的数据流转、参数合法性检验、异常抛出与逻辑运算；
3. 务必写出丰满的代码，避免任何省略占位符；
4. 每个文件前标注 // File: [FileName] 或 # File: [FileName]。
"""
        messages = [
            {"role": "system", "content": CODE_LAYER_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        
        return await self.llm.chat(messages, temperature=0.6, max_tokens=4000)

    async def generate_full_pipeline(
        self,
        software_name: str,
        language: str,
        blueprint: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute full code synthesis pipeline layer-by-layer."""
        layers = blueprint.get("layers", [])
        system_summary = blueprint.get("architecture_summary", "")
        
        results = {}
        all_code_lines = []
        
        for layer in layers:
            name = layer.get("name")
            display_name = layer.get("display_name")
            files = layer.get("files", [])
            desc = layer.get("description", "")
            
            raw_code = await self.generate_layer_code(
                software_name=software_name,
                language=language,
                layer_name=name,
                layer_display_name=display_name,
                layer_files=files,
                layer_description=desc,
                system_summary=system_summary
            )
            
            clean_lines = sanitize_code_text(raw_code)
            results[name] = {
                "display_name": display_name,
                "lines_count": len(clean_lines),
                "code": "\n".join(clean_lines)
            }
            all_code_lines.extend(clean_lines)
            all_code_lines.append("")
            all_code_lines.append(f"// {'=' * 70}")
            all_code_lines.append(f"// End of {display_name}")
            all_code_lines.append(f"// {'=' * 70}")
            all_code_lines.append("")
            
        full_code = "\n".join(all_code_lines)
        return {
            "total_lines": len(all_code_lines),
            "layers": results,
            "full_code": full_code,
            "lines_list": all_code_lines
        }

    async def generate_form_info(
        self,
        software_name: str,
        language: str,
        features: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate standardized CPCC application form dataset."""
        user_prompt = f"""软件全称：{software_name}
编程语言：{language}
主要功能概述：{features or '包含系统管理、数据处理、业务计算、报表分析等完整功能'}
"""
        messages = [
            {"role": "system", "content": FORM_INFO_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        raw_output = await self.llm.chat(messages, temperature=0.7)
        return self.llm.extract_json(raw_output)

    async def generate_manual_chapter(
        self,
        software_name: str,
        version: str,
        chapter_title: str,
        chapter_requirements: str
    ) -> str:
        """Generate a single in-depth User Manual chapter with zero fluff."""
        user_prompt = f"""软件全称：{software_name} ({version})
当前生成章节：【{chapter_title}】
章节具体内容与结构要求：
{chapter_requirements}

【撰写规范】：
1. 语言严密正式，输出规范 Markdown 格式，绝不使用空洞套话；
2. 必须给出具体翔实的操作指引：具体的界面按钮、输入字段参数说明表格、操作流程 1..6、常见异常与处理策略；
3. 本章输出不少于 1200 字。
"""
        messages = [
            {"role": "system", "content": "你是一名精通国家软著申报的资深软件架构师和系统技术文档专家。"},
            {"role": "user", "content": user_prompt}
        ]
        return await self.llm.chat(messages, temperature=0.6, max_tokens=3500)

    async def generate_full_manual_pipeline(
        self,
        software_name: str,
        language: str,
        blueprint: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Chapter-by-chapter long-form User Manual synthesis pipeline.
        Produces 8,000 ~ 12,000+ words of concrete, multi-page operational instructions.
        """
        version = blueprint.get("version", "V1.0")
        modules = blueprint.get("modules", [])
        arch_summary = blueprint.get("architecture_summary", "")

        chapter_tasks = [
            {
                "id": "ch1",
                "title": "第1章 系统概述与总体架构",
                "req": f"""1.1 系统开发背景与建设目标
1.2 系统适用对象与典型业务应用场景
1.3 系统总体技术架构与分层设计原则 (架构概括: {arch_summary})
1.4 核心数据流转拓扑与业务处理闭环"""
            },
            {
                "id": "ch2",
                "title": "第2章 运行环境与安装部署配置",
                "req": f"""2.1 推荐硬件与网络带宽环境要求 (以标准 Markdown 表格呈现)
2.2 支撑软件、运行依赖库与数据库环境要求 (以标准 Markdown 表格呈现)
2.3 服务端与客户端安装部署操作步骤指南
2.4 系统初始化参数配置与服务连通性验证"""
            },
            {
                "id": "ch3",
                "title": "第3章 系统登录认证与权限管理",
                "req": """3.1 统一身份认证与安全登录流程 (包含登录界面说明、账号密码校验、验证码机制、密码加密与重置)
3.2 基于 RBAC 的多角色权限分配与数据权限隔离配置
3.3 系统安全审计日志与在线会话管理"""
            }
        ]

        # Add chapters for each core business module
        for i, mod in enumerate(modules[:5]):
            m_code = mod.get("code", f"M0{i+1}")
            m_name = mod.get("name", f"核心业务模块{i+1}")
            m_desc = mod.get("description", "")
            chapter_tasks.append({
                "id": f"ch_mod_{i+1}",
                "title": f"第{i+4}章 {m_name} 详细操作指南",
                "req": f"""模块业务定位：{m_desc}
必须包含以下完整小节：
1. **模块功能概述与业务价值**：解决的核心业务痛点
2. **操作界面布局与交互说明**：包含界面各功能区分布、顶部筛选栏、操作按钮清单（如【新增】、【批量导出】、【状态变更】）
3. **输入表单参数说明表**：以标准 Markdown 表格列出 5-8 个关键字段名称、数据类型、取值范围、必填项与校验规则
4. **标准业务操作流程**：分步骤详解（步骤 1、步骤 2、步骤 3、步骤 4、步骤 5、步骤 6）
5. **业务规则与计算逻辑**：状态流转条件、公式算法或过滤机制
6. **常见操作异常与系统反馈提示**"""
            })

        # Final maintenance chapter
        final_ch_num = len(chapter_tasks) + 1
        chapter_tasks.append({
            "id": "ch_final",
            "title": f"第{final_ch_num}章 系统日常维护与常见问题排查 (FAQ)",
            "req": """1. 数据备份策略与灾难恢复预案 (全量备份与增量日志归档)
2. 系统性能监控与日志清理维护规范
3. 典型故障与异常排查诊断手册 (以问题描述、可能原因、处理方案三栏表格呈现)"""
        })

        chapters_output = {}
        full_markdown_parts = [f"# 《{software_name}》 用户操作手册与系统设计说明书 ({version})\n"]

        for task in chapter_tasks:
            ch_content = await self.generate_manual_chapter(
                software_name=software_name,
                version=version,
                chapter_title=task["title"],
                chapter_requirements=task["req"]
            )
            clean_ch = ch_content.strip()
            chapters_output[task["id"]] = {
                "title": task["title"],
                "content": clean_ch
            }
            full_markdown_parts.append(f"## {task['title']}\n")
            full_markdown_parts.append(clean_ch)
            full_markdown_parts.append("\n\n")

        full_manual_md = "\n".join(full_markdown_parts)

        # Also generate matching high-fidelity AI-driven UI Mockups
        ui_renderer = UIMockupRenderer(software_name, version)
        ui_mockup_data = blueprint.get("ui_mockup_data")
        mockups_bytes = ui_renderer.generate_all_mockups(modules, ui_mockup_data=ui_mockup_data)

        # Convert to base64 for frontend display
        mockups_b64 = {}
        for k, v in mockups_bytes.items():
            mockups_b64[k] = f"data:image/png;base64,{base64.b64encode(v).decode('utf-8')}"

        return {
            "total_words": len(full_manual_md),
            "chapters": chapters_output,
            "full_markdown": full_manual_md,
            "mockups_bytes": mockups_bytes,
            "mockups_b64": mockups_b64
        }
