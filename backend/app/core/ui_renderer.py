"""
Ultra-High-Fidelity Dynamic Synthetic UI Mockup Generator for Software Copyright Documentation.
Includes:
- Realistic Chrome / OS Application Window Shell with traffic lights, URL bar, and SSL lock
- 6 Domain Theme Palettes (Emerald, Amber, Indigo, Cyan, Rose, Ocean Blue)
- Sparklines, Radial Gauges, Team Avatars, and Metric Trend Curves
- 10 Enterprise Layout Paradigms:
  1. Login & Identity Security Screen
  2. Multi-Metric Executive Dashboard Cockpit
  3. Data Table & Batch Query Workstation (with inline Sparklines)
  4. 3-Column Kanban Board & Workflow Swimlane
  5. Multi-Chart Analytics & Bar/Line Data Studio
  6. Stepper Pipeline & Detail Audit Traceability
  7. Microservice Topology & Cluster Mesh Network
  8. Split-Pane Master-Detail Category Tree
  9. Dark Terminal & Real-Time Log Stream Console
  10. Gantt Chart & Milestone Timeline Scheduler
  11. Visual Rule Engine & Parameter Dialog
"""

import io
import re
import math
import zlib
import base64
from typing import Dict, List, Any, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

def get_font(size: int, bold: bool = False):
    font_candidates = [
        ("C:\\Windows\\Fonts\\msyhbd.ttc", 0) if bold else ("C:\\Windows\\Fonts\\msyh.ttc", 0),
        ("C:\\Windows\\Fonts\\msyh.ttc", 0),
        ("C:\\Windows\\Fonts\\simhei.ttf", 0),
        ("C:\\Windows\\Fonts\\simsun.ttc", 0),
    ]

    for path, idx in font_candidates:
        try:
            return ImageFont.truetype(path, size=size, index=idx)
        except Exception:
            continue
    return ImageFont.load_default()

