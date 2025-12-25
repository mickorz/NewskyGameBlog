---
title: "Animancer - Glossary 术语表"
date: 2025-12-25
draft: false
---

# Animancer - Glossary 术语表

## 通用术语

| 术语 | 描述 |
|------|------|
| **Unity编辑器** | 用于开发Unity游戏的应用程序 |
| **检视面板(Inspector)** | 查看和编辑所选对象详细信息的窗口 |
| **编辑模式** | 编辑场景和脚本，不运行游戏 |
| **播放模式** | 在编辑器中测试运行游戏 |
| **运行时构建** | 编译为独立应用程序供玩家使用 |

## 动画术语

| 术语 | 描述 |
|------|------|
| **Mecanim** | Unity基于控制器的动画系统 |
| **Playables** | Unity低级API，用于控制动画等可播放对象 |
| **AnimationClip** | 包含动画数据的资源文件 |
| **动画控制器(Animator Controller)** | 包含有限状态机的资源 |
| **AnimancerComponent** | Animancer主组件，替代Animator Controller |
| **状态(State)** | 图形中的节点，管理AnimationClip播放 |
| **动画层(Layer)** | 共享目的的状态组 |
| **混合树/混合器(Blend Tree/Mixer)** | 管理多个子状态混合的特殊状态 |
| **权重(Weight)** | 0到1之间的值，决定状态对最终混合的影响 |
| **淡入/淡出(Fade In/Out)** | 动画权重的渐变过渡 |
| **根运动(Root Motion)** | 使用动画数据驱动角色移动 |
| **IK(Inverse Kinematics)** | 逆向动力学，通过末端位置控制骨骼链 |

## Animancer特有术语

| 术语 | 描述 |
|------|------|
| **AnimancerState** | Animancer中管理单个动画的状态对象 |
| **Transition** | 定义如何播放动画的配置资产 |
| **Event** | 在动画特定时间点触发的回调 |
| **FSM(Finite State Machine)** | Animancer的独立状态机系统 |
| **StateBehaviour** | 自动启用/禁用的MonoBehaviour状态基类 |
| **HybridAnimancerComponent** | 支持Controller和Animancer混合的组件 |

---

**文档版本**: 1.0
**最后更新**: 2025-12-25
