# 微信公众号交付与排版

## 内容节奏

- 开头尽快说明问题、结论或实际收益。
- 每段只表达一个重点，优先使用短段落。
- 标题层级少而清楚，一般不超过三级。
- 列表用于并列信息，不把连续正文强行拆成列表。
- 谨慎加粗，只突出读者必须看到的结论或限制。
- 不用装饰性符号、连续分隔线或空泛金句制造节奏。
- 代码示例保持完整，但删除无关样板代码和超长输出。

## 设计原则

以下原则内置生效，无需额外调用设计技能。

### 主题与颜色

- 按 [themes.md](themes.md) 选择 6 款预设之一，统一应用其边线、字体、间距与圆角参数。
- 正文和所有非代码组件继承阅读环境文字色、使用透明背景。主题色只用于边线，链接保留下划线。
- 不增加渐变、阴影、大面积色块、装饰圆点或第二个强调色。代码语法高亮是独立的语义配色，不用于正文装饰。
- 深浅色检查与导出配色分离：预览环境可切换，复制出的文章片段保持相同。

### 排版与文案

- 标题用字号、粗细和主题边线区分层级；不靠装饰标签、大段留白或无关序号制造节奏。
- 表格只用于结构化对比，超过 5 行时优先拆分；宽表格改为列表，不能撑宽页面。
- 不使用 AI 紫色光效、虚假界面截图或装饰性渐变。鸢尾紫仅使用克制的纯色边线。
- 完稿后逐句重读标题、正文、代码注释、图片说明和互动语。
- 按 [natural-writing.md](natural-writing.md) 检查文风，重写“彻底讲透、赋能、颠覆、一站式、无缝衔接”等缺少具体信息的套话；不机械替换术语、引文、代码或提示词中的词语。
- 默认减少装饰性破折号，优先使用逗号、句号或括号；作者样稿中有明确用途的标点可保留，代码与引文标点不因文风润色而改动。
- 数字必须有依据，不编造精确到小数点的虚假指标。

## 默认输出结构

### 标题候选

提供 3 个准确兑现正文的标题。不使用悬念欺骗、夸张数字或“彻底讲透”等表达。

### 公众号摘要

控制在 60-100 字，直接说明文章解决的问题和读者收益。

### Markdown 原稿

直接保存为标准 Markdown，不在文件最外层增加代码围栏。保留文章内部的代码块、链接、引用和图片占位。

### 公众号 HTML 源码

`wechat.md` 只包含一句简短说明和一个完整的 `html` 代码块。代码块内保存文章 HTML 片段，不包含预览页外壳、按钮或脚本。Markdown 预览器通常会为代码块提供复制按钮，方便保存或修改源码。

文章正文的 CSS 全部写入元素的 `style` 属性。不要依赖外部样式表、外部字体、类名、CSS 变量、伪元素、动画、悬停状态或媒体查询。

复制代码块得到的是 HTML 源码文本。需要直接粘贴到微信公众号编辑器时，应打开同时生成的 `wechat.html`，点击“复制到公众号”。

### 公众号富文本预览

`wechat.html` 使用 [../assets/wechat-preview-template.html](../assets/wechat-preview-template.html) 作为页面外壳。将模板中的 `{{ARTICLE_HTML}}` 完整替换为文章 HTML 片段，不保留模板占位符。

预览页必须：

- 单文件运行，不依赖网络资源。
- 只复制 `#wechat-article` 的正文内容（不含 `<h1>` 标题），不复制按钮、说明、状态或页面背景。
- 优先写入 `text/html` 与 `text/plain`。
- 富文本剪贴板接口不可用时，使用同一文章克隆尝试兼容复制。
- 兼容复制失败时显示不含标题的正文副本并保留选中状态，提示用户手动复制；副本保持可见，直到用户关闭或再次复制。
- 与 `wechat.md` 使用完全相同的文章片段。
- 提供“跟随系统 / 浅色 / 深色”阅读环境切换，仅改变预览外壳的文字和背景，不修改文章节点的行内样式。
- 明示“预览检查不等于微信真机效果”；外壳样式不能替文章补上缺失的宽度或滚动规则。

### 配图清单

仅在正文确实需要图片时输出。每张图片包含：

- 编号
- 插入位置
- 用途
- 素材类型
- 建议尺寸或比例
- 图片说明
- 可选的图片生成提示词

