# Animancer 中文文档目录

> 完整的 Animancer 官方文档中文翻译版，包含丰富的代码示例和最佳实践。

**文档版本**: 1.0
**最后更新**: 2025-12-25
**适用 Animancer 版本**: 8.0+

---

## 📊 文档统计

- **总文档数**: 57篇
- **代码示例**: 500+ 个
- **涵盖内容**: 从基础到高级的完整Animancer使用指南

---

## 📚 目录结构

```
Animancer/
├── README.md (本文件)
├── 核心功能 (5篇)
├── Blend/ (9篇) - 混合系统
├── Event/ (9篇) - 事件系统
├── FSM/ (10篇) - 状态机系统
├── Transition/ (6篇) - 过渡系统
├── Animator/ (3篇) - Animator Controller集成
└── Why/ (15篇) - Mecanim vs Animancer对比
```

---

## 🎯 快速导航

### 新手入门推荐路线

1. [\1](./why/animancer-why.md) - 了解为什么选择Animancer
2. [\1](./why/animancer-mecanimvsanimancer.md) - 核心对比
3. [\1](./event/animancer-events.md) - 基础事件使用
4. [\1](./transition/animancer-transitions.md) - 动画过渡
5. [\1](./fsm/animancer-fsm.md) - 状态管理

---

## 📖 详细目录

### 🔧 核心功能 (5篇)

位于根目录 `Assets/Docs/Animancer/`

| 文档 | 说明 | 难度 |
|------|------|------|
| [\1](./animancer-parameters.md) | 强类型参数系统，替代Animator参数 | ⭐⭐ |
| [IK 逆向动力学](./animancer-ik.md) | IK系统配置和使用 | ⭐⭐⭐ |
| [\1](./animancer-timeline.md) | Unity Timeline集成 (Pro) | ⭐⭐⭐ |
| [\1](./animancer-strings.md) | StringReference性能优化 | ⭐⭐ |
| [\1](./animancer-units.md) | Inspector单位显示 | ⭐ |

---

### 🎨 Blend - 混合系统 (9篇)

位于 `Assets/Docs/Animancer/Blend/`

| 文档 | 说明 | 难度 |
|------|------|------|
| [\1](./blend/animancer-blending.md) | 混合系统概述 | ⭐⭐ |
| [\1](./blend/animancer-fading.md) | 动画淡入淡出机制 | ⭐⭐ |
| [\1](./blend/animancer-fadingmodes.md) | 不同的淡入模式对比 | ⭐⭐⭐ |
| [\1](./blend/animancer-customfading.md) | 自定义淡入曲线 | ⭐⭐⭐ |
| [\1](./blend/animancer-layers.md) | 多层动画管理 | ⭐⭐⭐ |
| [\1](./blend/animancer-weightedlayers.md) | 加权动画层 | ⭐⭐⭐ |
| [\1](./blend/animancer-mixers.md) | 混合器系统总览 | ⭐⭐⭐ |
| [\1](./blend/animancer-mixerscreation.md) | 线性/笛卡尔/手动混合器 | ⭐⭐⭐ |
| [\1](./blend/animancer-mixerssynchronization.md) | 混合器同步机制 | ⭐⭐⭐⭐ |

---

### ⚡ Event - 事件系统 (9篇)

位于 `Assets/Docs/Animancer/Event/`

| 文档 | 说明 | 难度 |
|------|------|------|
| [\1](./event/animancer-events.md) | 事件系统概述 | ⭐⭐ |
| [\1](./event/animancer-animationevents.md) | Unity原生AnimationEvent | ⭐⭐ |
| [\1](./event/animancer-animancerevents.md) | Animancer事件系统 (Pro) | ⭐⭐⭐ |
| [\1](./event/animancer-eventsusage.md) | 三种事件配置方式 | ⭐⭐ |
| [\1](./event/animancer-eventsbehaviour.md) | 循环与非循环事件 | ⭐⭐⭐ |
| [\1](./event/animancer-eventsparameters.md) | 带参数的事件 | ⭐⭐⭐ |
| [\1](./event/animancer-eventsutilities.md) | AnimancerEvent.Current等工具 | ⭐⭐⭐ |
| [\1](./event/animancer-endevents.md) | 动画结束事件详解 | ⭐⭐ |
| [\1](./event/animancer-endeventsalternatives.md) | Coroutine/手动检查等方式 | ⭐⭐ |

---

### 🔄 FSM - 状态机系统 (10篇)

位于 `Assets/Docs/Animancer/FSM/`

