---
title: "Slate Cinematic Sequencer 文档提取"
date: 2026-01-05T14:12:45+08:00
lastmod: 2026-01-05T14:12:45+08:00
draft: false
author: "逸空"
tags: ["Unity", "Animancer"]
categories: ["技术笔记"]
description: "深入了解 Slate Cinematic Sequencer 文档提取 的使用方法和最佳实践"
type: "posts"
---


# Slate Cinematic Sequencer 文档提取

## 页面概述

这是Slate Cinematic Sequencer for Unity的官方文档页面。该页面包含完整的产品文档导航和"Cutscene Groups"章节的详细内容。

## 主要内容

### 文档导航结构

文档包含18个主要章节：
- Welcome（欢迎）
- Getting Started（快速开始）
- Editor Overview（编辑器概览）
- Editor Preferences（编辑器偏好设置）
- Action Clips Overview（动作片段概览）
- 以及Camera Track、Audio Track等多个轨道类型

### Cutscene Groups（第6章）详解

**核心概念：**
Cutscene Groups包含Cutscene Tracks，每个都指向一个目标GameObject（称为Actor）。

**两种Group类型：**

1. **Director Group（导演组）**
   - 是cutscene的主控组，每个场景仅一个且不可删除
   - 目标为Director Camera（导演摄像机）
   - 支持的轨道：Camera Track、Action Track、Audio Track、Video Track
   - 用途：全局控制如摄像机镜头、环境光照动画、字幕、对象创建

2. **Actor Group（演员组）**
   - 用于影响特定GameObject的各种方式
   - 可通过拖放创建
   - 支持轨道：Action Track、Audio Track、Animator Track
   - 支持右键菜单替换actor、快速选择等功能

**核心功能特性：**
- Groups可被禁用（无任何作用）或锁定（防止修改）
- Actor Groups可通过拖拽重新排序
- Director Group始终保持在顶部
- 可通过双击快速选择scene中的actor
