import io
import zipfile
import json
import urllib.parse
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.core.docx_engine import generate_code_docx, generate_manual_docx
from app.core.ui_renderer import UIMockupRenderer

router = APIRouter(prefix="/api/export", tags=["Export"])

class ExportCodeDocxRequest(BaseModel):
    software_name: str
    version: str = "V1.0"
    code_text: Optional[str] = None
    code_lines: Optional[List[str]] = None
    lines_per_page: int = 50
    target_pages: int = 60

class ExportManualDocxRequest(BaseModel):
    software_name: str
    version: str = "V1.0"
    markdown_content: str
    modules: Optional[List[Dict[str, str]]] = None
    ui_mockup_data: Optional[Dict[str, Any]] = None

class ExportFullZipRequest(BaseModel):
    software_name: str
    version: str = "V1.0"
    code_text: str
    manual_markdown: str
    form_info: Optional[Dict[str, Any]] = None
    modules: Optional[List[Dict[str, str]]] = None
    ui_mockup_data: Optional[Dict[str, Any]] = None

def get_filename_header(filename: str) -> str:
    encoded = urllib.parse.quote(filename)
    return f'attachment; filename="{encoded}"; filename*=UTF-8\'\'{encoded}'

def add_zip_entry(zf: zipfile.ZipFile, filename: str, data: bytes):
    """Add a file to zip with explicit UTF-8 encoding flag for Windows Explorer compatibility."""
    zinfo = zipfile.ZipInfo(filename)
    zinfo.flag_bits |= 0x800
    zinfo.compress_type = zipfile.ZIP_DEFLATED
    zf.writestr(zinfo, data)

@router.post("/code-docx")
async def export_code_docx_endpoint(req: ExportCodeDocxRequest):
    try:
        lines = req.code_lines
        if not lines and req.code_text:
            lines = req.code_text.splitlines()
        if not lines:
            raise ValueError("代码内容不能为空")

        output_io = generate_code_docx(
            code_lines=lines,
            software_name=req.software_name,
            version=req.version,
            lines_per_page=req.lines_per_page,
            target_pages=req.target_pages
        )
        filename = f"{req.software_name}_{req.version}_60页源码文档.docx"
        headers = {"Content-Disposition": get_filename_header(filename)}
        return StreamingResponse(
            output_io,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers=headers
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出代码 Word 失败: {str(e)}")

@router.post("/manual-docx")
async def export_manual_docx_endpoint(req: ExportManualDocxRequest):
    try:
        # Generate UI mockups to embed in Word with dynamic AI data
        renderer = UIMockupRenderer(req.software_name, req.version)
        images = renderer.generate_all_mockups(req.modules or [], ui_mockup_data=req.ui_mockup_data)

        output_io = generate_manual_docx(
            markdown_content=req.markdown_content,
            software_name=req.software_name,
            version=req.version,
            images=images
        )
        filename = f"{req.software_name}_{req.version}_用户操作手册.docx"
        headers = {"Content-Disposition": get_filename_header(filename)}
        return StreamingResponse(
            output_io,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers=headers
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出说明书 Word 失败: {str(e)}")

@router.post("/full-zip")
async def export_full_zip_endpoint(req: ExportFullZipRequest):
    try:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            # 1. 60-page Code Docx
            code_lines = req.code_text.splitlines()
            code_docx_io = generate_code_docx(
                code_lines=code_lines,
                software_name=req.software_name,
                version=req.version
            )
            add_zip_entry(zf, f"01_标准60页源程序代码文档_{req.version}.docx", code_docx_io.getvalue())

            # 2. UI Mockup Images (AI dynamic data)
            renderer = UIMockupRenderer(req.software_name, req.version)
            images = renderer.generate_all_mockups(req.modules or [], ui_mockup_data=req.ui_mockup_data)

            # 3. User Manual Docx with embedded UI screenshots
            manual_docx_io = generate_manual_docx(
                markdown_content=req.manual_markdown,
                software_name=req.software_name,
                version=req.version,
                images=images
            )
            add_zip_entry(zf, f"02_用户操作手册与设计说明书(含截图)_{req.version}.docx", manual_docx_io.getvalue())

            # 4. Raw Source Code text file (UTF-8 encoded)
            add_zip_entry(zf, f"03_全量业务源代码合集_{req.version}.txt", req.code_text.encode('utf-8'))

            # 5. Form info text & json
            if req.form_info:
                form_json_str = json.dumps(req.form_info, ensure_ascii=False, indent=2)
                add_zip_entry(zf, "04_软著申请表填报信息.json", form_json_str.encode('utf-8'))

                form_txt_lines = [
                    "=" * 50,
                    f"《{req.software_name}》 软著申请表快速填报摘要",
                    "=" * 50,
                    f"软件全称: {req.form_info.get('software_full_name', req.software_name)}",
                    f"软件简称: {req.form_info.get('software_short_name', '')}",
                    f"版本号: {req.form_info.get('version', req.version)}",
                    f"分类号: {req.form_info.get('classification_number', '60000-0000')}",
                    f"开发完成日期: {req.form_info.get('development_completion_date', '')}",
                    f"发表状态: {req.form_info.get('first_published_status', '未发表')}",
                    f"开发方式: {req.form_info.get('development_mode', '独立开发')}",
                    f"编程语言: {req.form_info.get('programming_language', '')}",
                    f"代码总行数: {req.form_info.get('lines_of_code', len(code_lines))}",
                    "-" * 50,
                    "【硬件环境(开发)】:",
                    req.form_info.get('hardware_env_dev', ''),
                    "【硬件环境(运行)】:",
                    req.form_info.get('hardware_env_run', ''),
                    "【软件环境(开发)】:",
                    req.form_info.get('software_env_dev', ''),
                    "【软件环境(运行)】:",
                    req.form_info.get('software_env_run', ''),
                    "-" * 50,
                    "【主要功能简介(300字内)】:",
                    req.form_info.get('main_functions', ''),
                    "-" * 50,
                    "【技术特点(300字内)】:",
                    req.form_info.get('technical_features', ''),
                    "=" * 50,
                ]
                add_zip_entry(zf, "04_软著申请表填报信息.txt", "\n".join(form_txt_lines).encode('utf-8'))

            # 6. Save separate PNG screenshots into a dedicated folder
            img_name_map = {
                "login": "01_系统统一登录认证界面.png",
                "dashboard": "02_系统综合监控大屏与看板.png",
                "module_1": "03_核心业务数据管理与操作表.png",
                "module_2": "04_二级业务流转与处理列表.png",
                "module_3": "05_数据详情与链路追溯看板.png",
                "module_4": "06_综合统计报表与多维分析.png",
                "config_modal": "07_业务规则与告警阈值配置弹窗.png",
            }
            for k, img_bytes in images.items():
                fname = img_name_map.get(k, f"08_{k}.png")
                add_zip_entry(zf, f"05_系统高保真运行截图/{fname}", img_bytes)

        zip_buffer.seek(0)
        filename = f"{req.software_name}_{req.version}_全套软著申报材料(含截图).zip"
        headers = {"Content-Disposition": get_filename_header(filename)}
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers=headers
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成全套申报压缩包失败: {str(e)}")