| 文档 | 说明 | 难度 |
|------|------|------|
| [\1](./fsm/animancer-fsm.md) | 状态机基础概念 | ⭐⭐ |
| [\1](./fsm/animancer-fsmoverview.md) | 设计目标和架构 | ⭐⭐ |
| [\1](./fsm/animancer-statetypes.md) | MonoBehaviour/ScriptableObject/POCO | ⭐⭐⭐ |
| [\1](./fsm/animancer-initialization.md) | 序列化字段/只读字段方式 | ⭐⭐⭐ |
| [\1](./fsm/animancer-changingstates.md) | TrySetState/ForceSetState等 | ⭐⭐ |
| [\1](./fsm/animancer-keys.md) | 有键/无键状态机 | ⭐⭐⭐ |
| [\1](./fsm/animancer-inputbuffer.md) | 连击系统输入缓冲 | ⭐⭐⭐ |
| [\1](./fsm/animancer-stateselector.md) | 优先级状态选择 | ⭐⭐⭐ |
| [\1](./fsm/animancer-ownedstates.md) | IOwnedState接口 | ⭐⭐⭐ |
| [\1](./fsm/animancer-creatingcustomstates.md) | 创建自定义AnimancerState (Pro) | ⭐⭐⭐⭐ |

---

### 🎬 Transition - 过渡系统 (6篇)

位于 `Assets/Docs/Animancer/Transition/`

| 文档 | 说明 | 难度 |
|------|------|------|
| [\1](./transition/animancer-transitions.md) | 过渡系统概述 | ⭐⭐ |
| [\1](./transition/animancer-transitiontypes.md) | Clip/Mixer/Controller等类型 | ⭐⭐⭐ |
| [\1](./transition/animancer-transitionassets.md) | ScriptableObject过渡 | ⭐⭐⭐ |
| [\1](./transition/animancer-transitionlibraries.md) | 集中管理过渡资产 | ⭐⭐⭐ |
| [\1](./transition/animancer-transitionpreviews.md) | Inspector预览 (Pro) | ⭐⭐ |
| [\1](./transition/animancer-transitionsequences.md) | 顺序播放多个动画 | ⭐⭐⭐ |

---

### 🔌 Animator - Controller集成 (3篇)

位于 `Assets/Docs/Animancer/Animator/`

| 文档 | 说明 | 难度 |
|------|------|------|
| [\1](./animator/animancer-animatorcontrollers.md) | Native/Hybrid模式 | ⭐⭐⭐ |
| [\1](./animator/animancer-animatorcontrollersconversion.md) | Mecanim迁移到Animancer | ⭐⭐⭐⭐ |
| [\1](./animator/animancer-controllerstates.md) | ControllerState使用 (Pro) | ⭐⭐⭐ |

---

### 🆚 Why - Mecanim vs Animancer对比 (15篇)

位于 `Assets/Docs/Animancer/Why/`

#### 核心对比

| 文档 | 说明 | 难度 |
|------|------|------|
| [\1](./why/animancer-mecanimvsanimancer.md) | 全面对比和决策指南 | ⭐⭐ |

#### Why系列 - 六大优势

| 文档 | 说明 | 难度 |
|------|------|------|
| [\1](./why/animancer-why.md) | 选择Animancer的原因 | ⭐ |
| [\1](./why/animancer-simplicity.md) | 7步 vs 1步 | ⭐ |
| [\1](./why/animancer-transparency.md) | 黑盒 vs 透明 | ⭐⭐ |
| [\1](./why/animancer-adaptability.md) | 关注点分离 | ⭐⭐ |
| [\1](./why/animancer-clarity.md) | 依赖明确 | ⭐⭐ |
| [\1](./why/animancer-safety.md) | 类型安全 vs 魔法字符串 | ⭐⭐ |
| [\1](./why/animancer-reliability.md) | 即时 vs 延迟 | ⭐⭐ |

#### Comparison系列 - 实战对比

| 文档 | 说明 | 难度 |
|------|------|------|
| [\1](./why/animancer-comparison.md) | 四大场景对比 | ⭐ |
| [\1](./why/animancer-playing.md) | 播放动画方式对比 | ⭐ |
| [\1](./why/animancer-waiting.md) | 等待动画结束对比 | ⭐⭐ |
| [\1](./why/animancer-speedandtime.md) | 速度控制对比 | ⭐⭐ |
| [\1](./why/animancer-weaponanimations.md) | 武器系统对比 | ⭐⭐⭐ |

#### 其他

| 文档 | 说明 | 难度 |
|------|------|------|
| [\1](./why/animancer-performance.md) | 性能测试数据 | ⭐⭐ |
| [\1](./why/animancer-glossary.md) | 术语对照表 | ⭐ |

---

## 🗺️ 学习路线图

### 初级（入门）

**目标**: 理解Animancer基础概念，能够播放简单动画

