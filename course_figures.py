"""Draw the first lessons' SVG diagrams without external dependencies."""

from html import escape

FONT = "system-ui, -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif"
INK = "#14243b"
MUTED = "#4c5f79"
ACCENT = "#164bc4"
BLUE = "#385984"
RED = "#a3362e"
COLORS = {
    "neutral": ("#ffffff", "#dbe4ef", INK),
    "accent": ("#eaf2ff", "#a9c4f6", ACCENT),
    "blue": ("#eef2f8", "#b3c4db", BLUE),
    "amber": ("#faf0d9", "#d4b776", "#77520c"),
    "red": ("#fbe9e6", "#e1aaa2", RED),
}


class Figure:
    def __init__(self, title, height):
        self.height = height
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="640" height="{height}" viewBox="0 0 640 {height}">',
            f"<title>{escape(title)}</title>",
            "<defs>",
        ]
        for name, color in (("ink", MUTED), ("accent", ACCENT), ("red", RED), ("blue", BLUE)):
            self.parts.append(
                f'<marker id="{name}" viewBox="0 0 10 10" refX="8" refY="5" '
                f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M 0 1 L 8 5 L 0 9 z" fill="{color}"/></marker>'
            )
        self.parts.extend(("</defs>", f'<g font-family="{FONT}">'))
        self.rect(1, 1, 638, height - 2, "#f5f8fe", "#dbe4ef", 18)

    def rect(self, x, y, w, h, fill, stroke="none", radius=12):
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'
        )

    def text(self, x, y, content, size=22, color=INK, weight=550, anchor="start"):
        self.parts.append(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}">{escape(content)}</text>'
        )

    def box(self, x, y, w, h, title, detail="", tone="neutral"):
        fill, border, ink = COLORS[tone]
        self.rect(x, y, w, h, fill, border)
        self.text(x + w / 2, y + (h / 2 - 4 if detail else h / 2 + 8), title, 23, ink, 680, "middle")
        if detail:
            self.text(x + w / 2, y + h / 2 + 22, detail, 20, ink, 500, "middle")

    def path(self, points, color=MUTED, width=2.5, end=None, dashed=False):
        line = " ".join(f"{x},{y}" for x, y in points)
        marker = f' marker-end="url(#{end})"' if end else ""
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        self.parts.append(
            f'<polyline points="{line}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linecap="round" stroke-linejoin="round"{marker}{dash}/>'
        )

    def arrow(self, *points, tone="ink"):
        color = {"ink": MUTED, "accent": ACCENT, "red": RED, "blue": BLUE}[tone]
        self.path(points, color, end=tone)

    def dot(self, x, y, r, fill, stroke="none"):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}"/>')

    def write(self, path):
        path.write_text("\n".join((*self.parts, "</g></svg>", "")), encoding="utf-8")


def policy_paths():
    fig = Figure("同一个任务的三种实现", 468)
    fig.box(24, 20, 592, 56, "同一输入：当前观察 + 搬运指令")
    paths = [
        ("VLA", "图像与指令", "预测动作", "一步或一段", "下发动作", "blue"),
        ("WAM", "未来变化建模", "学习动作", "如联合预测", "下发动作", "amber"),
        ("机器人 Agent", "目标与反馈", "选择下一步", "工具或程序", "执行技能", "accent"),
    ]
    for index, (name, detail, process, note, output, tone) in enumerate(paths):
        y = 100 + 96 * index
        fig.box(24, y, 170, 74, name, detail, tone)
        fig.arrow((202, y + 37), (230, y + 37))
        fig.box(238, y, 174, 74, process, note)
        fig.arrow((420, y + 37), (448, y + 37))
        fig.box(456, y, 160, 74, output, tone=tone)
    fig.box(24, 396, 592, 51, "执行后获取新观察，可进入下一轮")
    return fig


def module_map():
    fig = Figure("从传统机器人模块到本课实现", 460)
    fig.text(40, 42, "模块化机器人常见职责", weight=700)
    fig.text(340, 42, "本课实现", weight=700)
    rows = [
        ("感知与状态估计", "World.observe()", "blue"),
        ("任务规划与监控", "scripted_agent()", "accent"),
        ("运动与底层控制", "World.move() + 伺服", "amber"),
        ("完成条件检查", "World.success()", "accent"),
    ]
    for index, (function, code, tone) in enumerate(rows):
        y = 60 + 95 * index
        fig.box(24, y, 258, 64, function, tone=tone)
        fig.arrow((290, y + 32), (321, y + 32))
        fig.box(329, y, 287, 64, code)
        if index < len(rows) - 1:
            fig.arrow((473, y + 71), (473, y + 88))
    fig.text(320, 437, "验收未通过时，下一轮继续读新状态", 20, ACCENT, 640, "middle")
    return fig


def agent_loop():
    fig = Figure("机器人 Agent 的任务反馈循环", 296)
    fig.box(24, 23, 142, 58, "任务目标", tone="amber")
    fig.arrow((173, 52), (212, 52))
    fig.box(220, 23, 172, 58, "观察状态", tone="blue")
    fig.arrow((400, 52), (434, 52))
    fig.box(442, 23, 174, 58, "选择技能", tone="accent")
    fig.arrow((529, 89), (529, 134))
    fig.box(442, 142, 174, 58, "执行运动")
    fig.arrow((434, 171), (400, 171))
    fig.box(220, 142, 172, 58, "检查结果", tone="accent")
    fig.arrow((211, 171), (174, 171), tone="accent")
    fig.box(24, 142, 142, 58, "达标，结束", tone="accent")
    fig.arrow((305, 207), (305, 232), (194, 232), (194, 109), (305, 109), (305, 90), tone="blue")
    fig.text(320, 270, "未达标时读取新状态，再选择动作", 22, BLUE, 650, "middle")
    return fig