正文占位格式：

```text
【配图 01｜用途｜建议比例｜替换为公众号素材库图片】
```

`article.md`、`wechat.md`、`wechat.html` 和 `assets.md` 使用相同编号与位置。没有必要配图时，省略占位和清单。

### 封面图提示词

提供 1 条简洁提示词。画面应与文章主题直接相关，采用克制的技术编辑视觉，避免通用 AI 紫色光效、虚假界面和无意义装饰。封面比例为 **2.35:1**（公众号默认封面比例），生成图片时使用此比例。

### 文末互动语

可选。确有具体讨论点或用户要求互动时，最多问 1 个与正文直接相关的问题；否则自然结束。不以“你怎么看”凑结尾，不要求点赞、在看或转发。

## 自动保存

文章通过质量检查后，保存到执行任务时的当前工作区：

```text
微信公众号文章/
└── YYYY-MM-DD-短标题/
    ├── article.md
    ├── wechat.md
    ├── wechat.html
    └── assets.md
```

按以下规则写入：

- `article.md`：标题候选、公众号摘要、Markdown 正文和参考资料。
- `wechat.md`：简短说明和一个包含完整文章片段的 `html` 代码块。
- `wechat.html`：可独立打开的排版预览页和富文本复制按钮。
- `assets.md`：封面图提示词、正文配图清单和素材库替换说明。没有正文配图时，仍写入封面图提示词，并注明正文无需配图。

从最终推荐标题提取短标题。删除 `\ / : * ? " < > |` 等不安全字符，将连续空格替换为连字符，截取前 40 个字符。清理后为空时使用 `未命名文章`。

目标目录已存在时，依次追加 `-2`、`-3` 等后缀，禁止覆盖已有文件。

保存成功后，对话只返回：

1. 一段简短摘要
2. `article.md`、`wechat.md`、`wechat.html` 和 `assets.md` 的可点击链接
3. 已完成的校验项目

当前工作区不可写时，不写入 Skill 安装目录。此时在对话中输出完整交付内容，并说明保存失败原因。

用户指定保存路径、文件名或仅需部分交付内容时，以用户要求为准。

## 提示词排版

- 将完整提示词放在一个代码块中，方便复制。
- 用方括号标出可替换变量。
- 在代码块前标明适用工具、模型和测试状态。
- 代码块后只解释关键变量和限制。

## 文章 HTML 样式

组件中的 `{{ACCENT}}`、`{{RADIUS}}`、`{{LINE_HEIGHT}}`、`{{PARAGRAPH_GAP}}`、`{{HEADING_FONT}}` 和 `{{H2_STYLE}}` 从 [themes.md](themes.md) 展开。所有模板标记须在生成文章片段时替换完毕；预览外壳只接收最终的 `{{ARTICLE_HTML}}`。

### 容器与文字

根节点使用以下结构，示例内容替换为正文：

```html
<section id="wechat-article" style="box-sizing:border-box !important;display:block !important;width:100% !important;min-width:0 !important;max-width:677px !important;margin:0 auto !important;padding:4px 4px 32px !important;border:0 !important;background:transparent !important;color:inherit !important;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',Arial,sans-serif !important;font-size:16px !important;line-height:{{LINE_HEIGHT}} !important;word-break:normal !important;overflow-wrap:anywhere !important;">
  <!-- 文章内容 -->
</section>
```

- 各正文组件显式设置必要的字号、行高、间距、背景和 `color:inherit`；关键布局声明使用行内 `!important`。这是减少编辑器默认样式影响的措施，不能阻止平台过滤或保证暗色转换行为。
- 主标题 24px / 1.4、700 字重，使用主题标题字体；二级标题 19px / 1.5、700 字重；三级标题 17px / 1.6、700 字重。步骤文章可用 `1.`、`1.1.` 编号，其他文章不强制编号。
- 普通段落、列表、引用、图注、链接和表格均不设置固定文字色。链接额外写 `color:inherit !important;text-decoration:underline !important;`。
- 图片宽度不超过容器，使用 `max-width:100% !important;height:auto !important;`；图片占位不用假截图。
- 表格使用 `width:100%;table-layout:fixed` 和可断行的单元格。不能以页面级 `overflow-x:hidden` 掩盖溢出。
- 行内短代码使用等宽字体、继承文字色及透明背景，允许自然断行；很长的命令移入独立代码块。下述不换行规则针对代码块和提示词块。

