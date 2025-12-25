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

1. [Why Animancer](./Why/Animancer_Why官方文档.md) - 了解为什么选择Animancer
2. [Mecanim vs Animancer](./Why/Animancer_MecanimVsAnimancer官方文档.md) - 核心对比
3. [Events 事件系统](./Event/Animancer_Events官方文档.md) - 基础事件使用
4. [Transitions 过渡系统](./Transition/Animancer_Transitions官方文档.md) - 动画过渡
5. [FSM 状态机](./FSM/Animancer_FSM官方文档.md) - 状态管理

---

## 📖 详细目录

### 🔧 核心功能 (5篇)

位于根目录 `Assets/Docs/Animancer/`

| 文档 | 说明 | 难度 |
|------|------|------|
| [Parameters 参数系统](./Animancer_Parameters官方文档.md) | 强类型参数系统，替代Animator参数 | ⭐⭐ |
| [IK 逆向动力学](./Animancer_IK官方文档.md) | IK系统配置和使用 | ⭐⭐⭐ |
| [Timeline 时间轴](./Animancer_Timeline官方文档.md) | Unity Timeline集成 (Pro) | ⭐⭐⭐ |
| [Strings 字符串优化](./Animancer_Strings官方文档.md) | StringReference性能优化 | ⭐⭐ |
| [Units 单位特性](./Animancer_Units官方文档.md) | Inspector单位显示 | ⭐ |

---

### 🎨 Blend - 混合系统 (9篇)

位于 `Assets/Docs/Animancer/Blend/`

| 文档 | 说明 | 难度 |
|------|------|------|
| [Blending 混合总览](./Blend/Animancer_Blending官方文档.md) | 混合系统概述 | ⭐⭐ |
| [Fading 淡入淡出](./Blend/Animancer_Fading官方文档.md) | 动画淡入淡出机制 | ⭐⭐ |
| [Fading Modes 淡入模式](./Blend/Animancer_FadingModes官方文档.md) | 不同的淡入模式对比 | ⭐⭐⭐ |
| [Custom Fading 自定义淡入](./Blend/Animancer_CustomFading官方文档.md) | 自定义淡入曲线 | ⭐⭐⭐ |
| [Layers 动画层](./Blend/Animancer_Layers官方文档.md) | 多层动画管理 | ⭐⭐⭐ |
| [Weighted Layers 权重层](./Blend/Animancer_WeightedLayers官方文档.md) | 加权动画层 | ⭐⭐⭐ |
| [Mixers 混合器](./Blend/Animancer_Mixers官方文档.md) | 混合器系统总览 | ⭐⭐⭐ |
| [Mixers Creation 创建混合器](./Blend/Animancer_MixersCreation官方文档.md) | 线性/笛卡尔/手动混合器 | ⭐⭐⭐ |
| [Mixers Synchronization 混合同步](./Blend/Animancer_MixersSynchronization官方文档.md) | 混合器同步机制 | ⭐⭐⭐⭐ |

---

### ⚡ Event - 事件系统 (9篇)

位于 `Assets/Docs/Animancer/Event/`

| 文档 | 说明 | 难度 |
|------|------|------|
| [Events 事件总览](./Event/Animancer_Events官方文档.md) | 事件系统概述 | ⭐⭐ |
| [Animation Events 原生事件](./Event/Animancer_AnimationEvents官方文档.md) | Unity原生AnimationEvent | ⭐⭐ |
| [Animancer Events 自定义事件](./Event/Animancer_AnimancerEvents官方文档.md) | Animancer事件系统 (Pro) | ⭐⭐⭐ |
| [Events Usage 事件使用](./Event/Animancer_EventsUsage官方文档.md) | 三种事件配置方式 | ⭐⭐ |
| [Events Behaviour 事件行为](./Event/Animancer_EventsBehaviour官方文档.md) | 循环与非循环事件 | ⭐⭐⭐ |
| [Events Parameters 事件参数](./Event/Animancer_EventsParameters官方文档.md) | 带参数的事件 | ⭐⭐⭐ |
| [Events Utilities 事件工具](./Event/Animancer_EventsUtilities官方文档.md) | AnimancerEvent.Current等工具 | ⭐⭐⭐ |
| [End Events 结束事件](./Event/Animancer_EndEvents官方文档.md) | 动画结束事件详解 | ⭐⭐ |
| [End Events Alternatives 替代方案](./Event/Animancer_EndEventsAlternatives官方文档.md) | Coroutine/手动检查等方式 | ⭐⭐ |

---

### 🔄 FSM - 状态机系统 (10篇)

位于 `Assets/Docs/Animancer/FSM/`

