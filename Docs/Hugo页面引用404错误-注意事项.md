# Hugo 页面引用 (Ref) 404 错误 - 注意事项

## 问题描述

在 Hugo 项目中，使用 `{{< ref "filename.md" >}}` 引用其他页面时，出现 `REF_NOT_FOUND` 错误，即使文件确实存在于对应的子目录中。

## 根本原因：叶子束 (Leaf Bundle) 与 分支束 (Branch Bundle) 的区别

### 问题核心
- **文件名**: `index.md` vs `_index.md`
- **行为差异**: 
    - 如果一个目录下存在 `index.md`，该目录被视为 **叶子束 (Leaf Bundle)**。
    - **叶子束不允许有子页面**。该目录下的所有其他 `.md` 文件都会被视为资源（Resources），而不是独立的页面。
    - 因此，`ref` 无法找到这些文件，因为它们在 Hugo 的页面索引中不存在。

### 错误示例
结构如下：
```
content/animancer/
├── index.md             <-- 错误：使用了 index.md
└── why/
    └── animancer-why.md <-- 被视为资源，而非页面
```
在这种情况下，引用 `{{< ref "why/animancer-why.md" >}}` 会失败。

### 正确配置
结构如下：
```
content/animancer/
├── _index.md            <-- 正确：使用 _index.md 使其成为分支束 (Section)
└── why/
    └── animancer-why.md <-- 现在是一个独立的页面
```

## 解决方案

1. **重命名主索引文件**:
   将 `content/目录/index.md` 重命名为 `content/目录/_index.md`。

2. **验证引用路径**:
   - 如果文件在同一目录下，可以使用 `{{< ref "filename.md" >}}`。
   - 如果文件在子目录下，建议使用相对于 `content` 的路径或相对路径，如 `{{< ref "subpath/filename.md" >}}`。
   - **注意**: Hugo 的 `ref` 也会尝试全局搜索唯一的名称，但在分支束结构中，明确路径更可靠。

## 类比理解

### 类比：文件夹的属性

*   **index.md (叶子束)**：像是一个**密封的包裹**。你可以看到包裹上的标签（index.md 的内容），包裹里可以放一些附件（图片、文本资源），但包裹里不能再有独立的“信件”（子页面）。
*   **_index.md (分支束/目录)**：像是一个**文件夹**。它本身有一张说明页（_index.md 的内容），但它同时允许文件夹内部存放很多独立的“文件”（子页面），并且可以继续嵌套文件夹。

## 检查清单

- [ ] 检查报错页面所在的目录是否包含 `index.md`。
- [ ] 如果该目录下有子页面或需要引用子目录的文件，请确保使用 `_index.md`。
- [ ] 检查引用语法是否正确：`{{< ref "path/to/file.md" >}}`。
- [ ] 确保目标文件的 Front Matter 中没有设置 `draft: true`（除非你构建时带了 `-D` 参数）。

## 参考资源

- [Hugo Content Organization - Page Bundles](https://gohugo.io/content-management/page-bundles/)
- [Hugo `ref` and `relref` shortcodes](https://gohugo.io/content-management/shortcodes/#ref-and-relref)

---

**创建日期**: 2026-01-05
**问题类型**: Hugo 内容组织结构
**关键词**: index.md, _index.md, Leaf Bundle, Branch Bundle, REF_NOT_FOUND