### 常用组件

```html
<p style="box-sizing:border-box !important;display:block !important;margin:0 0 {{PARAGRAPH_GAP}} !important;padding:0 !important;border:0 !important;background:transparent !important;color:inherit !important;font-size:16px !important;line-height:{{LINE_HEIGHT}} !important;font-weight:400 !important;text-align:left !important;">正文段落</p>

<h2 style="box-sizing:border-box !important;display:block !important;margin:28px 0 14px !important;border:0 !important;{{H2_STYLE}}background:transparent !important;color:inherit !important;font-family:{{HEADING_FONT}} !important;font-size:19px !important;line-height:1.5 !important;font-weight:700 !important;text-align:left !important;">二级标题</h2>

<h3 style="box-sizing:border-box !important;display:block !important;margin:22px 0 12px !important;padding:0 !important;border:0 !important;background:transparent !important;color:inherit !important;font-family:{{HEADING_FONT}} !important;font-size:17px !important;line-height:1.6 !important;font-weight:700 !important;text-align:left !important;">三级标题</h3>

<section style="box-sizing:border-box !important;display:block !important;width:100% !important;min-width:0 !important;max-width:100% !important;margin:18px 0 !important;padding:10px 14px !important;border:0 !important;border-left:2px solid {{ACCENT}} !important;background:transparent !important;color:inherit !important;">
  <p style="margin:0 !important;background:transparent !important;color:inherit !important;font-size:15px !important;line-height:1.8 !important;"><strong style="color:inherit !important;font-weight:700 !important;">关键点：</strong>提示内容</p>
</section>

<section data-image-slot="01" style="box-sizing:border-box !important;display:block !important;width:100% !important;max-width:100% !important;margin:20px 0 8px !important;padding:28px 16px !important;border:1px solid {{ACCENT}} !important;border-radius:{{RADIUS}} !important;background:transparent !important;color:inherit !important;text-align:center !important;">
  <p style="margin:0 !important;background:transparent !important;color:inherit !important;font-size:14px !important;line-height:1.7 !important;">【配图 01｜用途｜建议比例｜替换为公众号素材库图片】</p>
</section>

<table style="box-sizing:border-box !important;display:table !important;width:100% !important;max-width:100% !important;table-layout:fixed !important;margin:18px 0 !important;border-collapse:collapse !important;border-spacing:0 !important;background:transparent !important;color:inherit !important;font-size:15px !important;line-height:1.7 !important;overflow-wrap:anywhere !important;">
  <thead><tr>
    <th style="padding:10px !important;border-bottom:2px solid {{ACCENT}} !important;background:transparent !important;color:inherit !important;font-weight:700 !important;text-align:left !important;">条件</th>
    <th style="padding:10px !important;border-bottom:2px solid {{ACCENT}} !important;background:transparent !important;color:inherit !important;font-weight:700 !important;text-align:left !important;">结果</th>
  </tr></thead>
  <tbody><tr>
    <td style="padding:10px !important;border-bottom:1px solid {{ACCENT}} !important;background:transparent !important;color:inherit !important;">单元格</td>
    <td style="padding:10px !important;border-bottom:1px solid {{ACCENT}} !important;background:transparent !important;color:inherit !important;">单元格</td>
  </tr></tbody>
</table>
```

### 代码块与提示词块

以下组件是所有主题的共同约束，适用于单行命令、多行代码和完整提示词。代码块圆角默认 2px，上限 2px，不使用主题的 `RADIUS` 参数；内层代码元素保持直角：

```html
<pre tabindex="0" aria-label="代码块，可横向滚动" style="box-sizing:border-box !important;display:block !important;width:100% !important;min-width:0 !important;max-width:100% !important;margin:18px 0 !important;padding:16px !important;border:1px solid #74808c !important;border-radius:2px !important;background:#202630 !important;color:#e6edf3 !important;font-family:Consolas,Monaco,'Liberation Mono',Menlo,monospace !important;font-size:13px !important;line-height:1.7 !important;font-weight:400 !important;text-align:left !important;white-space:pre !important;word-break:normal !important;overflow-wrap:normal !important;word-wrap:normal !important;hyphens:none !important;overflow-x:auto !important;overflow-y:hidden !important;tab-size:4 !important;-webkit-overflow-scrolling:touch;"><code style="display:block !important;width:max-content !important;min-width:100% !important;margin:0 !important;padding:0 !important;border:0 !important;border-radius:0 !important;background:transparent !important;color:#e6edf3 !important;font-family:Consolas,Monaco,'Liberation Mono',Menlo,monospace !important;font-size:13px !important;line-height:1.7 !important;font-weight:400 !important;text-align:left !important;white-space:pre !important;word-break:normal !important;overflow-wrap:normal !important;word-wrap:normal !important;hyphens:none !important;tab-size:4 !important;">已转义的代码或提示词</code></pre>
```