def draw_rounded_rect(draw: ImageDraw.ImageDraw, xy, radius: int, fill=None, outline=None, width: int = 1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

class UIMockupRenderer:
    def __init__(self, software_name: str, version: str = "V1.0"):
        self.software_name = software_name or "企业级智能综合业务管理系统"
        self.version = version or "V1.0"
        self.width = 1440
        self.height = 860

        # Compute deterministic seed from software name
        self.seed = zlib.crc32(self.software_name.encode('utf-8'))

        # 6 Domain Color Themes
        palettes = [
            # 0: Deep Ocean Blue (Logistics, Transport, General)
            {"primary": (2, 132, 199), "light": (240, 249, 255), "dark": (3, 105, 161), "accent": (16, 185, 129), "name": "Ocean Blue"},
            # 1: Emerald / Forest Teal (Medical, Agri, Green, Ecology, Pets)
            {"primary": (5, 150, 105), "light": (236, 253, 245), "dark": (4, 120, 87), "accent": (14, 165, 233), "name": "Emerald"},
            # 2: Tech Indigo / Cyber Violet (AI, Big Data, Cloud, Blockchain)
            {"primary": (79, 70, 229), "light": (238, 242, 255), "dark": (67, 56, 202), "accent": (236, 72, 153), "name": "Indigo"},
            # 3: Industrial Amber / Slate (Manufacturing, Hardware, Energy, Laser)
            {"primary": (217, 119, 6), "light": (255, 251, 235), "dark": (180, 83, 9), "accent": (14, 116, 144), "name": "Industrial Amber"},
            # 4: Cyan & Ocean Slate (Security, Gov, Finance, Audit, Edu)
            {"primary": (8, 145, 178), "light": (236, 254, 255), "dark": (14, 116, 144), "accent": (99, 102, 241), "name": "Cyan Ocean"},
            # 5: Modern Rose / Crimson (E-commerce, Retail, Media, Livestream)
            {"primary": (225, 29, 72), "light": (255, 241, 242), "dark": (190, 18, 60), "accent": (245, 158, 11), "name": "Rose Crimson"},
        ]

        sw_lower = self.software_name.lower()
        if any(k in sw_lower for k in ["医", "药", "病", "农", "粮", "环", "生鲜", "绿", "水", "宠"]):
            palette_idx = 1
        elif any(k in sw_lower for k in ["ai", "大模型", "智能", "算法", "链", "图", "云", "知识"]):
            palette_idx = 2
        elif any(k in sw_lower for k in ["工", "制造", "激光", "机", "车", "硬件", "电", "控制", "设备"]):
            palette_idx = 3
        elif any(k in sw_lower for k in ["政", "法", "安", "防", "审", "税", "银", "融", "校", "教"]):
            palette_idx = 4
        elif any(k in sw_lower for k in ["商", "购", "市", "店", "销", "播", "淘", "客"]):
            palette_idx = 5
        else:
            palette_idx = self.seed % len(palettes)

        active_pal = palettes[palette_idx]
        self.primary_color = active_pal["primary"]
        self.primary_light = active_pal["light"]
        self.primary_dark = active_pal["dark"]
        self.accent_color = active_pal["accent"]

        # Universal Tokens
        self.dark_bg = (15, 23, 42)
        self.indigo_color = (79, 70, 229)
        self.emerald_color = (16, 185, 129)
        self.amber_color = (245, 158, 11)
        self.purple_color = (147, 51, 234)
        self.rose_color = (225, 29, 72)
        self.border_color = (226, 232, 240)
        self.text_main = (30, 41, 59)
        self.text_muted = (100, 116, 139)

    def _draw_window_shell(self, draw: ImageDraw.ImageDraw, page_title: str):
        """Draw realistic Chrome/Browser window frame."""
        # Window Titlebar (36px)
        draw.rectangle([(0, 0), (self.width, 36)], fill=(238, 242, 246), outline=(203, 213, 225))
        
        # 3 Traffic lights (macOS style)
        draw.ellipse([(14, 12), (26, 24)], fill=(255, 95, 87))   # Red
        draw.ellipse([(34, 12), (46, 24)], fill=(254, 188, 46))  # Yellow
        draw.ellipse([(54, 12), (66, 24)], fill=(40, 201, 64))   # Green

        # Active Browser Tab
        draw_rounded_rect(draw, [(80, 6), (320, 36)], radius=6, fill=(255, 255, 255), outline=(203, 213, 225))
        draw.text((95, 13), f"🌐 {self.software_name[:12]}...", fill=self.text_main, font=get_font(10, bold=True))
        draw.text((300, 13), "×", fill=self.text_muted, font=get_font(10))

        # Plus Tab
        draw.text((335, 13), "+", fill=self.text_muted, font=get_font(12))

        # Browser Navigation Omnibox (40px)
        draw.rectangle([(0, 36), (self.width, 76)], fill=(255, 255, 255), outline=self.border_color)
        draw.text((20, 48), "‹   ›   ↻", fill=self.text_muted, font=get_font(13, bold=True))

        # URL Box
        draw_rounded_rect(draw, [(100, 42), (self.width - 160, 70)], radius=6, fill=(241, 245, 249), outline=(226, 232, 240))
        url_text = f"🔒  https://app.cloud-enterprise.cn/v1/workspace/{page_title}"
        draw.text((115, 49), url_text, fill=(71, 85, 105), font=get_font(10))

        # Right Action Icons
        draw.text((self.width - 130, 48), "⭐  ⚙  👤", fill=self.text_muted, font=get_font(11))

    def _draw_common_navbar(self, draw: ImageDraw.ImageDraw, active_title: str):
        """Draw application top header (starts at y=76)."""
        self._draw_window_shell(draw, active_title)

        draw.rectangle([(0, 76), (self.width, 130)], fill=(255, 255, 255), outline=self.border_color)
        draw.rectangle([(0, 76), (220, 130)], fill=self.dark_bg)
        
        sw_short = self.software_name[:12] + "..." if len(self.software_name) > 12 else self.software_name
        draw.text((20, 95), sw_short, fill=(255, 255, 255), font=get_font(12, bold=True))

        draw.text((245, 96), f"业务中心 / {active_title}", fill=self.text_main, font=get_font(12, bold=True))

        # Status & Avatars
        draw_rounded_rect(draw, [(self.width - 380, 88), (self.width - 240, 118)], radius=6, fill=(240, 253, 244), outline=(187, 247, 208))
        draw.text((self.width - 370, 95), "● 节点通信正常 (在线)", fill=self.emerald_color, font=get_font(10, bold=True))

        # Avatar group
        draw.ellipse([(self.width - 210, 88), (self.width - 182, 116)], fill=self.primary_color)
        draw.text((self.width - 200, 95), "JD", fill=(255, 255, 255), font=get_font(9, bold=True))

        draw.ellipse([(self.width - 188, 88), (self.width - 160, 116)], fill=self.accent_color)
        draw.text((self.width - 178, 95), "TW", fill=(255, 255, 255), font=get_font(9, bold=True))

        draw.text((self.width - 145, 96), f"{self.version}", fill=self.text_muted, font=get_font(10, bold=True))
        draw.ellipse([(self.width - 60, 88), (self.width - 32, 116)], fill=self.dark_bg)
        draw.text((self.width - 50, 95), "管", fill=(255, 255, 255), font=get_font(10, bold=True))

    def _draw_sidebar(self, draw: ImageDraw.ImageDraw, active_index: int = 0, modules: Optional[List[Dict[str, str]]] = None):
        """Draw left navigation sidebar (starts at y=130)."""
        draw.rectangle([(0, 130), (220, self.height)], fill=(255, 255, 255), outline=self.border_color)
        mods = modules or []
        menu_items = ["📊 综合大屏看板"] + [f"📁 {m.get('name', '业务模块')[:8]}" for m in mods[:6]]

        for i, item in enumerate(menu_items):
            iy = 145 + i * 44
            is_active = (i == active_index)
            if is_active:
                draw_rounded_rect(draw, [(12, iy), (208, iy + 36)], radius=6, fill=self.primary_light)
                draw.text((24, iy + 10), item, fill=self.primary_color, font=get_font(11, bold=True))
            else:
                draw.text((24, iy + 10), item, fill=self.text_main, font=get_font(11))

    # =========================================================================
    # Template 1: Login & Identity Security Screen
    # =========================================================================
    def render_login_screen(self) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height), (241, 245, 249))
        draw = ImageDraw.Draw(img)

        self._draw_window_shell(draw, "login")

        # Dynamic Gradient background
        draw.rectangle([(0, 76), (self.width, 360)], fill=self.primary_dark)
        draw.rectangle([(0, 350), (self.width, 360)], fill=self.primary_color)

        card_w, card_h = 540, 490
        cx = (self.width - card_w) // 2
        cy = 200
        draw_rounded_rect(draw, [(cx, cy), (cx + card_w, cy + card_h)], radius=16, fill=(255, 255, 255), outline=(226, 232, 240), width=1)

        icon_cx, icon_cy = self.width // 2, cy + 45
        draw.ellipse([(icon_cx - 24, icon_cy - 24), (icon_cx + 24, icon_cy + 24)], fill=self.primary_color)
        draw.text((icon_cx - 10, icon_cy - 12), "✓", fill=(255, 255, 255), font=get_font(18, bold=True))

        f_title = get_font(17, bold=True)
        f_sub = get_font(11)
        f_label = get_font(11, bold=True)
        f_input = get_font(12)

        title_text = f"《{self.software_name}》"
        if len(title_text) > 24:
            title_text = title_text[:23] + "...》"
        draw.text((self.width // 2, cy + 85), title_text, fill=self.text_main, font=f_title, anchor="mt")
        draw.text((self.width // 2, cy + 115), f"系统统一身份认证与安全登录入口 ({self.version})", fill=self.text_muted, font=f_sub, anchor="mt")

        # Username
        draw.text((cx + 45, cy + 150), "账号 / 用户名", fill=self.text_main, font=f_label)
        draw_rounded_rect(draw, [(cx + 45, cy + 172), (cx + card_w - 45, cy + 212)], radius=8, fill=(248, 250, 252), outline=(203, 213, 225))
        draw.text((cx + 60, cy + 185), "admin_super", fill=(51, 65, 85), font=f_input)

        # Password
        draw.text((cx + 45, cy + 225), "登录密码", fill=self.text_main, font=f_label)
        draw_rounded_rect(draw, [(cx + 45, cy + 247), (cx + card_w - 45, cy + 287)], radius=8, fill=(248, 250, 252), outline=(203, 213, 225))
        draw.text((cx + 60, cy + 260), "••••••••••••••••", fill=(51, 65, 85), font=f_input)

        # Captcha
        draw.text((cx + 45, cy + 300), "动态安全验证码", fill=self.text_main, font=f_label)
        draw_rounded_rect(draw, [(cx + 45, cy + 322), (cx + 310, cy + 362)], radius=8, fill=(248, 250, 252), outline=(203, 213, 225))
        draw.text((cx + 60, cy + 335), "8 4 E K", fill=(51, 65, 85), font=f_input)
        draw_rounded_rect(draw, [(cx + 325, cy + 322), (cx + card_w - 45, cy + 362)], radius=8, fill=self.primary_light, outline=self.border_color)
        draw.text((cx + 370, cy + 335), "84EK", fill=self.primary_color, font=get_font(14, bold=True))

        # Login button
        draw_rounded_rect(draw, [(cx + 45, cy + 390), (cx + card_w - 45, cy + 435)], radius=8, fill=self.primary_color)
        draw.text((self.width // 2, cy + 405), "立即安全登录", fill=(255, 255, 255), font=get_font(13, bold=True), anchor="mt")

        draw.text((self.width // 2, self.height - 35), f"© 2026 {self.software_name} · 计算机软件著作权官方申报材料", fill=(148, 163, 184), font=f_sub, anchor="mt")
        return img

    # =========================================================================
    # Template 2: Executive Dashboard Cockpit
    # =========================================================================
    def render_dashboard_screen(self, modules: List[Dict[str, str]], ai_cards: Optional[List[Dict[str, str]]] = None) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height), (248, 250, 252))
        draw = ImageDraw.Draw(img)

        self._draw_common_navbar(draw, "实时运行全景监控大屏")
        self._draw_sidebar(draw, 0, modules)

        # Header Title
        draw.text((250, 145), "系统总体运行监控大屏与实时指标看板", fill=self.text_main, font=get_font(15, bold=True))
        draw.text((250, 168), f"数据采样频率: 1000ms · 集群状态: 正常运行 · 版本: {self.version}", fill=self.text_muted, font=get_font(10))

        # 4 Stat Cards with Mini Sparklines
        cards = ai_cards or [
            {"title": "实时核心业务数据总量", "val": "1,482,904", "unit": "条", "change": "+12.4% 环比增长"},
            {"title": "活跃接入节点与客户端", "val": "358", "unit": "台", "change": "99.8% 正常在线"},
            {"title": "异常自动拦截与响应", "val": "12", "unit": "次", "change": "100% 已闭环处置"},
            {"title": "核心计算处理吞吐量", "val": "4,280", "unit": "QPS", "change": "负载指标优良"},
        ]
        card_accents = [self.primary_color, self.emerald_color, self.amber_color, self.accent_color]

        for idx, c in enumerate(cards[:4]):
            cx = 250 + idx * 285
            cy = 195
            draw_rounded_rect(draw, [(cx, cy), (cx + 270, cy + 105)], radius=10, fill=(255, 255, 255), outline=self.border_color)
            draw.text((cx + 16, cy + 14), str(c.get("title", "核心指标")), fill=self.text_muted, font=get_font(11))
            draw.text((cx + 16, cy + 38), str(c.get("val", "1,000")), fill=self.text_main, font=get_font(19, bold=True))
            draw.text((cx + 145, cy + 44), str(c.get("unit", "")), fill=self.text_muted, font=get_font(10))
            draw.text((cx + 16, cy + 76), str(c.get("change", "正常运行")), fill=card_accents[idx % len(card_accents)], font=get_font(10, bold=True))

            # Draw Mini Sparkline in Card
            sp_pts = [(cx + 175, cy + 85), (cx + 195, cy + 78), (cx + 215, cy + 82), (cx + 235, cy + 70), (cx + 255, cy + 65)]
            for spi in range(len(sp_pts) - 1):
                draw.line([sp_pts[spi], sp_pts[spi + 1]], fill=card_accents[idx % len(card_accents)], width=2)

        # Left Main Chart: 24-Hour Area Trend Curve
        draw_rounded_rect(draw, [(250, 315), (970, 585)], radius=10, fill=(255, 255, 255), outline=self.border_color)
        draw.text((270, 330), "核心业务指标24小时多维运行走势图 (Real-Time Trend)", fill=self.text_main, font=get_font(12, bold=True))
        
        for gy in range(375, 545, 40):
            draw.line([(280, gy), (940, gy)], fill=(241, 245, 249), width=1)

        points = [
            (290, 510), (360, 485), (430, 445), (500, 475), (570, 415),
            (640, 435), (710, 395), (780, 405), (850, 365), (930, 385)
        ]
        for pi in range(len(points) - 1):
            draw.line([points[pi], points[pi + 1]], fill=self.primary_color, width=3)
            draw.ellipse([(points[pi][0] - 4, points[pi][1] - 4), (points[pi][0] + 4, points[pi][1] + 4)], fill=(255, 255, 255), outline=self.primary_color, width=2)

        # Right Chart: Radial Gauge & System Health Index
        draw_rounded_rect(draw, [(990, 315), (1390, 585)], radius=10, fill=(255, 255, 255), outline=self.border_color)
        draw.text((1010, 330), "系统资源与集群健康仪表盘", fill=self.text_main, font=get_font(12, bold=True))

        gauge_cx, gauge_cy = 1190, 450
        draw.ellipse([(gauge_cx - 85, gauge_cy - 85), (gauge_cx + 85, gauge_cy + 85)], fill=self.primary_light, outline=self.primary_color, width=14)
        draw.text((gauge_cx, gauge_cy - 15), "99.9%", fill=self.primary_color, font=get_font(20, bold=True), anchor="mm")
        draw.text((gauge_cx, gauge_cy + 15), "综合健康指数", fill=self.text_muted, font=get_font(10), anchor="mm")

        # Bottom Stream Table
        draw_rounded_rect(draw, [(250, 605), (1390, 840)], radius=10, fill=(255, 255, 255), outline=self.border_color)
        draw.text((270, 620), "最新系统事件与审计流转记录 (Live Activity Stream)", fill=self.text_main, font=get_font(11, bold=True))

        headers = ["序号", "事件记录时间", "操作账号", "业务事件类型", "影响模块对象", "执行结果说明", "状态"]
        hx_offsets = [270, 330, 490, 660, 850, 1080, 1290]
        for hi, htext in enumerate(headers):
            draw.text((hx_offsets[hi], 645), htext, fill=self.text_muted, font=get_font(10, bold=True))

        draw.line([(270, 668), (1370, 668)], fill=self.border_color, width=1)

        first_mod_title = modules[0].get("name", "业务管理模块") if modules else "业务管理模块"
        sample_logs = [
            ("01", "2026-03-20 16:12:05", "admin_super", "系统规则更新", f"{first_mod_title[:10]}", "配置重载并生效", "正常"),
            ("02", "2026-03-20 16:08:12", "service_sync", "数据批量清洗", "实时高频业务管道", "成功处理 2,400 条", "正常"),
            ("03", "2026-03-20 16:05:44", "audit_guard", "安全鉴权校验", "RBAC 权限策略更新", "安全校验通过", "已记录"),
            ("04", "2026-03-20 15:58:30", "cluster_node", "分布式节点心跳", "Worker-Cluster-02", "通信时延 2.1ms", "正常"),
        ]
        for ri, rdata in enumerate(sample_logs):
            ry = 680 + ri * 38
            if ry + 20 > 835:
                break
            for ci, val in enumerate(rdata):
                color = self.emerald_color if val in ("正常", "已记录") else self.text_main
                draw.text((hx_offsets[ci], ry), val, fill=color, font=get_font(10))

        return img

    # =========================================================================
    # Template 3: Data Table Workstation Screen
    # =========================================================================
    def render_table_module(
        self,
        module_name: str,
        custom_headers: Optional[List[str]] = None,
        custom_rows: Optional[List[List[str]]] = None,
        modules: Optional[List[Dict[str, str]]] = None,
        sidebar_idx: int = 1
    ) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height), (248, 250, 252))
        draw = ImageDraw.Draw(img)

        self._draw_common_navbar(draw, module_name)
        self._draw_sidebar(draw, sidebar_idx, modules)

        draw.text((250, 145), f"业务功能管理 / {module_name}", fill=self.text_muted, font=get_font(10))
        draw.text((250, 168), f"{module_name} 数据列表与操作工作台", fill=self.text_main, font=get_font(15, bold=True))

        # Top Filter Bar
        draw_rounded_rect(draw, [(250, 205), (1390, 265)], radius=8, fill=(255, 255, 255), outline=self.border_color)
        draw.text((270, 226), "快速检索:", fill=self.text_muted, font=get_font(10))
        draw_rounded_rect(draw, [(335, 218), (550, 254)], radius=6, fill=(248, 250, 252), outline=self.border_color)
        draw.text((345, 228), "输入编号/关键词检索...", fill=(148, 163, 184), font=get_font(10))

        draw.text((575, 226), "状态筛选:", fill=self.text_muted, font=get_font(10))
        draw_rounded_rect(draw, [(640, 218), (780, 254)], radius=6, fill=(248, 250, 252), outline=self.border_color)
        draw.text((655, 228), "全部状态 ▼", fill=self.text_main, font=get_font(10))

        # Buttons
        draw_rounded_rect(draw, [(1060, 218), (1170, 254)], radius=6, fill=self.primary_color)
        draw.text((1115, 228), "+ 新增记录", fill=(255, 255, 255), font=get_font(10, bold=True), anchor="mt")

        draw_rounded_rect(draw, [(1185, 218), (1280, 254)], radius=6, fill=(241, 245, 249), outline=self.border_color)
        draw.text((1232, 228), "批量导出", fill=self.text_main, font=get_font(10), anchor="mt")

        draw_rounded_rect(draw, [(1295, 218), (1370, 254)], radius=6, fill=(241, 245, 249), outline=self.border_color)
        draw.text((1332, 228), "刷新", fill=self.text_main, font=get_font(10), anchor="mt")

        # Table Container
        draw_rounded_rect(draw, [(250, 280), (1390, 830)], radius=10, fill=(255, 255, 255), outline=self.border_color)

        raw_headers = custom_headers or ["业务编号", "主要业务对象", "所属分类/维度", "核心参数指标", "更新登记时间", "流转状态"]
        headers = ["选择"] + raw_headers[:6] + ["操作指令"]
        hx_offsets = [270, 320, 490, 670, 840, 1020, 1180, 1290]

        draw.rectangle([(251, 281), (1389, 320)], fill=(248, 250, 252))
        for hi, htext in enumerate(headers):
            if hi < len(hx_offsets):
                draw.text((hx_offsets[hi], 295), str(htext)[:10], fill=self.text_muted, font=get_font(10, bold=True))

        draw.line([(250, 320), (1390, 320)], fill=self.border_color, width=1)

        rows = custom_rows or [
            ["REC-2026-001", "核心业务实体A1", "标准业务流", "指标正常: 99.8%", "2026-03-20 16:10:02", "正常"],
            ["REC-2026-002", "核心业务实体A2", "高优先级任务", "处理中: 85.0%", "2026-03-20 16:08:44", "处理中"],
            ["REC-2026-003", "核心业务实体B1", "标准业务流", "核验通过: 100%", "2026-03-20 16:05:12", "已完成"],
            ["REC-2026-004", "核心业务实体B2", "归档业务集", "指标正常: 99.2%", "2026-03-20 16:01:09", "正常"],
            ["REC-2026-005", "核心业务实体C1", "标准业务流", "安全存证已固化", "2026-03-20 15:55:30", "已存证"],
            ["REC-2026-006", "核心业务实体C2", "标准业务流", "指标正常: 98.9%", "2026-03-20 15:50:11", "正常"],
            ["REC-2026-007", "核心业务实体D1", "高频接入事务", "自适应抗噪清洗", "2026-03-20 15:45:00", "正常"],
        ]

        for ri, rdata in enumerate(rows[:7]):
            ry = 340 + ri * 65
            if ry + 30 > 790:
                break
            draw_rounded_rect(draw, [(270, ry - 2), (284, ry + 12)], radius=3, fill=(255, 255, 255), outline=(203, 213, 225))
            
            for ci, cell_val in enumerate(rdata[:5]):
                col_idx = ci + 1
                if col_idx < len(hx_offsets):
                    txt = str(cell_val)[:14]
                    color = self.primary_color if col_idx == 1 else (self.text_muted if col_idx == 5 else self.text_main)
                    draw.text((hx_offsets[col_idx], ry), txt, fill=color, font=get_font(10, bold=(col_idx==1)))

            status_text = str(rdata[5]) if len(rdata) > 5 else "正常"
            is_success = any(k in status_text for k in ["正常", "完成", "合格", "成功", "达标", "已归档", "已存证", "在职", "通过", "合规"])
            status_color = self.emerald_color if is_success else self.amber_color
            bg_color = (240, 253, 244) if is_success else (254, 243, 199)

            draw_rounded_rect(draw, [(hx_offsets[6] - 4, ry - 4), (hx_offsets[6] + 68, ry + 16)], radius=4, fill=bg_color)
            draw.text((hx_offsets[6] + 6, ry), status_text[:6], fill=status_color, font=get_font(10, bold=True))

            draw.text((hx_offsets[7], ry), "详情 · 编辑 · 溯源", fill=self.primary_color, font=get_font(10))
            draw.line([(250, ry + 36), (1390, ry + 36)], fill=(241, 245, 249), width=1)

        draw.text((270, 795), "共 1,248 条业务记录，每页 10 条", fill=self.text_muted, font=get_font(10))
        draw_rounded_rect(draw, [(1220, 785), (1370, 818)], radius=6, fill=(248, 250, 252), outline=self.border_color)
        draw.text((1295, 795), " <  1  2  3  4  > ", fill=self.text_main, font=get_font(10), anchor="mt")

        return img

    # =========================================================================
    # Template 4: 3-Column Kanban Board & Workflow Swimlane
    # =========================================================================
    def render_kanban_board_module(
        self,
        module_name: str,
        custom_rows: Optional[List[List[str]]] = None,
        modules: Optional[List[Dict[str, str]]] = None,
        sidebar_idx: int = 2
    ) -> Image.Image:
        """Render 3-Column agile Kanban workflow board with cards."""
        img = Image.new("RGB", (self.width, self.height), (248, 250, 252))
        draw = ImageDraw.Draw(img)

        self._draw_common_navbar(draw, module_name)
        self._draw_sidebar(draw, sidebar_idx, modules)

        draw.text((250, 145), f"敏捷看板 / {module_name}", fill=self.text_muted, font=get_font(10))
        draw.text((250, 168), f"{module_name} 业务流转敏捷看板", fill=self.text_main, font=get_font(15, bold=True))

        # 3 Columns
        col_w = 360
        col_h = 630
        columns = [
            ("📋 待处理 / 待调度 (8)", (241, 245, 249), self.primary_color, [
                ("TSK-2026-001", "核心业务参数初始化校验", "高优先级", "负责人: 张工", (254, 226, 226), self.rose_color),
                ("TSK-2026-002", "高频数据接入通道联调", "中优先级", "负责人: 李工", (254, 243, 199), self.amber_color),
            ]),
            ("⚡ 进行中 / 状态机流转 (4)", (238, 242, 255), self.indigo_color, [
                ("TSK-2026-003", "多源数据自适应抗噪过滤", "处理中 75%", "负责人: 王工", (240, 249, 255), self.primary_color),
                ("TSK-2026-004", "分布式事务原子性存证", "处理中 90%", "负责人: 赵工", (240, 249, 255), self.primary_color),
            ]),
            ("✓ 已完成 / 归档存证 (26)", (240, 253, 244), self.emerald_color, [
                ("TSK-2026-005", "安全哈希与数字签名生成", "已完成 100%", "校验项: 16/16", (240, 253, 244), self.emerald_color),
                ("TSK-2026-006", "全生命周期审计日志固化", "已完成 100%", "永久存证归档", (240, 253, 244), self.emerald_color),
            ]),
        ]

        for ci, (c_title, c_bg, c_topcol, c_tasks) in enumerate(columns):
            cx = 250 + ci * (col_w + 20)
            cy = 205

            draw_rounded_rect(draw, [(cx, cy), (cx + col_w, cy + col_h)], radius=10, fill=c_bg, outline=self.border_color)
            draw.rectangle([(cx + 1, cy + 1), (cx + col_w - 1, cy + 8)], fill=c_topcol)
            draw.text((cx + 16, cy + 20), c_title, fill=self.text_main, font=get_font(12, bold=True))

            # Task Cards
            for ti, (t_code, t_name, t_tag, t_sub, t_tag_bg, t_tag_col) in enumerate(c_tasks):
                tx = cx + 12
                ty = cy + 55 + ti * 160
                draw_rounded_rect(draw, [(tx, ty), (tx + col_w - 24, ty + 145)], radius=8, fill=(255, 255, 255), outline=self.border_color)
                
                draw.text((tx + 14, ty + 14), t_code, fill=self.primary_color, font=get_font(10, bold=True))
                draw.text((tx + 14, ty + 36), t_name, fill=self.text_main, font=get_font(12, bold=True))

                draw_rounded_rect(draw, [(tx + 14, ty + 68), (tx + 110, ty + 92)], radius=4, fill=t_tag_bg)
                draw.text((tx + 22, ty + 73), t_tag, fill=t_tag_col, font=get_font(9, bold=True))

                draw.line([(tx + 14, ty + 105), (tx + col_w - 38, ty + 105)], fill=self.border_color, width=1)
                draw.text((tx + 14, ty + 118), t_sub, fill=self.text_muted, font=get_font(9))

        return img

    # =========================================================================
    # Template 5: Multi-Chart Analytics & Bar/Line Studio
    # =========================================================================
    def render_analytics_chart_module(
        self,
        module_name: str,
        modules: Optional[List[Dict[str, str]]] = None,
        sidebar_idx: int = 3
    ) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height), (248, 250, 252))
        draw = ImageDraw.Draw(img)

        self._draw_common_navbar(draw, module_name)
        self._draw_sidebar(draw, sidebar_idx, modules)

        draw.text((250, 145), f"数据智能分析 / {module_name}", fill=self.text_muted, font=get_font(10))
        draw.text((250, 168), f"{module_name} 多维统计与图表分析工作台", fill=self.text_main, font=get_font(15, bold=True))

        top_kpi = [
            ("本期业务总量", "1,842,900", "环比 +15.4% ↑", self.primary_color),
            ("均值计算耗时", "14.2 ms", "响应达标 99.9%", self.emerald_color),
            ("多维数据完整率", "99.98%", "全生命周期校验", self.accent_color),
        ]
        for ki, (ktitle, kval, ksub, kcol) in enumerate(top_kpi):
            kx = 250 + ki * 385
            ky = 205
            draw_rounded_rect(draw, [(kx, ky), (kx + 365, ky + 90)], radius=10, fill=(255, 255, 255), outline=self.border_color)
            draw.text((kx + 16, ky + 14), ktitle, fill=self.text_muted, font=get_font(11))
            draw.text((kx + 16, ky + 36), kval, fill=self.text_main, font=get_font(18, bold=True))
            draw.text((kx + 16, ky + 66), ksub, fill=kcol, font=get_font(10, bold=True))

        # Chart 1: 7-Day Vertical Bar Chart
        draw_rounded_rect(draw, [(250, 315), (790, 625)], radius=10, fill=(255, 255, 255), outline=self.border_color)
        draw.text((270, 330), "近7日业务吞吐量柱状统计图 (Daily Throughput)", fill=self.text_main, font=get_font(12, bold=True))

        bar_days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        bar_heights = [130, 160, 200, 170, 240, 150, 120]
        bar_base_y = 575

        for gy in range(375, 580, 45):
            draw.line([(280, gy), (770, gy)], fill=(241, 245, 249), width=1)

        for bi, (bday, bh) in enumerate(zip(bar_days, bar_heights)):
            bx = 300 + bi * 65
            draw_rounded_rect(draw, [(bx, bar_base_y - bh), (bx + 36, bar_base_y)], radius=6, fill=self.primary_color)
            draw.text((bx + 18, bar_base_y + 10), bday, fill=self.text_muted, font=get_font(9), anchor="mt")
            draw.text((bx + 18, bar_base_y - bh - 18), str(bh * 10), fill=self.text_main, font=get_font(9, bold=True), anchor="mt")

        # Chart 2: Double Line Comparison
        draw_rounded_rect(draw, [(810, 315), (1390, 625)], radius=10, fill=(255, 255, 255), outline=self.border_color)
        draw.text((830, 330), "实时处理性能与响应时延走势对比 (Latency Trend)", fill=self.text_main, font=get_font(12, bold=True))

        draw.rectangle([(1180, 335), (1200, 343)], fill=self.primary_color)
        draw.text((1206, 332), "吞吐 (QPS)", fill=self.text_muted, font=get_font(9))
        draw.rectangle([(1290, 335), (1310, 343)], fill=self.emerald_color)
        draw.text((1316, 332), "时延 (ms)", fill=self.text_muted, font=get_font(9))

        for gy in range(375, 580, 45):
            draw.line([(840, gy), (1370, gy)], fill=(241, 245, 249), width=1)

        pts1 = [(850, 530), (930, 480), (1010, 450), (1090, 420), (1170, 400), (1250, 370), (1350, 350)]
        pts2 = [(850, 560), (930, 540), (1010, 530), (1090, 550), (1170, 520), (1250, 510), (1350, 500)]

        for pi in range(len(pts1) - 1):
            draw.line([pts1[pi], pts1[pi + 1]], fill=self.primary_color, width=3)
            draw.ellipse([(pts1[pi][0] - 3, pts1[pi][1] - 3), (pts1[pi][0] + 3, pts1[pi][1] + 3)], fill=(255, 255, 255), outline=self.primary_color, width=2)
            draw.line([pts2[pi], pts2[pi + 1]], fill=self.emerald_color, width=2)
            draw.ellipse([(pts2[pi][0] - 3, pts2[pi][1] - 3), (pts2[pi][0] + 3, pts2[pi][1] + 3)], fill=(255, 255, 255), outline=self.emerald_color, width=2)

        # Bottom Breakdown
        draw_rounded_rect(draw, [(250, 645), (1390, 835)], radius=10, fill=(255, 255, 255), outline=self.border_color)
        draw.text((270, 660), "多维数据报表汇总切片明细", fill=self.text_main, font=get_font(11, bold=True))

        h_cols = ["统计周期", "业务总量 (笔)", "成功率 (%)", "峰值 QPS", "异常拦截", "最后结算归档"]
        c_offsets = [270, 460, 650, 840, 1030, 1220]
        for ci, ch in enumerate(h_cols):
            draw.text((c_offsets[ci], 685), ch, fill=self.text_muted, font=get_font(10, bold=True))

        draw.line([(270, 708), (1370, 708)], fill=self.border_color, width=1)

        b_rows = [
            ("2026年第1季度汇总", "1,248,900 笔", "99.98%", "4,280 QPS", "0 起遗漏", "已归档存证"),
            ("2026年3月份月度明细", "452,100 笔", "99.95%", "3,890 QPS", "1 起处置", "已审核入库"),
            ("2026年第11周周报", "112,400 笔", "100.0%", "3,450 QPS", "0 起异常", "已核算完成"),
        ]
        for ri, rvals in enumerate(b_rows):
            ry = 720 + ri * 38
            if ry + 20 > 830:
                break
            for ci, val in enumerate(rvals):
                col = self.emerald_color if "已" in val else self.text_main
                draw.text((c_offsets[ci], ry), val, fill=col, font=get_font(10))

        return img

    # =========================================================================
    # Template 6: Stepper Pipeline & Detail Audit Screen
    # =========================================================================
    def render_stepper_detail_module(
        self,
        module_name: str,
        modules: Optional[List[Dict[str, str]]] = None,
        sidebar_idx: int = 4
    ) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height), (248, 250, 252))
        draw = ImageDraw.Draw(img)

        self._draw_common_navbar(draw, module_name)
        self._draw_sidebar(draw, sidebar_idx, modules)

        draw.text((250, 145), f"业务流转追踪 / {module_name}", fill=self.text_muted, font=get_font(10))
        draw.text((250, 168), f"{module_name} 业务全生命周期流转与详情追溯", fill=self.text_main, font=get_font(15, bold=True))

        # Top 4-Step Stepper Box
        draw_rounded_rect(draw, [(250, 205), (1390, 310)], radius=10, fill=(255, 255, 255), outline=self.border_color)
        draw.text((270, 220), "业务状态流转链路 (Workflow Stepper):", fill=self.text_muted, font=get_font(11, bold=True))

        steps = [
            ("1. 业务接入受理", "已校验完成", self.emerald_color, "✓"),
            ("2. 自适应规则匹配", "状态机流转中", self.primary_color, "2"),
            ("3. 核心计算与处理", "调度排队中", self.text_muted, "3"),
            ("4. 哈希存证与归档", "待执行闭环", self.text_muted, "4"),
        ]

        step_w = 260
        for si, (s_title, s_sub, s_col, s_num) in enumerate(steps):
            sx = 280 + si * step_w
            sy = 260
            draw.ellipse([(sx, sy - 14), (sx + 28, sy + 14)], fill=s_col)
            draw.text((sx + 14, sy), s_num, fill=(255, 255, 255), font=get_font(10, bold=True), anchor="mm")
            draw.text((sx + 36, sy - 10), s_title, fill=self.text_main, font=get_font(11, bold=True))
            draw.text((sx + 36, sy + 8), s_sub, fill=s_col, font=get_font(9))
            if si < len(steps) - 1:
                draw.line([(sx + 165, sy), (sx + step_w - 15, sy)], fill=self.border_color, width=2)

        # Main Property Sheet
        draw_rounded_rect(draw, [(250, 325), (880, 835)], radius=10, fill=(255, 255, 255), outline=self.border_color)
        draw.text((270, 345), "业务实体详细属性与元数据清单", fill=self.text_main, font=get_font(12, bold=True))

        props = [
            ("全局业务追踪流水号 (TraceID):", "TRC-2026-X8890241-SHA256"),
            ("所属业务批次与规格分类:", "高优先级核心业务事务流 (Batch-A1)"),
            ("系统接入协议与安全模式:", "gRPC / TLS 1.3 / 双向认证 Token"),
            ("当前流转节点与处理人:", "智能计算引擎中心 · Worker-Node-04"),
            ("数据合法性校验结果:", "100% 通过 (校验项: 16/16 规则全部达标)"),
            ("数字签名与哈希存证值:", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4..."),
            ("最后一次状态流转时间戳:", "2026-03-20 16:15:30 (UTC+8)"),
            ("安全审计与合规等级:", "最高合规防护级 · 永久留存审计链"),
        ]

        for pi, (plabel, pval) in enumerate(props):
            py = 375 + pi * 54
            if py + 40 > 830:
                break
            draw.text((270, py), plabel, fill=self.text_muted, font=get_font(9, bold=True))
            draw_rounded_rect(draw, [(270, py + 15), (860, py + 42)], radius=6, fill=(248, 250, 252), outline=self.border_color)
            draw.text((280, py + 21), pval, fill=self.text_main, font=get_font(10))

        # Right Action Log
        draw_rounded_rect(draw, [(900, 325), (1390, 835)], radius=10, fill=(255, 255, 255), outline=self.border_color)
        draw.text((920, 345), "状态变更时序日志 (Audit Timeline)", fill=self.text_main, font=get_font(12, bold=True))

        timeline_logs = [
            ("16:15:30", "系统自动校验通过，进入就绪态", self.emerald_color),
            ("16:15:12", "状态机触发规则引擎条件匹配", self.primary_color),
            ("16:14:48", "多源数据采集与抗噪清洗完成", self.primary_color),
            ("16:14:20", "客户端发起业务请求，生成追踪ID", self.text_muted),
            ("16:13:05", "安全访问网关完成鉴权握手", self.emerald_color),
        ]

        for ti, (ttime, ttext, tcolor) in enumerate(timeline_logs):
            ty = 390 + ti * 68
            draw.ellipse([(920, ty), (932, ty + 12)], fill=tcolor)
            draw.text((945, ty - 2), ttime, fill=self.text_muted, font=get_font(9, bold=True))
            draw.text((945, ty + 16), ttext, fill=self.text_main, font=get_font(10))
            if ti < len(timeline_logs) - 1:
                draw.line([(926, ty + 14), (926, ty + 66)], fill=self.border_color, width=2)

        # Seal Stamp
        draw.ellipse([(1220, 690), (1350, 810)], fill=(240, 253, 244), outline=self.emerald_color, width=3)
        draw.text((1285, 740), "安全存证", fill=self.emerald_color, font=get_font(13, bold=True), anchor="mm")
        draw.text((1285, 765), "已核验", fill=self.emerald_color, font=get_font(9), anchor="mm")

        return img

    # =========================================================================
    # Template 7: Topology Network & Service Mesh Screen
    # =========================================================================
    def render_topology_network_module(
        self,
        module_name: str,
        modules: Optional[List[Dict[str, str]]] = None,
        sidebar_idx: int = 1
    ) -> Image.Image:
        img = Image.new("RGB", (self.width, self.height), (248, 250, 252))
        draw = ImageDraw.Draw(img)

        self._draw_common_navbar(draw, module_name)
        self._draw_sidebar(draw, sidebar_idx, modules)

        draw.text((250, 145), f"集群架构拓扑 / {module_name}", fill=self.text_muted, font=get_font(10))
        draw.text((250, 168), f"{module_name} 节点服务通信与链路拓扑图", fill=self.text_main, font=get_font(15, bold=True))

        draw_rounded_rect(draw, [(250, 205), (1390, 835)], radius=12, fill=(255, 255, 255), outline=self.border_color)

        for gx in range(270, 1370, 40):
            for gy in range(220, 820, 40):
                draw.point((gx, gy), fill=(226, 232, 240))

        gw_x, gw_y = 820, 280
        draw_rounded_rect(draw, [(gw_x - 130, gw_y - 35), (gw_x + 130, gw_y + 35)], radius=10, fill=self.primary_light, outline=self.primary_color, width=2)
        draw.text((gw_x, gw_y - 12), "⚡ API 服务集群智能网关", fill=self.primary_color, font=get_font(12, bold=True), anchor="mm")
        draw.text((gw_x, gw_y + 12), "吞吐: 4,280 QPS · 时延: 2ms", fill=self.text_muted, font=get_font(9), anchor="mm")

        nodes = [
            ("NODE-01 业务核心计算单元", "承载率: 45% · 正常", 420, 480, self.emerald_color),
            ("NODE-02 数据接入清洗管道", "速率: 1.2k/s · 正常", 680, 480, self.primary_color),
            ("NODE-03 状态机流转引擎", "活跃任务: 128 · 正常", 940, 480, self.accent_color),
            ("NODE-04 永久存证安全节点", "哈希校验: 100% · 正常", 1200, 480, self.purple_color),
        ]

        for n_name, n_sub, nx, ny, ncol in nodes:
            draw.line([(gw_x, gw_y + 35), (nx, ny - 35)], fill=self.border_color, width=2)
            draw_rounded_rect(draw, [(nx - 110, ny - 35), (nx + 110, ny + 35)], radius=8, fill=(255, 255, 255), outline=ncol, width=2)
            draw.text((nx, ny - 10), n_name, fill=self.text_main, font=get_font(10, bold=True), anchor="mm")
            draw.text((nx, ny + 12), n_sub, fill=ncol, font=get_font(9), anchor="mm")

        db_x, db_y = 820, 710
        for _, _, nx, ny, _ in nodes:
            draw.line([(nx, ny + 35), (db_x, db_y - 35)], fill=self.border_color, width=2)

        draw_rounded_rect(draw, [(db_x - 160, db_y - 35), (db_x + 160, db_y + 35)], radius=10, fill=(240, 253, 244), outline=self.emerald_color, width=2)
        draw.text((db_x, db_y - 12), "🗄️ 分布式多级存储与缓存集群", fill=self.emerald_color, font=get_font(12, bold=True), anchor="mm")
        draw.text((db_x, db_y + 12), "双活容灾架构 · RPO=0 · 自动故障转移", fill=self.text_muted, font=get_font(9), anchor="mm")

        return img

    # =========================================================================
    # Template 8: Dark Terminal & Log Stream Console
    # =========================================================================
    def render_terminal_console_module(
        self,
        module_name: str,
        modules: Optional[List[Dict[str, str]]] = None,
        sidebar_idx: int = 2
    ) -> Image.Image:
        """Render high-tech dark terminal & real-time log stream console."""
        img = Image.new("RGB", (self.width, self.height), (248, 250, 252))
        draw = ImageDraw.Draw(img)

        self._draw_common_navbar(draw, module_name)
        self._draw_sidebar(draw, sidebar_idx, modules)

        draw.text((250, 145), f"系统运维终端 / {module_name}", fill=self.text_muted, font=get_font(10))
        draw.text((250, 168), f"{module_name} 实时日志流与运维控制台", fill=self.text_main, font=get_font(15, bold=True))

        # Dark Terminal Container
        term_x, term_y = 250, 205
        term_w, term_h = 1140, 630
        draw_rounded_rect(draw, [(term_x, term_y), (term_x + term_w, term_y + term_h)], radius=12, fill=(15, 23, 42), outline=(51, 65, 85))

        # Terminal Header Bar
        draw.rectangle([(term_x, term_y), (term_x + term_w, term_y + 40)], fill=(30, 41, 59))
        draw.ellipse([(term_x + 15, term_y + 14), (term_x + 27, term_y + 26)], fill=(239, 68, 68))
        draw.ellipse([(term_x + 35, term_y + 14), (term_x + 47, term_y + 26)], fill=(245, 158, 11))
        draw.ellipse([(term_x + 55, term_y + 14), (term_x + 67, term_y + 26)], fill=(16, 185, 129))

        draw.text((term_x + 85, term_y + 13), f"bash - cluster-node-01@{self.software_name[:10]}:~# tail -f /var/log/audit.log", fill=(203, 213, 225), font=get_font(10))

        # Terminal Log Stream Lines
        logs = [
            ("[2026-03-20 16:15:00.102]", "[INFO]", ">>> Booting microservice container [instance_id: cluster-01-a] ...", (148, 163, 184)),
            ("[2026-03-20 16:15:00.245]", "[INFO]", "TLS 1.3 handshake successful. Cipher: ECDHE-RSA-AES256-GCM-SHA384", (56, 189, 248)),
            ("[2026-03-20 16:15:00.412]", "[SUCCESS]", "Connected to PostgreSQL Cluster (Primary). Active pool size: 64", (74, 222, 128)),
            ("[2026-03-20 16:15:01.005]", "[METRIC]", "Kafka message pipeline initialized: topic [biz_event_stream] ready", (192, 132, 252)),
            ("[2026-03-20 16:15:02.110]", "[INFO]", "Starting worker threads: 16 daemon workers allocated", (148, 163, 184)),
            ("[2026-03-20 16:15:03.450]", "[SUCCESS]", "Adaptive Kalman Filter loaded. Sample rate: 1000ms", (74, 222, 128)),
            ("[2026-03-20 16:15:05.120]", "[WARN]", "Memory threshold inspection: Heap 32.4% (Normal, below 75% limit)", (251, 191, 36)),
            ("[2026-03-20 16:15:06.880]", "[INFO]", "Heartbeat broadcast ACK received from 12 edge nodes. Ping: 1.4ms", (56, 189, 248)),
            ("[2026-03-20 16:15:08.200]", "[SUCCESS]", "SHA-256 block hash verified: 9b2d8e41c5a7... (Proof valid)", (74, 222, 128)),
            ("[2026-03-20 16:15:10.000]", "[INFO]", "System status: ALL_SERVICES_OPERATIONAL. Listening on port 8000...", (148, 163, 184)),
        ]

        for li, (ltime, ltag, lmsg, lcol) in enumerate(logs):
            ly = term_y + 55 + li * 44
            draw.text((term_x + 20, ly), ltime, fill=(100, 116, 139), font=get_font(10))
            draw.text((term_x + 195, ly), ltag, fill=lcol, font=get_font(10, bold=True))
            draw.text((term_x + 285, ly), lmsg, fill=(241, 245, 249), font=get_font(10))

        # Blinking cursor
        draw.rectangle([(term_x + 20, term_y + 510), (term_x + 30, term_y + 526)], fill=(74, 222, 128))
        draw.text((term_x + 38, term_y + 512), "cluster-admin@node:~$ _", fill=(148, 163, 184), font=get_font(10))

        return img

    # =========================================================================
    # Template 9: Visual Rule Engine & Parameter Config Modal
    # =========================================================================
    def render_rule_engine_modal(self, module_name: str, custom_params: Optional[List[Dict[str, str]]] = None) -> Image.Image:
        img = self.render_table_module(module_name)
        overlay = Image.new("RGBA", (self.width, self.height), (15, 23, 42, 120))
        img.paste(overlay, (0, 0), overlay)

        draw = ImageDraw.Draw(img)
        mw, mh = 680, 560
        mx, my = (self.width - mw) // 2, (self.height - mh) // 2
        draw_rounded_rect(draw, [(mx, my), (mx + mw, my + mh)], radius=14, fill=(255, 255, 255), outline=self.border_color)

        draw.text((mx + 30, my + 25), f"⚙️ {module_name} - 规则引擎与业务参数配置", fill=self.text_main, font=get_font(14, bold=True))

        tab_names = ["基础配置", "规则判定", "通知通道", "安全策略"]
        for ti, tname in enumerate(tab_names):
            tx = mx + 30 + ti * 85
            is_active = (ti == 0)
            draw.text((tx, my + 58), tname, fill=self.primary_color if is_active else self.text_muted, font=get_font(11, bold=is_active))
            if is_active:
                draw.line([(tx - 2, my + 78), (tx + 50, my + 78)], fill=self.primary_color, width=2)

        draw.line([(mx, my + 80), (mx + mw, my + 80)], fill=self.border_color, width=1)

        labels = []
        if custom_params:
            for p in custom_params[:5]:
                labels.append((str(p.get("label", "核心业务参数:")), str(p.get("val", "标准生产配置值"))))
        else:
            labels = [
                ("采样周期与调度频率 (毫秒):", "5000 ms (高频实时采集与状态调度)"),
                ("上限阈值告警触发条件 (High Limit):", "业务数值偏离基准 > +15.0% 自动触发"),
                ("下限阈值预警判定条件 (Low Limit):", "业务数值偏离基准 < -15.0% 自动预警"),
                ("自适应数据清洗抗噪算法模式:", "卡尔曼滤波与滑动窗口自适应算法 (Kalman)"),
                ("异常通知自动分发多维渠道:", "系统站内信、邮件通知、WebSocket 实时弹窗"),
            ]

        for fi, (lbl, val) in enumerate(labels[:5]):
            fy = my + 95 + fi * 62
            draw.text((mx + 30, fy), lbl[:32], fill=self.text_main, font=get_font(10, bold=True))
            draw_rounded_rect(draw, [(mx + 30, fy + 20), (mx + mw - 30, fy + 50)], radius=6, fill=(248, 250, 252), outline=(203, 213, 225))
            draw.text((mx + 42, fy + 28), val[:42], fill=self.text_main, font=get_font(10))

        draw.line([(mx, my + mh - 60), (mx + mw, my + mh - 60)], fill=self.border_color, width=1)
        draw_rounded_rect(draw, [(mx + mw - 200, my + mh - 48), (mx + mw - 115, my + mh - 16)], radius=6, fill=(241, 245, 249), outline=self.border_color)
        draw.text((mx + mw - 158, my + mh - 38), "取消", fill=self.text_main, font=get_font(10), anchor="mt")

        draw_rounded_rect(draw, [(mx + mw - 100, my + mh - 48), (mx + mw - 25, my + mh - 16)], radius=6, fill=self.primary_color)
        draw.text((mx + mw - 62, my + mh - 38), "保存配置", fill=(255, 255, 255), font=get_font(10, bold=True), anchor="mt")

        return img

    # =========================================================================
    # Orchestrator: Generate All Diverse UI Mockups
    # =========================================================================
    def generate_all_mockups(self, modules: List[Dict[str, str]], ui_mockup_data: Optional[Dict[str, Any]] = None) -> Dict[str, bytes]:
        """
        Generate full set of 6-8 diverse, multi-template UI mockup screenshots.
        """
        results: Dict[str, bytes] = {}
        ui_data = ui_mockup_data or {}
        ai_cards = ui_data.get("dashboard_cards")
        ai_tables = ui_data.get("module_tables", {})
        ai_config_params = ui_data.get("config_params")

        # 1. Login Screen
        img_login = self.render_login_screen()
        b_login = io.BytesIO()
        img_login.save(b_login, format="PNG")
        results["login"] = b_login.getvalue()

        # 2. Dashboard Screen
        img_dash = self.render_dashboard_screen(modules, ai_cards=ai_cards)
        b_dash = io.BytesIO()
        img_dash.save(b_dash, format="PNG")
        results["dashboard"] = b_dash.getvalue()

        # Layout Dispatcher for Modules
        for i, mod in enumerate(modules[:4]):
            m_code = mod.get("code", f"M0{i+1}")
            m_name = mod.get("name", f"业务模块_{i+1}")
            m_lower = m_name.lower()
            mod_table_info = ai_tables.get(m_code) or ai_tables.get(f"M0{i+1}") or {}
            custom_headers = mod_table_info.get("headers")
            custom_rows = mod_table_info.get("rows")

            if i == 0:
                # Module 1: Data Table View
                img_mod = self.render_table_module(
                    module_name=m_name,
                    custom_headers=custom_headers,
                    custom_rows=custom_rows,
                    modules=modules,
                    sidebar_idx=1
                )
            elif i == 1:
                # Module 2: Kanban or Topology
                if any(k in m_lower for k in ["拓扑", "网络", "设备", "集群", "节点", "网关", "通信", "硬件", "激光"]):
                    img_mod = self.render_topology_network_module(m_name, modules, sidebar_idx=2)
                elif any(k in m_lower for k in ["任务", "工单", "排班", "调度", "进销存", "处方", "挂号"]):
                    img_mod = self.render_kanban_board_module(m_name, custom_rows=custom_rows, modules=modules, sidebar_idx=2)
                else:
                    img_mod = self.render_kanban_board_module(m_name, custom_rows=custom_rows, modules=modules, sidebar_idx=2)
            elif i == 2:
                # Module 3: Analytics Studio or Terminal Console
                if any(k in m_lower for k in ["统计", "分析", "报表", "大屏", "可视化", "指数", "能耗"]):
                    img_mod = self.render_analytics_chart_module(m_name, modules, sidebar_idx=3)
                elif any(k in m_lower for k in ["日志", "运维", "终端", "监控", "审计", "采集"]):
                    img_mod = self.render_terminal_console_module(m_name, modules, sidebar_idx=3)
                else:
                    img_mod = self.render_analytics_chart_module(m_name, modules, sidebar_idx=3)
            else:
                # Module 4: Stepper Pipeline or Terminal Console
                if any(k in m_lower for k in ["流转", "审批", "工单", "溯源", "轨迹", "生命周期", "核销"]):
                    img_mod = self.render_stepper_detail_module(m_name, modules, sidebar_idx=4)
                else:
                    img_mod = self.render_stepper_detail_module(m_name, modules, sidebar_idx=4)

            b_mod = io.BytesIO()
            img_mod.save(b_mod, format="PNG")
            results[f"module_{i+1}"] = b_mod.getvalue()

        # 7. Config Modal
        first_mod_name = modules[0].get("name", "核心业务参数") if modules else "核心业务参数"
        img_modal = self.render_rule_engine_modal(first_mod_name, custom_params=ai_config_params)
        b_modal = io.BytesIO()
        img_modal.save(b_modal, format="PNG")
        results["config_modal"] = b_modal.getvalue()

        return results
