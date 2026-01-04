# Hugo Blowfish 主题侧边栏(TOC)不显示问题 - 注意事项

## 问题描述

在使用 Hugo Blowfish 主题时，GSpawn 页面的侧边栏目录(Table of Contents)不显示，而 Animancer 页面可以正常显示。

## 根本原因

### 原因 1: 标题级别不正确

**问题:**
- Markdown 文件中使用了一级标题 `#` 作为内容标题
- Hugo 的 TOC 生成器**默认不包含一级标题(H1)**，只显示二级及以上标题(`##`, `###`, `####`)

**错误示例:**
```markdown
---
title: "文档标题"
showTableOfContents: true
---

# 第一章
内容...

# 第二章
内容...
```

**正确示例:**
```markdown
---
title: "文档标题"
showTableOfContents: true
---

## 第一章
内容...

## 第二章
内容...
```

**原因说明:**
- 一级标题 `#` 在语义上代表页面主标题，通常对应 front matter 中的 `title`
- TOC 目录从二级标题 `##` 开始，用于展示文档的章节结构

---

### 原因 2: 布局类型选择错误

**问题:**
- 使用了 `layout: "list"` 或 `layout: "simple"` 布局
- 这些布局**不支持显示侧边栏 TOC**

**Blowfish 主题布局对比:**

| 布局类型 | 是否支持 TOC | 适用场景 | 说明 |
|---------|-------------|---------|------|
| `list` | ❌ | 列表页面 | 用于显示子页面列表，如博客文章列表 |
| `simple` | ❌ | 简单页面 | 简洁布局，无侧边栏 |
| `single` | ✅ | 单篇文章/文档 | **完整文章布局，支持 TOC 侧边栏** |

**错误配置:**
```yaml
---
title: "文档标题"
layout: "list"                # ❌ 不支持 TOC
showTableOfContents: true
---
```

**正确配置:**
```yaml
---
title: "文档标题"
layout: "single"              # ✅ 支持 TOC
showTableOfContents: true
---
```

---

## 完整解决方案

### 步骤 1: 修复标题级别

使用以下命令批量替换一级标题为二级标题:

```bash
# 从第14行开始(跳过 front matter)，将单个 # 替换为 ##
sed -i '14,$s/^# \([^#=]\)/## \1/' "文件路径/index.md"
```

**正则说明:**
- `^# ` - 匹配行首的单个 `#` 加空格
- `\([^#=]\)` - 捕获后面的字符(不是 `#` 或 `=`，避免误替换注释)
- `## \1` - 替换为 `##` 加原字符

### 步骤 2: 修改布局配置

**修改前:**
```yaml
---
title: "Gspawn 中文文档目录"
date: 2025-12-25
draft: false

layout: "list"                # ❌ 错误
showSimpleListing: true       # list 布局专用，single 不需要
showPagination: true          # list 布局专用，single 不需要
showTableOfContents: true
---
```

**修改后:**
```yaml
---
title: "Gspawn 中文文档目录"
date: 2025-12-25
draft: false

layout: "single"              # ✅ 正确
showTableOfContents: true
---
```

### 步骤 3: 重新构建

```bash
cd "项目根目录"
hugo
```

### 步骤 4: 验证 TOC 生成

```bash
# 检查生成的 HTML 中是否包含 TOC 元素
grep -i "class=\"toc" public/gspawn/index.html
```

期望输出:
```html
<div class="toc ps-5 print:hidden lg:sticky lg:top-10">
```

---

## 关键知识点总结

### 1. Markdown 标题层级语义

```markdown
# H1 - 页面主标题（通常只有一个，对应 front matter 的 title）
## H2 - 章节标题（TOC 从这里开始）
### H3 - 小节标题
#### H4 - 子小节标题
```

### 2. Hugo TOC 配置

在 `hugo.toml` 中可以配置 TOC 的标题层级范围:

```toml
[markup]
  [markup.tableOfContents]
    startLevel = 2  # 从 H2 开始
    endLevel = 4    # 到 H4 结束
    ordered = false # 使用无序列表
```

### 3. Blowfish 主题 TOC 显示条件

必须**同时满足**以下条件:

1. ✅ 使用 `layout: "single"` 布局
2. ✅ 设置 `showTableOfContents: true`
3. ✅ 文档中有 `##` (H2) 或更高级别的标题
4. ✅ 在大屏幕设备上查看 (TOC 在移动端会收起)

---

## 类比理解

### 类比 1: 书籍结构

```
书名（H1，只有一个）
├── 第一章（H2）← TOC 从这里开始
│   ├── 1.1 节（H3）
│   └── 1.2 节（H3）
├── 第二章（H2）
│   ├── 2.1 节（H3）
│   └── 2.2 节（H3）
└── 第三章（H2）
```

TOC 不会显示"书名"，只显示章节目录。

### 类比 2: 网站页面类型

| 布局 | 对应网站 | 特点 |
|-----|---------|------|
| `list` | 博客首页 | 显示文章列表，没有具体内容 |
| `simple` | 关于页面 | 简单信息展示，无需目录 |
| `single` | 技术文档 | 长篇内容，需要目录导航 |

---

## 检查清单

在创建新的长文档页面时，请检查:

- [ ] Front Matter 中使用 `layout: "single"`
- [ ] 设置 `showTableOfContents: true`
- [ ] 正文使用 `##` 或 `###` 标题（不是单个 `#`）
- [ ] Front Matter 中的 `title` 对应页面主标题
- [ ] 删除 `showPagination` 和 `showSimpleListing` 等 list 布局专用配置

---

## 快速修复脚本

如果遇到类似问题，可以使用以下脚本快速修复:

```bash
#!/bin/bash
# 修复 Hugo 文档 TOC 不显示问题

FILE="$1"

# 1. 替换一级标题为二级标题
sed -i '14,$s/^# \([^#=]\)/## \1/' "$FILE"

# 2. 修改布局为 single
sed -i 's/layout: "list"/layout: "single"/' "$FILE"
sed -i 's/layout: "simple"/layout: "single"/' "$FILE"

# 3. 删除不需要的配置
sed -i '/showSimpleListing:/d' "$FILE"
sed -i '/showPagination:/d' "$FILE"

echo "✅ 修复完成！请运行 hugo 重新构建网站"
```

使用方法:
```bash
chmod +x fix-toc.sh
./fix-toc.sh "content/GSpawn/index.md"
```

---

## 参考资源

- [Hugo Table of Contents 官方文档](https://gohugo.io/content-management/toc/)
- [Blowfish 主题文档 - 布局类型](https://blowfish.page/docs/content-examples/)
- [Markdown 标题层级最佳实践](https://www.markdownguide.org/basic-syntax/#headings)

---

**创建日期**: 2026-01-04
**问题类型**: Hugo Blowfish 主题配置
**关键词**: TOC, 侧边栏, 标题层级, 布局类型