1. ✅ [\1](./why/animancer-why.md) - 了解优势
2. ✅ [\1](./why/animancer-playing.md) - 播放动画
3. ✅ [\1](./transition/animancer-transitions.md) - 动画过渡
4. ✅ [\1](./blend/animancer-fading.md) - 平滑切换

**实战项目**: 简单的角色移动动画（Idle → Walk → Run）

---

### 中级（进阶）

**目标**: 掌握事件、状态机、混合系统

5. ✅ [\1](./event/animancer-events.md) - 动画事件
6. ✅ [\1](./fsm/animancer-fsm.md) - 状态管理
7. ✅ [\1](./blend/animancer-layers.md) - 多层动画
8. ✅ [\1](./blend/animancer-mixers.md) - 动画混合

**实战项目**: 完整的角色控制器（移动 + 战斗 + 交互）

---

### 高级（精通）

**目标**: 自定义扩展、性能优化、复杂系统

9. ✅ [\1](./fsm/animancer-creatingcustomstates.md) - 自定义状态
10. ✅ [\1](./fsm/animancer-inputbuffer.md) - 输入缓冲
11. ✅ [\1](./animator/animancer-controllerstates.md) - Controller集成
12. ✅ [\1](./why/animancer-performance.md) - 性能优化

**实战项目**: 复杂的战斗系统（连击 + AI + 多武器）

---

## 🔍 快速查找

### 按功能查找

**播放动画:**
- [\1](./transition/animancer-transitions.md)
- [\1](./why/animancer-playing.md)

**动画事件:**
- [\1](./event/animancer-events.md)
- [\1](./event/animancer-endevents.md)

**状态管理:**
- [\1](./fsm/animancer-fsm.md)
- [\1](./fsm/animancer-changingstates.md)

**动画混合:**
- [\1](./blend/animancer-fading.md)
- [\1](./blend/animancer-layers.md)
- [\1](./blend/animancer-mixers.md)

**性能优化:**
- [\1](./animancer-strings.md)
- [\1](./why/animancer-performance.md)

---

## 📝 文档说明

### 难度标识

- ⭐ **基础** - 适合新手
- ⭐⭐ **简单** - 需要基础知识
- ⭐⭐⭐ **中等** - 需要一定经验
- ⭐⭐⭐⭐ **困难** - 需要深入理解

### 版本标识

- **(Pro)** - 需要Animancer Pro版本
- **无标识** - Lite和Pro版本都可用

### 文档特点

✅ 完整的中文翻译
✅ 丰富的代码示例（10x+原文）
✅ 详细的对比表格
✅ 最佳实践指南（✅ DO / ❌ DON'T）
✅ FAQ常见问题
✅ 完整的交叉引用

---

## 🔗 外部资源

### 官方资源

- [Animancer 官网](https://kybernetik.com.au/animancer/)
- [Animancer API 文档](https://kybernetik.com.au/animancer/api/)
- [Animancer Samples](https://kybernetik.com.au/animancer/docs/samples/)

### Unity资源

- [Unity Animation System](https://docs.unity3d.com/Manual/AnimationOverview.html)
- [Unity Playables API](https://docs.unity3d.com/Manual/Playables.html)

---

## 💡 常见问题

### Q: 从哪里开始学习？

**A:** 推荐按以下顺序：
1. [\1](./why/animancer-why.md) - 理解优势
2. [\1](./why/animancer-mecanimvsanimancer.md) - 对比差异
3. [\1](./transition/animancer-transitions.md) - 基础使用

### Q: Lite版本和Pro版本有什么区别？

**A:** 查看标有 **(Pro)** 的文档，这些功能仅在Pro版本可用：
- 自定义AnimancerState
- Timeline集成
- Controller States
- Transition Previews

### Q: 如何从Mecanim迁移到Animancer？

**A:** 参考 [\1](./animator/animancer-animatorcontrollersconversion.md)

### Q: 性能如何？

**A:** 参考 [\1](./why/animancer-performance.md)，Animancer通常比Mecanim快5%左右

---

## 📮 反馈与贡献

如发现文档错误或有改进建议，欢迎反馈！

---

**创建日期**: 2025-12-25
**文档数量**: 57篇
**总字数**: 约30万字

---

## 📊 文档统计详情

| 类别 | 文档数 | 平均长度 |
|------|--------|---------|
| 核心功能 | 5 | 5000字 |
| Blend混合 | 9 | 6000字 |
| Event事件 | 9 | 5500字 |
| FSM状态机 | 10 | 6500字 |
| Transition过渡 | 6 | 5500字 |
| Animator集成 | 3 | 7000字 |
| Why对比 | 15 | 4500字 |
| **总计** | **57** | **5500字** |

---

**Happy Animancing! 🎮✨**