def first_experiment():
    fig = Figure("第一次运行仿真的读图顺序", 316)
    fig.rect(24, 22, 592, 100, "#eef2f8", "#b3c4db")
    fig.text(46, 56, "输入", color=BLUE, weight=700)
    fig.text(46, 91, "scene.xml · 固定种子 7 · 固定动作顺序", 23, BLUE)
    fig.arrow((320, 128), (320, 151))
    fig.box(24, 158, 592, 54, "MuJoCo 执行动作并更新物体状态", tone="accent")
    fig.path(((320, 218), (320, 230)))
    fig.arrow((320, 230), (164, 230), (164, 241))
    fig.arrow((320, 230), (470, 230), (470, 241))
    fig.box(24, 248, 280, 49, "过程 events.jsonl")
    fig.box(324, 248, 292, 49, "结果 summary.json")
    return fig


def observation_paths():
    fig = Figure("同一个场景的两条观测路径", 332)
    fig.box(24, 20, 592, 55, "MuJoCo 中的同一个场景", tone="accent")
    fig.arrow((168, 82), (168, 111))
    fig.arrow((472, 82), (472, 111))
    fig.box(24, 118, 288, 76, "直接读取状态", "关节、方块、目标位置", "blue")
    fig.box(328, 118, 288, 76, "相机渲染 RGB", "经颜色与标定估计位置", "amber")
    fig.arrow((168, 202), (168, 229))
    fig.arrow((472, 202), (472, 229))
    fig.box(24, 236, 288, 76, "第 3、6 章主线", "反馈控制读取坐标")
    fig.box(328, 236, 288, 76, "第 8 章独立练习", "估计与真值比较")
    return fig


def scara_geometry():
    fig = Figure("俯视 SCARA 机械臂与坐标轴", 306)
    fig.text(27, 39, "俯视图 · XY 平面", color=ACCENT, weight=720)
    fig.arrow((55, 204), (566, 204))
    fig.arrow((320, 237), (320, 68))
    fig.text(575, 211, "+x")
    fig.text(327, 66, "+y")
    fig.text(329, 232, "世界原点", 20, MUTED)
    fig.path(((89, 204), (243, 117), (389, 149)), ACCENT, 14)
    fig.dot(89, 204, 12, ACCENT, "white")
    fig.dot(243, 117, 12, ACCENT, "white")
    fig.dot(389, 149, 11, BLUE, "white")
    fig.text(100, 238, "机械臂基座", 20, MUTED)
    fig.text(143, 123, "0.35 m", 20, ACCENT, 650)
    fig.text(341, 112, "0.30 m", 20, ACCENT, 650)
    fig.text(412, 155, "末端目标", color=BLUE, weight=700)
    fig.text(320, 287, "竖直关节单独改变 z 高度，垂直于图面", 20, MUTED, 550, "middle")
    return fig


def skill_contract():
    fig = Figure("一次抓取调用的输入、条件与结果", 306)
    fig.box(24, 21, 184, 68, "请求 grasp()", "使用当前状态", "blue")
    fig.arrow((215, 55), (253, 55))
    fig.box(261, 21, 355, 68, "检查前置条件", "手空着，末端靠近方块", "amber")
    fig.arrow((390, 96), (390, 121), (169, 121), (169, 153), tone="accent")
    fig.arrow((487, 96), (487, 153), tone="red")
    fig.box(24, 160, 287, 76, "尝试抓取", "成功时启用附着约束", "accent")
    fig.box(329, 160, 287, 76, "条件不满足", "返回失败原因", "red")
    fig.text(320, 278, "返回 ok、当前观察，失败时附 error", 23, INK, 650, "middle")
    return fig


def recovery_trace():
    fig = Figure("同一次抓空后的两条执行轨迹", 330)
    fig.box(24, 22, 592, 62, "第 3 次调用抓空，holding = false", tone="red")
    fig.arrow((164, 91), (164, 115))
    fig.arrow((476, 91), (476, 115))
    fig.box(24, 122, 289, 67, "固定脚本", "第 4 次调用：抬手", "amber")
    fig.box(327, 122, 289, 67, "规则闭环", "第 4 次调用：再抓", "accent")
    fig.arrow((164, 198), (164, 225))
    fig.arrow((476, 198), (476, 225))
    fig.box(24, 232, 289, 75, "走完整个序列", "松手时夹爪仍为空", "red")
    fig.box(327, 232, 289, 75, "抓稳后继续搬运", "释放后通过验收", "accent")
    return fig


def build_figures(directory):
    directory.mkdir(parents=True, exist_ok=True)
    for draw in (policy_paths, module_map, agent_loop, first_experiment,
                 observation_paths, scara_geometry, skill_contract, recovery_trace):
        draw().write(directory / (draw.__name__.replace("_", "-") + ".svg"))