| 文档 | 说明 | 难度 |
|------|------|------|
| [FSM 状态机总览](./FSM/Animancer_FSM官方文档.md) | 状态机基础概念 | ⭐⭐ |
| [FSM Overview 系统概述](./FSM/Animancer_FSMOverview官方文档.md) | 设计目标和架构 | ⭐⭐ |
| [State Types 状态类型](./FSM/Animancer_StateTypes官方文档.md) | MonoBehaviour/ScriptableObject/POCO | ⭐⭐⭐ |
| [Initialization 初始化](./FSM/Animancer_Initialization官方文档.md) | 序列化字段/只读字段方式 | ⭐⭐⭐ |
| [Changing States 状态切换](./FSM/Animancer_ChangingStates官方文档.md) | TrySetState/ForceSetState等 | ⭐⭐ |
| [Keys 键值状态机](./FSM/Animancer_Keys官方文档.md) | 有键/无键状态机 | ⭐⭐⭐ |
| [Input Buffer 输入缓冲](./FSM/Animancer_InputBuffer官方文档.md) | 连击系统输入缓冲 | ⭐⭐⭐ |
| [State Selector 状态选择器](./FSM/Animancer_StateSelector官方文档.md) | 优先级状态选择 | ⭐⭐⭐ |
| [Owned States 状态所有权](./FSM/Animancer_OwnedStates官方文档.md) | IOwnedState接口 | ⭐⭐⭐ |
| [Creating Custom States 自定义状态](./FSM/Animancer_CreatingCustomStates官方文档.md) | 创建自定义AnimancerState (Pro) | ⭐⭐⭐⭐ |

---

### 🎬 Transition - 过渡系统 (6篇)

位于 `Assets/Docs/Animancer/Transition/`

| 文档 | 说明 | 难度 |
|------|------|------|
| [Transitions 过渡总览](./Transition/Animancer_Transitions官方文档.md) | 过渡系统概述 | ⭐⭐ |
| [Transition Types 过渡类型](./Transition/Animancer_TransitionTypes官方文档.md) | Clip/Mixer/Controller等类型 | ⭐⭐⭐ |
| [Transition Assets 过渡资产](./Transition/Animancer_TransitionAssets官方文档.md) | ScriptableObject过渡 | ⭐⭐⭐ |
| [Transition Libraries 过渡库](./Transition/Animancer_TransitionLibraries官方文档.md) | 集中管理过渡资产 | ⭐⭐⭐ |
| [Transition Previews 预览功能](./Transition/Animancer_TransitionPreviews官方文档.md) | Inspector预览 (Pro) | ⭐⭐ |
| [Transition Sequences 序列过渡](./Transition/Animancer_TransitionSequences官方文档.md) | 顺序播放多个动画 | ⭐⭐⭐ |

---

### 🔌 Animator - Controller集成 (3篇)

位于 `Assets/Docs/Animancer/Animator/`

| 文档 | 说明 | 难度 |
|------|------|------|
| [Animator Controllers 控制器集成](./Animator/Animancer_AnimatorControllers官方文档.md) | Native/Hybrid模式 | ⭐⭐⭐ |
| [Controllers Conversion 转换指南](./Animator/Animancer_AnimatorControllersConversion官方文档.md) | Mecanim迁移到Animancer | ⭐⭐⭐⭐ |
| [Controller States 控制器状态](./Animator/Animancer_ControllerStates官方文档.md) | ControllerState使用 (Pro) | ⭐⭐⭐ |

---

### 🆚 Why - Mecanim vs Animancer对比 (15篇)

位于 `Assets/Docs/Animancer/Why/`

#### 核心对比

| 文档 | 说明 | 难度 |
|------|------|------|
| [Mecanim vs Animancer 总对比](./Why/Animancer_MecanimVsAnimancer官方文档.md) | 全面对比和决策指南 | ⭐⭐ |

#### Why系列 - 六大优势

| 文档 | 说明 | 难度 |
|------|------|------|
| [Why Animancer 六大理由](./Why/Animancer_Why官方文档.md) | 选择Animancer的原因 | ⭐ |
| [Simplicity 简洁性](./Why/Animancer_Simplicity官方文档.md) | 7步 vs 1步 | ⭐ |
| [Transparency 透明性](./Why/Animancer_Transparency官方文档.md) | 黑盒 vs 透明 | ⭐⭐ |
| [Adaptability 适应性](./Why/Animancer_Adaptability官方文档.md) | 关注点分离 | ⭐⭐ |
| [Clarity 清晰性](./Why/Animancer_Clarity官方文档.md) | 依赖明确 | ⭐⭐ |
| [Safety 安全性](./Why/Animancer_Safety官方文档.md) | 类型安全 vs 魔法字符串 | ⭐⭐ |
| [Reliability 可靠性](./Why/Animancer_Reliability官方文档.md) | 即时 vs 延迟 | ⭐⭐ |

#### Comparison系列 - 实战对比

