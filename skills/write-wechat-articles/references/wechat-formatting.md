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

### 色彩一致性

- 全文锁定一个强调色 `#246ba5`，标题左边线、序号、链接、表头底边线统一使用。
- 不引入渐变、阴影、大面积色块或第二个强调色。
- 正文不设显式文字颜色，由微信主题自动适配深浅模式。

### 圆角一致性

- 全文统一使用 `6px` 圆角（代码块、图片占位、表格等），不混用不同圆角值。

### 排版反默认

- 不使用 AI 紫色光效、虚假界面截图或装饰性渐变。
- 不使用装饰性圆点、版本标签、序号前缀（标题序号除外）或滚动提示。
- 表格只用于真正的结构化对比，不用表格撑版面；超过 5 行的数据考虑拆分或改用列表。
- 标题用字号和粗细区分层级，不靠装饰元素或大段留白制造节奏。

### 文案自检

- 完稿后逐句重读所有可见文字（标题、正文、代码注释、图片说明、互动语）。
- 删除填充动词：彻底讲透、赋能、颠覆、一站式、无缝衔接。
- 不使用破折号（—）作为装饰或分隔，用逗号、句号或括号替代。
- 数字必须有依据，不编造精确到小数点的虚假指标。

### 深色主题兼容

- 代码块保留固定深色背景（`#172331`），两种主题下都可读。
- 提示框、图片占位、表格等非代码组件不设背景色，仅用边框区分。
- 正文不设显式文字颜色，交由微信主题反转；标题颜色使用深色系（`#173b5d`），深色主题下仍可辨。

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
- 富文本剪贴板接口不可用时，选中正文并尝试兼容复制。
- 兼容复制失败时保留选中状态，提示用户手动复制。
- 与 `wechat.md` 使用完全相同的文章片段。

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

只问 1 个与文章内容直接相关的问题。不要求点赞、在看或转发。

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

默认采用冷静、克制的技术编辑风。根节点使用：

```html
<section id="wechat-article" style="box-sizing:border-box !important;display:block !important;margin:0 auto !important;padding:4px 4px 32px !important;max-width:677px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Hiragino Sans GB','Microsoft YaHei',Arial,sans-serif !important;font-size:16px !important;line-height:1.85 !important;word-break:break-word;border:0 !important;background:transparent !important;">
  <!-- 文章内容 -->
</section>
```

按以下规则排版：

- 正文使用 `16px`、`1.85` 行高和 `#29323d`，段落下边距一般为 `16px`。
- 主标题使用 `24px` 左右的深色粗体，标题下方只保留必要的栏目和日期信息。
- 标题层级使用有序列表风格：二级标题使用 `1.`、`2.` 等序号，三级标题使用 `1.1.`、`1.2.` 等序号。
- 二级标题使用 `19px` 左右的粗体和深蓝左边线；三级标题使用 `17px` 粗体。
- 深蓝强调色使用 `#246ba5`，不要增加渐变、阴影或大面积色块。
- 提示框使用 `#7fa8c7` 左边线，不设背景色（深色主题兼容）。
- 代码块使用 macOS 风格：深灰背景 `#282c34`、圆角 6px、带阴影、顶部显示红黄绿窗口控件圆点；代码文字 `#abb2bf`，注释建议用 `<em>` 包裹设为 `#5c6370` 斜体，内置函数用 `#e6c07b`；长行水平滚动不换行。
- 图片占位使用细边框和明确编号，不使用虚假图片。
- 链接使用深蓝色和下划线；参考资料保持简短。
- 表格使用边框分隔行，不使用单元格背景色，表头加粗即可。
- 深色主题兼容：提示框、图片占位等非代码组件不设背景色，仅用边框区分；正文文字颜色由微信主题自动反转，不要手动设浅色文字。
- 所有正文组件都写入必要的行内样式，不依赖根节点继承关键尺寸或颜色，避免粘贴时部分外层样式丢失。
- **对抗编辑器覆盖：** 所有组件的关键属性（box-sizing、display、margin、padding、border、border-radius、background、color、font-family、font-size、font-weight、line-height、text-align、white-space、overflow、border-collapse）都显式声明并加 `!important`；不允许用继承或省略方式依赖默认值，否则会被公众号编辑器注入的默认样式覆盖。

代码与提示词中的 `&`、`<`、`>` 必须分别转义为 `&amp;`、`&lt;`、`&gt;`。不要转义普通中文正文。

文末互动问题放在文章 HTML 片段内，并保持与 Markdown 原稿一致。

优先复用以下组件，只替换文字内容：