- `<pre>` 是唯一横向滚动容器，宽度始终受文章约束；内层 `<code>` 可按内容伸展。不在内层再设置滚动条，也不把正文包进 flex/grid。若外层确实使用 flex/grid，对包含代码块的项目设置 `min-width:0`。
- `white-space:pre` 保留原始换行和空格且不自动折行；同时在 `pre`、`code` 及高亮 `span` 上禁止单词断行。不能用 `pre-wrap`、`break-all`、`overflow-wrap:anywhere` 或 `nowrap` 替代代码块规则。
- 不向单行插入换行、`<br>`、`<wbr>`、软连字符或零宽空格。不为排版缩短命令、截断内容、使用省略号或缩小字体。
- 多行输入保留原始行数、空行及缩进；不是把整个代码块压成一行。不要为了美化 HTML 源码在 `<code>` 标签与实际代码之间添加缩进或空行。
- 不设置固定高度、最大高度、行数限制或内层隐藏溢出。长行可横向读到结尾，多行在垂直方向完整展示。
- 默认不带红黄绿窗口圆点、阴影或独立工具栏。高亮只使用合法闭合的行内 `span`，不允许把代码放进图标或装饰节点。
- 使用 HTML 转义函数对代码及提示词的 `&`、`<`、`>` 转义一次；序列化后的 DOM 文本应与原文一致，不做二次转义。文末互动语也保持与 Markdown 原稿一致。

### 可选语法高亮

深色代码底固定为 `#202630`。共享配色如下，注释也必须清晰，不用低对比灰色或低透明度：

| 语义 | 颜色 |
| --- | --- |
| 普通代码 | `#e6edf3` |
| 注释 | `#aab6c5` |
| 关键字、函数 | `#d8c5fa` |
| 字符串 | `#b5d99c` |
| 数字、常量 | `#f2c38b` |
| 命令、操作符 | `#9ddce2` |

示例：`<span style="color:#aab6c5 !important;font-style:normal !important;white-space:pre !important;word-break:normal !important;overflow-wrap:normal !important;">注释文字</span>`。不确定语言或分词边界时使用纯文本，不能为高亮改变代码。真机改色后的回退见 [themes.md](themes.md)。

### 浏览器验收与平台边界

- 每款主题检查 320px、375px 和 768px 宽度下的浅色与深色预览；页面及文章不能出现横向滚动。
- 测试至少包含一行很长的命令、一行中英文混排提示词、带空行和缩进的多行代码、长链接、引用和表格。
- 长行应满足 `pre.scrollWidth > pre.clientWidth`，且能够滚到末尾；短单行只占一行，多行保持输入行数。移除预览外壳样式后再次检查，确认滚动依赖文章行内 CSS。
- 复制与环境切换不能改变源文章 HTML。检查现代剪贴板、兼容复制、手动复制三条路径，都只包含不带 `h1` 的正文，不夹带预览主题配色或工具栏。
- 微信编辑器粘贴与手机实测单独记录。未执行时说明“浏览器已检查，微信真机待验证”，不能将模拟结果当作发布保证。

实现依据：[MDN white-space](https://developer.mozilla.org/en-US/docs/Web/CSS/white-space)、[MDN overflow-x](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-x)、[W3C G148 阅读环境配色策略](https://www.w3.org/WAI/WCAG22/Techniques/general/G148)。这些资料说明浏览器行为和可访问性原则，不证明微信公众号对每项 CSS 的支持。

## 图片规则

- 用户提供图片时，优先使用并给出裁剪、排序和说明建议。
- 技术截图、效果对比和生成结果必须是真实素材。
- AI 图片只作为封面或装饰插图。
- 不为丰富版面堆图。
