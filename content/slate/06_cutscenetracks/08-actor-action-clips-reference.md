---
title: "Slate Cinematic Sequencer - 演员动作片段文档"
date: 2026-01-05T14:12:45+08:00
lastmod: 2026-01-05T14:12:45+08:00
draft: false
author: "逸空"
tags: ["Unity", "Animancer"]
categories: ["技术笔记"]
description: "深入了解 Slate Cinematic Sequencer - 演员动作片段文档 的使用方法和最佳实践"
type: "posts"
---

# Slate Cinematic Sequencer - 演员动作片段文档

## 概述

该页面是 **Slate Cinematic Sequencer** 的官方文档，位于 `https://slate.paradoxnotion.com/documentation/`。这是一个用于 Unity 的电影级序列编辑工具。

## 主要内容：演员动作片段参考 (7.5.2)

文档详细列举了可在**演员组的动作轨道**中添加的各类 ActionClips。内容按类别组织：

### 核心类别

**动画属性 (Animate Properties)**
- 支持在演员或其整个变换层级内的任何组件上动画化任意数量的属性或字段
- 支持 Blend In 和 Blend Out 功能，可从原始值平滑过渡到动画值
- 可编辑插值方式

**动画师 IK 控制**
- Animate Limb IK：需要 Animator Controller 和启用的 IK Pass
- Animate Look At IK：控制头部注视目标

**角色动画**
- Animate Blend Shape：操纵 Skinned Mesh Renderer 的混合形状
- Character Expression：混合角色表情
- Character Look At：使角色注视目标位置或变换

**路径动画**
- Animate On Path：沿预制路径移动角色
- Follow Path：跟随路径移动
- Pathfind From To：基于寻路的移动（需要烘焙的 NavMesh）

**变换操作**
- Translate/Rotate/Scale：移动、旋转、缩放演员
- Attach Object：附加对象或预制体
- Simple Grounder：将演员着地到下方最近的碰撞体

**其他类别**
- 事件（发送消息）
- GameObject 操作（可见性、激活状态）
- 渲染器（材质颜色、纹理动画）
- Sprites（精灵翻页、排序层设置）

## 技术特性

文档强调多数片段都拥有至少一个可动画化参数，支持在片段持续时间内动画化效果。

## 导航结构

完整文档包含 18 个主要章节，从"欢迎"到"脚本编程"，包含子章节如相机轨道、音频轨道、离线渲染等。