| 文档 | 说明 | 难度 |
|------|------|------|
| [Comparison 对比总览](./Why/Animancer_Comparison官方文档.md) | 四大场景对比 | ⭐ |
| [Playing 播放对比](./Why/Animancer_Playing官方文档.md) | 播放动画方式对比 | ⭐ |
| [Waiting 等待对比](./Why/Animancer_Waiting官方文档.md) | 等待动画结束对比 | ⭐⭐ |
| [Speed and Time 速度时间对比](./Why/Animancer_SpeedAndTime官方文档.md) | 速度控制对比 | ⭐⭐ |
| [Weapon Animations 武器动画对比](./Why/Animancer_WeaponAnimations官方文档.md) | 武器系统对比 | ⭐⭐⭐ |

#### 其他

| 文档 | 说明 | 难度 |
|------|------|------|
| [Performance 性能对比](./Why/Animancer_Performance官方文档.md) | 性能测试数据 | ⭐⭐ |
| [Glossary 术语表](./Why/Animancer_Glossary官方文档.md) | 术语对照表 | ⭐ |

---

## 🗺️ 学习路线图

### 初级（入门）

**目标**: 理解Animancer基础概念，能够播放简单动画

1. ✅ [Why Animancer](./Why/Animancer_Why官方文档.md) - 了解优势
2. ✅ [Playing 播放对比](./Why/Animancer_Playing官方文档.md) - 播放动画
3. ✅ [Transitions 过渡系统](./Transition/Animancer_Transitions官方文档.md) - 动画过渡
4. ✅ [Fading 淡入淡出](./Blend/Animancer_Fading官方文档.md) - 平滑切换

**实战项目**: 简单的角色移动动画（Idle → Walk → Run）

---

### 中级（进阶）

**目标**: 掌握事件、状态机、混合系统

5. ✅ [Events 事件系统](./Event/Animancer_Events官方文档.md) - 动画事件
6. ✅ [FSM 状态机](./FSM/Animancer_FSM官方文档.md) - 状态管理
7. ✅ [Layers 动画层](./Blend/Animancer_Layers官方文档.md) - 多层动画
8. ✅ [Mixers 混合器](./Blend/Animancer_Mixers官方文档.md) - 动画混合

**实战项目**: 完整的角色控制器（移动 + 战斗 + 交互）

---

### 高级（精通）

**目标**: 自定义扩展、性能优化、复杂系统

9. ✅ [Creating Custom States](./FSM/Animancer_CreatingCustomStates官方文档.md) - 自定义状态
10. ✅ [Input Buffer](./FSM/Animancer_InputBuffer官方文档.md) - 输入缓冲
11. ✅ [Controller States](./Animator/Animancer_ControllerStates官方文档.md) - Controller集成
12. ✅ [Performance 性能对比](./Why/Animancer_Performance官方文档.md) - 性能优化

**实战项目**: 复杂的战斗系统（连击 + AI + 多武器）

---

## 🔍 快速查找

### 按功能查找

**播放动画:**
- [Transitions 过渡系统](./Transition/Animancer_Transitions官方文档.md)
- [Playing 播放对比](./Why/Animancer_Playing官方文档.md)

**动画事件:**
- [Events 事件系统](./Event/Animancer_Events官方文档.md)
- [End Events 结束事件](./Event/Animancer_EndEvents官方文档.md)

**状态管理:**
- [FSM 状态机](./FSM/Animancer_FSM官方文档.md)
- [Changing States 状态切换](./FSM/Animancer_ChangingStates官方文档.md)

**动画混合:**
- [Fading 淡入淡出](./Blend/Animancer_Fading官方文档.md)
- [Layers 动画层](./Blend/Animancer_Layers官方文档.md)
- [Mixers 混合器](./Blend/Animancer_Mixers官方文档.md)

**性能优化:**
- [Strings 字符串优化](./Animancer_Strings官方文档.md)
- [Performance 性能对比](./Why/Animancer_Performance官方文档.md)

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
1. [Why Animancer](./Why/Animancer_Why官方文档.md) - 理解优势
2. [Mecanim vs Animancer](./Why/Animancer_MecanimVsAnimancer官方文档.md) - 对比差异
3. [Transitions 过渡系统](./Transition/Animancer_Transitions官方文档.md) - 基础使用

### Q: Lite版本和Pro版本有什么区别？

**A:** 查看标有 **(Pro)** 的文档，这些功能仅在Pro版本可用：
- 自定义AnimancerState
- Timeline集成
- Controller States
- Transition Previews

### Q: 如何从Mecanim迁移到Animancer？

**A:** 参考 [Controllers Conversion 转换指南](./Animator/Animancer_AnimatorControllersConversion官方文档.md)

### Q: 性能如何？

**A:** 参考 [Performance 性能对比](./Why/Animancer_Performance官方文档.md)，Animancer通常比Mecanim快5%左右

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