```html
<p style="box-sizing:border-box !important;display:block !important;margin:0 0 16px !important;padding:0 !important;border:0 !important;background:transparent !important;font-size:16px !important;line-height:1.85 !important;font-weight:400 !important;text-align:left !important;">正文段落</p>

<h2 style="box-sizing:border-box !important;display:block !important;margin:26px 0 14px !important;padding:0 0 0 11px !important;border:0 !important;border-left:3px solid #246ba5 !important;background:transparent !important;color:#173b5d !important;font-size:19px !important;line-height:1.5 !important;font-weight:750 !important;text-align:left !important;"><span style="color:#246ba5 !important;margin-right:6px !important;font-weight:750 !important;">1.</span>二级标题</h2>

<h3 style="box-sizing:border-box !important;display:block !important;margin:20px 0 12px !important;padding:0 0 0 11px !important;border:0 !important;border-left:2px solid #7fa8c7 !important;background:transparent !important;color:#173b5d !important;font-size:17px !important;line-height:1.5 !important;font-weight:750 !important;text-align:left !important;"><span style="color:#7fa8c7 !important;margin-right:6px !important;font-weight:750 !important;">1.1.</span>三级标题</h3>

<section style="box-sizing:border-box !important;display:block !important;margin:18px 0 !important;padding:13px 15px !important;border:0 !important;border-left:3px solid #7fa8c7 !important;background:transparent !important;border-radius:0 !important;">
  <p style="box-sizing:border-box !important;display:block !important;margin:0 !important;padding:0 !important;border:0 !important;font-size:15px !important;line-height:1.8 !important;font-weight:400 !important;text-align:left !important;"><strong style="font-weight:750 !important;">关键点：</strong>提示内容</p>
</section>

<pre style="box-sizing:border-box !important;display:block !important;position:relative !important;margin:18px 0 !important;padding:1px 0 0 0 !important;border:0 !important;border-radius:6px !important;background:#282c34 !important;box-shadow:0 2px 10px rgba(0,0,0,0.35) !important;font-family:Consolas,Monaco,'Liberation Mono',Menlo,monospace !important;font-size:13px !important;line-height:1.7 !important;font-weight:400 !important;text-align:left !important;white-space:pre !important;word-break:normal !important;overflow-x:auto !important;"><span style="display:block !important;position:relative !important;margin:12px 0 0 12px !important;padding:0 !important;border-radius:50% !important;background:#ff5f56 !important;width:10px !important;height:10px !important;box-shadow:18px 0 0 #ffbd2e,36px 0 0 #27c93f !important;"><code style="display:block !important;margin:0 !important;padding:16px 14px !important;background:#282c34 !important;color:#abb2bf !important;font-family:Consolas,Monaco,'Liberation Mono',Menlo,monospace !important;font-size:13px !important;line-height:1.7 !important;font-weight:400 !important;text-align:left !important;white-space:pre !important;word-break:normal !important;overflow-x:auto !important;tab-size:4 !important;white-space:pre !important;">已转义的代码或提示词</code></pre>

<section data-image-slot="01" style="box-sizing:border-box !important;display:block !important;margin:20px 0 8px !important;padding:34px 18px !important;border:1px solid #cddbe7 !important;border-radius:6px !important;background:transparent !important;text-align:center !important;">
  <p style="box-sizing:border-box !important;display:block !important;margin:0 !important;padding:0 !important;border:0 !important;font-size:13px !important;line-height:1.7 !important;font-weight:400 !important;text-align:center !important;">【配图 01｜用途｜建议比例｜替换为公众号素材库图片】</p>
</section>

<table style="box-sizing:border-box !important;display:table !important;width:100% !important;margin:18px 0 !important;padding:0 !important;border-collapse:collapse !important;font-size:15px !important;line-height:1.7 !important;border-spacing:0 !important;border:0 !important;background:transparent !important;">
  <thead style="display:table-header-group !important;">
    <tr style="display:table-row !important;">
      <th style="box-sizing:border-box !important;display:table-cell !important;padding:10px 12px !important;border:0 !important;border-bottom:2px solid #246ba5 !important;background:transparent !important;font-size:inherit !important;line-height:inherit !important;font-weight:750 !important;text-align:left !important;">列标题</th>
      <th style="box-sizing:border-box !important;display:table-cell !important;padding:10px 12px !important;border:0 !important;border-bottom:2px solid #246ba5 !important;background:transparent !important;font-size:inherit !important;line-height:inherit !important;font-weight:750 !important;text-align:left !important;">列标题</th>
    </tr>
  </thead>
  <tbody style="display:table-row-group !important;">
    <tr style="display:table-row !important;">
      <td style="box-sizing:border-box !important;display:table-cell !important;padding:10px 12px !important;border:0 !important;border-bottom:1px solid #dce3eb !important;background:transparent !important;font-size:inherit !important;line-height:inherit !important;font-weight:400 !important;text-align:left !important;">单元格</td>
      <td style="box-sizing:border-box !important;display:table-cell !important;padding:10px 12px !important;border:0 !important;border-bottom:1px solid #dce3eb !important;background:transparent !important;font-size:inherit !important;line-height:inherit !important;font-weight:400 !important;text-align:left !important;">单元格</td>
    </tr>
  </tbody>
</table>
```

### 代码块语法高亮写法

代码块内的语义元素用 `<span>` 包裹以实现语法高亮，推荐使用以下映射：

| 语义 | 写法 | 效果 |
|------|------|------|
| 注释 | `<span style="color:#5c6370;font-style:italic;">注释文字</span>` | 灰色斜体 |
| 内置函数/关键字 | `<span style="color:#e6c07b;">函数名</span>` | 橙色 |
| 字符串 | `<span style="color:#98c379;">"字符串"</span>` | 绿色 |
| 数字/常量 | `<span style="color:#d19a66;">42</span>` | 橙色 |
| 命令/操作符 | `<span style="color:#56b6c2;">\|\|\|&&\|\-></span>` | 青色 |

无需高亮的代码直接写纯文本即可。

## 图片规则

- 用户提供图片时，优先使用并给出裁剪、排序和说明建议。
- 技术截图、效果对比和生成结果必须是真实素材。
- AI 图片只作为封面或装饰插图。
- 不为丰富版面堆图。
