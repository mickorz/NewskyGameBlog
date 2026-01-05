---
title: "Slate Cinematic Sequencer 文档 - 编辑器偏好设置"
date: 2026-01-05T14:12:45+08:00
lastmod: 2026-01-05T14:12:45+08:00
draft: false
author: "逸空"
tags: ["Unity", "Animancer"]
categories: ["技术笔记"]
description: "深入了解 Slate Cinematic Sequencer 文档 - 编辑器偏好设置 的使用方法和最佳实践"
type: "posts"
---

# Slate Cinematic Sequencer 文档 - 编辑器偏好设置

## 概览

本页面是 **Slate Cinematic Sequencer** 的官方文档，这是一个用于 Unity 的电影序列编辑工具。内容涵盖了编辑器偏好设置面板的详细说明。

## 编辑器偏好设置 (Editor Preferences)

编辑器偏好设置面板可通过 Slate 编辑器窗口右上角的"齿轮"图标打开。

### 主要设置项

**时间步长模式 (Time Step Mode)**
- 可设置为"秒"或"帧"
- 设置为帧时，编辑器显示帧数，强制吸附间隔为 1/30 或 1/60
- 仅用于显示目的，后台仍以秒为单位工作

**工作吸附间隔 (Working Snap Interval)**
- 指定吸附发生的秒数间隔
- 影响时间轴擦拭、剪辑放置和关键帧放置

**剪辑磁力吸附 (Clips Magnet Snapping)**
- 启用时，剪辑在时间轴编辑器中靠近时会自动时间对齐

**锁定X轴曲线编辑 (Lock xAxis Curve Editing)**
- 启用时，禁用在曲线编辑器中沿x轴（时间）移动关键帧
- 仍可通过DopeSheet编辑器移动关键帧

**自动首个关键帧 (Auto First Key)**
- 启用时，对每个无关键帧的可动画参数自动创建关键帧

**自动清理关键帧 (Auto Clean Keys)**
- 启用时，自动清理超出剪辑范围的关键帧

**显示关键帧值 (Show Keyframe Values)**
- 启用时，关键帧在DopeSheet编辑器中显示其数值

**初始关键帧切线 (Initial Keyframe Tangent)**
- 指定新创建关键帧的切线模式
- 默认为"光滑"(Smooth)

**关键帧样式 (Keyframes Style)**
- 指定DopeSheet编辑器中的关键帧图标是否反映切线模式或始终显示为菱形

**显示镜头缩略图 (Show Shot Thumbnails)**
- 启用时，摄像机轨道中的镜头剪辑显示渲染预览缩略图

**缩略图刷新频率 (Thumbnails Refresh)**
- 指定缩略图刷新频率（以帧为单位）
- 较低值更实时，但对编辑器性能有影响

**滚轮缩放 (Scroll Wheel Zooms)**
- 启用时，鼠标滚轮缩放时间轴
- 禁用时，滚轮上下滚动编辑器

**显示帮助描述 (Show Help Descriptions)**
- 启用时，选中元素的检查器中显示帮助信息
- 强烈推荐保持启用

**灯光亮度 (Gizmos Lightness)**
- 控制各种Slate特定辅助工具在场景视图中的亮暗程度

**运动路径颜色 (Motion Paths Color)**
- 设置运动路径在场景视图中的显示颜色

**自动创建导演摄像机 (Auto Create Director Camera)**
- 启用时，自动创建所需导演摄像机
- 强烈推荐保持启用

**后处理堆栈v2定义 (Use Post Processing Stack v2 Define)**
- 在导入Post Processing Stack v2的项目中启用
- 允许在摄像机镜头剪辑中直接控制景深效果

**HDRP定义 (Use HDRP Define)**
- 用于高清渲染管线项目

**URP定义 (Use URP Define)**
- 用于通用渲染管线项目

---

**最后更新：** 2023年2月19日
**官方网站：** slate.paradoxnotion.com
