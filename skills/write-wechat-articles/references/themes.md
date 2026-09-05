# 公众号排版主题

## 选择与应用

每篇文章只选一款主题。用户指定名称或 ID 时优先采用；否则按下表匹配文章类型，无法判断时用 `technical-blue`。主题只影响排版，不增加文章章节、装饰文案或图片。

| ID | 名称 | 适用内容 | 视觉特征 |
| --- | --- | --- | --- |
| `ink` | 极简墨色 | 原理分析、观点、长文 | 衬线标题、细底线，接近书刊阅读 |
| `technical-blue` | 技术蓝 | 技术教程、API、工具实践；默认 | 无衬线标题、蓝色左线，步骤清楚 |
| `pine` | 松针绿 | 工作流、经验整理、效率实践 | 细绿左线，正文节奏舒展 |
| `sand` | 暖砂棕 | 创作手记、案例、音乐与影像实践 | 衬线标题、暖棕底线，留白稍宽 |
| `vermilion` | 朱砂红 | 故障复盘、避坑、限制与取舍 | 较粗红色左线，结构紧凑 |
| `iris` | 鸢尾紫 | AI 创作、提示词分享、工具评测 | 无衬线标题、紫色细底线，无光效或渐变 |

下表是主题参数的唯一来源；不要在其他文件另存一份色板。将参数替换成实际行内 CSS，不在文章片段中保留变量、模板标记或依赖类名。预览页不另行换主题，修改主题时重新生成同源的 `wechat.md` 与 `wechat.html`。

| ID | `ACCENT` | `RADIUS` | `LINE_HEIGHT` | `PARAGRAPH_GAP` | `HEADING_FONT` | `H2_STYLE` |
| --- | --- | --- | --- | --- | --- | --- |
| `ink` | `#7b7f86` | `2px` | `1.9` | `18px` | serif | `padding:0 0 10px !important;border-bottom:1px solid #7b7f86 !important;` |
| `technical-blue` | `#477ead` | `6px` | `1.85` | `16px` | sans | `padding:0 0 0 11px !important;border-left:3px solid #477ead !important;` |
| `pine` | `#428579` | `6px` | `1.9` | `18px` | sans | `padding:0 0 0 12px !important;border-left:2px solid #428579 !important;` |
| `sand` | `#9a794b` | `4px` | `1.95` | `20px` | serif | `padding:0 0 10px !important;border-bottom:2px solid #9a794b !important;` |
| `vermilion` | `#b66b63` | `4px` | `1.85` | `16px` | sans | `padding:0 0 0 10px !important;border-left:4px solid #b66b63 !important;` |
| `iris` | `#8874ad` | `6px` | `1.9` | `18px` | sans | `padding:0 0 10px !important;border-bottom:1px solid #8874ad !important;` |

字体参数展开为：

- `sans`：`-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',Arial,sans-serif`
- `serif`：`'Songti SC','Noto Serif CJK SC','Source Han Serif SC',SimSun,serif`，只用于文章标题。字体不存在时使用系统回退，不加载网络字体。

统一的正文基线：16px、左对齐、不首行缩进；主标题 24px，二级标题 19px，三级标题 17px。正文行高和段后距按主题取值，代码统一 13px / 1.7。`RADIUS` 仅用于图片占位等非代码封闭容器。代码块和提示词块独立使用 2px 圆角，允许更小但不得超过 2px；标题边线和引用左线保持直角。

## 同一主题兼容两种阅读环境

- 文章根节点不设置固定文字色或整页底色。正文、标题、序号、加粗、引用、列表、图注、表格和链接使用 `color:inherit !important;background:transparent !important;`，让阅读环境提供基础文字与背景配对。
- `ACCENT` 只用于标题边线、引用边线和表格分隔等装饰；链接用继承文字色和下划线，重要性用粗细、字号和文字表达。不要把主题强调色当作正文、浅灰图注或白字标签色。
- 不依赖微信执行 JavaScript、媒体查询、CSS 变量或 `color-scheme` 来切换已发布正文；这些能力只用于独立预览页外壳。
- 不通过滤镜、混合模式、透明文字、背景图锁色等方式强行阻止客户端处理颜色。
- 代码块使用 [wechat-formatting.md](wechat-formatting.md) 中统一的深色底与高对比文字配对，语法高亮与代码圆角不随主题更换，所有主题的代码圆角上限均为 2px。

这是以阅读环境为基础的兼容策略，不是对微信所有版本的保证。本技能不假设公众号图文存在稳定可依赖的暗色转换规则；客户端改色、编辑器过滤和粘贴行为须在目标版本验证。不能把浏览器深色预览描述为微信算法复刻。

## 验证口径

浏览器先检查浅色纸面 `#ffffff` / 文字 `#1f2329` 和深色纸面 `#191919` / 文字 `#e6e6e6`，这两组仅属于预览环境，不写入导出正文。正文、链接、图注及代码注释的目标对比度至少为 4.5:1；装饰色不承担文字信息。对比度计算依据 [W3C 对比度要求](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)，不等同于发布后测量结果。

发布前在微信编辑器粘贴后预览：分别检查手机浅色和深色模式的标题、正文、引用、链接、表格、图片占位及代码底色与文字；左右滑动最长代码行直到末尾，确认能读全且页面不横移。记录实际检查的平台、微信版本和结果；没有真机条件时标记“微信真机待验证”，不补写通过结论。

若真机改色导致语法高亮不可读，先移除高亮，保留统一代码文字色与底色；仍不清楚时，将代码改为继承文字色、透明背景及细边框，继续保留不换行和块内滚动。若编辑器删除滚动属性，修复后重试；无法保留时明确报告不满足横向滚动要求，提供 HTML 源码和原始代码，不能以截断、缩小字体或折行冒充修复。

## 使用示例

- “用松针绿排版这篇工作流文章。”
- “这次用极简墨色，正文内容保持不变。”
- “生成一篇 API 教程。”：自动使用技术蓝并完成同源 HTML 交付。
