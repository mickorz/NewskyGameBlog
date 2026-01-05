---
title: "动画轨道 (Animator Track) 文档"
date: 2026-01-05T14:12:45+08:00
lastmod: 2026-01-05T14:12:45+08:00
draft: false
author: "逸空"
tags: ["Unity", "Animancer", "Animator"]
categories: ["技术笔记"]
description: "深入了解 动画轨道 (Animator Track) 文档 的使用方法和最佳实践"
type: "posts"
---

# 动画轨道 (Animator Track) 文档

## 概述

动画轨道能够播放为Mecanim创建的动画剪辑。演员需要具有Animator组件，但**无需创建或分配任何动画控制器**。如果分配了控制器，动画轨道可以混合叠加在控制器正在播放的动画之上。

## 多层动画支持

可在同一演员组中添加多个动画轨道。每条轨道代表一个单独的动画层，具有自己的权重，可以以覆盖(Override)或加法(Additive)方式与下层混合，并可通过[Avatar Masks](https://docs.unity3d.com/560/Documentation/Manual/class-AvatarMask.html)选择性影响演员身体的不同部位。

## 根运动(Root Motion)

如在**第一个**动画轨道中启用"Use Root Motion"参数，可使用来自动画的根运动。需要注意的是，仅第一个(底部)动画轨道拥有此选项，根运动仅可应用于该第一动画轨道内播放的动画剪辑。与Slate中的大多数剪辑一样，动画轨道中使用的动画剪辑也可相互混合，或与下层轨道正在播放的动画混合进/出。

## 动画剪辑设置

### 基础参数

| 参数 | 说明 |
|------|------|
| **Animation Clip** | 要播放的动画剪辑 |
| **Clip Offset** | 动画剪辑开始时间相对于Slate剪辑开始时间的时间偏移 |
| **Clip Wrap Mode** | 循环(Loop)或乒乓球(Ping Pong)模式 |
| **Clip Weight** | 动画剪辑的权重(乘以轨道权重) |
| **Playback Speed** | 播放速度(可为正值或负值用于反向播放) |

### 起始变换设置

这些设置在动画具有根运动且在动画轨道中启用"Use Root Motion"时最为相关:

- **Starting Transforms Mode**:
  - "Auto Match Transforms" - 自动匹配演员位置/旋转到前一剪辑的最后位置/旋转(默认)
  - "Manually Set Transforms" - 手动设置起始位置/旋转

- **Transform Space**: 位置/旋转设置所在的空间(默认为过场空间)

- **Starting Position**: 手动模式下的起始位置(可在场景视图中编辑)

- **Starting Rotation**: 手动模式下的起始旋转(可在场景视图中编辑)

### 本地旋转偏移

此可动画化参数允许对演员旋转进行动画化偏移。例如，仅使用"Walk"动画但通过动画化"Y"值使演员转身时很有用。

## 重要提示

若动画未循环,请确保AnimationClip的"Loop Time"选项已启用。

---

**上次更新**: 2025年4月4日
