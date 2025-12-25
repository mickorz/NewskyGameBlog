# Animancer Transition Previews 官方文档

> 原文地址：https://kybernetik.com.au/animancer/docs/manual/transitions/previews/
> 抓取日期：2025-01-24

---

## 概述 (Overview)

**Transition Previews** 功能允许开发者**在编辑器中预览动画过渡效果，无需进入 Play Mode**，从而大大提高动画调试和迭代效率。

### 核心功能

> "预览过渡效果的样子，无需进入 Play Mode"

**主要用途**：
1. **可视化预览**：直接查看动画切换效果
2. **快速调试**：实时调整过渡参数
3. **多角色测试**：在不同角色模型上测试动画
4. **时间轴控制**：精确查看动画的每一帧

---

## 打开 Preview 窗口

### 方法1：点击预览图标

在 Inspector 中，任何 Transition 字段旁边都有一个**预览图标**：

```
┌─────────────────────────────────────┐
│ Idle Animation                      │
│ ┌─────────────────────────────┐ [▶] │  ← 点击这个图标
│ │ Clip: Rifle_Idle            │     │
│ │ Fade Duration: 0.25         │     │
│ └─────────────────────────────┘     │
└─────────────────────────────────────┘
```

点击 `[▶]` 图标后，会打开一个新的 Inspector 窗口，专门用于预览该 Transition。

---

### 方法2：右键菜单

```
1. 右键点击 Transition 字段
2. 选择 "Open Preview"
```

---

## Preview 窗口界面

打开 Preview 后，你会看到以下界面：

```
┌────────────────────────────────────────────┐
│ Transition Preview                         │
├────────────────────────────────────────────┤
│ ┌────────────────────────────────────────┐ │
│ │                                        │ │
│ │         [场景预览窗口]                 │ │
│ │     显示角色和动画效果                │ │
│ │                                        │ │
│ └────────────────────────────────────────┘ │
├────────────────────────────────────────────┤
│ Preview Settings:                          │
│ ├─ Previous Animation: [选择动画]         │
│ ├─ Current Transition: Idle (显示)        │
│ └─ Next Animation: [选择动画]             │
├────────────────────────────────────────────┤
│ Timeline:                                  │
│ ├─────────────────────────────────────────│ │
│ │ ← ═══════|══════════════════════ →     │ │  ← 可拖拽
│ └─────────────────────────────────────────│ │
├────────────────────────────────────────────┤
│ Transition Inspector:                      │
│ ├─ Clip: Rifle_Idle                       │
│ ├─ Fade Duration: 0.25                    │
│ ├─ Speed: 1                               │
│ └─ ...                                    │
└────────────────────────────────────────────┘
```

---

## 主要功能详解

### 1. 场景预览窗口

**显示内容**：
- 角色模型的 3D 视图
- 实时播放动画
- 可以旋转视角查看不同角度

**操作**：
- **左键拖拽**：旋转视角
- **滚轮**：缩放
- **中键拖拽**：平移视图

---

### 2. Preview Settings（预览设置）

#### Previous Animation（前一个动画）

**作用**：设置过渡的**起始动画**

```
示例：
├─ Previous: Walk
├─ Current: Idle (要预览的)
└─ Next: Run

预览效果：
Walk → (淡入) → Idle → (淡出) → Run
```

**自动选择逻辑**：
- Animancer 会尝试**自动找到**同一角色引用的其他动画
- 默认优先选择名称包含 `"_Idle_"` 的动画
- 如果找不到，使用空动画

**手动设置**：
```
点击 Previous Animation 的对象字段
→ 从下拉列表选择或拖入动画片段
```

---

#### Current Transition（当前过渡）

**显示**：正在预览的 Transition

这个字段是**只读的**，显示你当前选中的 Transition 配置。

---

#### Next Animation（后一个动画）

**作用**：设置过渡的**目标动画**

```
示例：
├─ Previous: Idle
├─ Current: Walk (要预览的)
└─ Next: Run

预览效果：
Idle → (淡入) → Walk → (淡出) → Run
```

**用途**：
- 查看动画如何淡出到下一个动画
- 测试连续的动画切换效果

---

### 3. Timeline（时间轴）

**功能**：精确控制动画播放时间

```
Timeline:
├─────────────────────────────────────────│
│ ← ═══════|══════════════════════ →     │  ← 拖拽滑块
└─────────────────────────────────────────│
   ↑       ↑                        ↑
  开始  当前时间                   结束
```

**操作**：
- **点击并拖拽**：在时间轴上任意位置点击拖拽，动画会跳到对应时间
- **查看淡入淡出**：可以清晰看到动画混合的过程

**应用场景**：
```
场景1：检查动画的特定帧
拖拽到 0.5 → 查看动画中间时刻的姿态

场景2：检查淡入效果
拖拽到 0.1 → 查看淡入 10% 时两个动画的混合

场景3：检查淡出效果
拖拽到 0.9 → 查看淡出前的状态
```

---

### 4. Transition Inspector（过渡检查器）

**显示内容**：
- 标准的 Play Mode Inspector
- 显示所有动画细节
- 可以实时查看和控制参数

**可查看的信息**：
```
Transition Inspector:
├─ Clip: 当前播放的动画片段
├─ Fade Duration: 淡入时长
├─ Speed: 播放速度
├─ Time: 当前播放时间
├─ Weight: 动画权重（混合时）
├─ Normalized Time: 归一化时间（0-1）
└─ Events: 动画事件列表
```

**实时控制**：
- 可以在预览时修改 Speed、Time 等参数
- 立即看到效果变化

---

## 高级功能

### 1. 测试不同角色模型

**功能**：将任意角色模型拖入预览场景，测试动画在不同模型上的效果

**操作步骤**：

```
1. 从 Project 窗口选中一个角色 Prefab 或 Model
2. 拖拽到 Preview 场景窗口
3. 动画会自动应用到新模型上
```

**应用场景**：

```
场景1：测试通用动画
├─ 将相同动画应用到不同身材的角色
├─ 检查动画是否适配
└─ 及时发现问题

场景2：角色变体测试
├─ 玩家角色有多个皮肤/装备变体
├─ 快速测试动画在不同变体上的效果
└─ 无需逐个进入 Play Mode
```

**示例**：

```csharp
// 假设你有多个角色变体
Assets/Characters/
├─ PlayerLight.prefab   (轻装角色)
├─ PlayerHeavy.prefab   (重装角色)
└─ PlayerMage.prefab    (法师角色)

测试流程：
1. 打开 Walk 动画的 Preview
2. 拖入 PlayerLight → 查看轻装角色行走
3. 拖入 PlayerHeavy → 查看重装角色行走
4. 拖入 PlayerMage → 查看法师角色行走
5. 对比效果，调整动画或角色比例
```

---

### 2. 设置不会被序列化

**重要特性**：Preview Settings 中的配置是**临时的**，不会保存到 Transition 资源中

```
✅ 优点：
- 可以自由实验，不会影响实际配置
- 多人协作时不会产生冲突

⚠️ 注意：
- 关闭 Preview 窗口后，设置会丢失
- 如果需要保留某个配置，应该修改 Transition 本身
```

**示例**：

```
在 Preview 中测试：
├─ Previous: Walk
├─ Current: Run
└─ Next: Attack

关闭 Preview 后：
这些设置不会保存，下次打开需要重新设置
```

---

### 3. 自动查找动画

**智能功能**：Animancer 会自动尝试找到合适的前后动画

**查找逻辑**：

```
1. 查找同一角色引用的其他动画
   ├─ 检查同一脚本中的其他 Transition 字段
   └─ 检查相关联的动画资源

2. 优先选择包含 "_Idle_" 的动画
   ├─ Rifle_Idle_Aim_C ✅
   ├─ Character_Idle ✅
   └─ Walk_Idle ✅

3. 如果找不到合适的，使用空动画
```

**手动覆盖**：

如果自动选择的动画不合适，可以手动选择：

```csharp
// 在 Preview Settings 中
Previous Animation: [手动拖入 Walk.asset]
Next Animation: [手动拖入 Run.asset]
```

---

## 实战应用

### 应用1：调试动画淡入时长

**场景**：你不确定 Fade Duration 应该设置多少

**操作流程**：

```
1. 打开 Walk 动画的 Preview
2. 设置 Previous: Idle
3. 拖拽 Timeline，观察淡入效果
4. 如果淡入太慢或太快：
   ├─ 修改 Fade Duration
   ├─ 再次拖拽 Timeline 查看效果
   └─ 重复直到满意
5. 应用修改到 Transition Asset
```

**可视化过程**：

```
Fade Duration = 0.1s
Timeline: |==| 淡入太快，看起来生硬

Fade Duration = 0.5s
Timeline: |==========| 淡入太慢，反应迟钝

Fade Duration = 0.25s ✅
Timeline: |=====| 刚刚好，平滑自然
```

---

### 应用2：检查动画循环衔接

**场景**：检查循环动画（如 Walk、Run）的首尾是否平滑衔接

**操作流程**：

```
1. 打开 Walk 动画的 Preview
2. 设置 Previous: Walk (同一个动画)
3. 设置 Next: Walk (同一个动画)
4. 拖拽 Timeline 到结束位置
5. 查看动画是否能平滑循环
6. 如果有跳帧或不自然：
   └─ 调整动画片段或使用 Synchronize Children
```

---

### 应用3：对比不同动画变体

**场景**：你有多个 Walk 动画变体，需要选择最合适的

**操作流程**：

```
1. 创建 Walk_Variant1.asset
2. 打开 Preview
3. 记录当前效果
4. 关闭 Preview
5. 创建 Walk_Variant2.asset
6. 打开 Preview
7. 对比两者效果
8. 选择更合适的变体
```

**高级技巧**：

使用两个 Inspector 窗口同时预览：

```
1. 打开 Walk_Variant1 的 Preview
2. 在另一个 Inspector 窗口打开 Walk_Variant2 的 Preview
3. 同步拖拽 Timeline
4. 直接对比两个动画效果
```

---

### 应用4：测试不同角色身材

**场景**：你的游戏有瘦高型和矮胖型角色，需要确保动画适配

**操作流程**：

```
1. 打开 Jump 动画的 Preview
2. 拖入瘦高型角色模型
   ├─ 查看跳跃高度是否合适
   └─ 检查落地姿态
3. 拖入矮胖型角色模型
   ├─ 查看跳跃高度
   └─ 检查是否需要调整
4. 如果不适配：
   ├─ 调整动画的 Root Motion
   ├─ 或创建角色专属的动画变体
   └─ 再次测试
```

---

## 导航技巧

### 快捷键：Shift + D

**功能**：取消选中当前对象，返回 Preview Inspector

**使用场景**：

```
场景1：不小心点击了其他对象
├─ 当前：正在预览 Walk 动画
├─ 误操作：点击了 Hierarchy 中的其他对象
├─ 结果：Inspector 切换到其他对象
└─ 解决：按 Shift + D 返回 Preview

场景2：需要对比不同对象但保持 Preview 打开
├─ 查看其他对象的配置
└─ 按 Shift + D 快速返回 Preview
```

---

### 点击空白区域

**功能**：也可以通过点击特定窗口的空白区域返回 Preview

**可点击的窗口**：
- **Hierarchy 窗口**的空白区域
- **Project 窗口**的空白区域
- **Scene 窗口**的空白区域

**操作示例**：

```
1. 正在预览动画
2. 点击了场景中的某个 GameObject
3. Inspector 切换到该 GameObject
4. 点击 Hierarchy 的空白处
5. 自动返回 Preview Inspector
```

---

## 最佳实践

### 1. 预览前先规划

**推荐流程**：

```
1. 明确要测试的内容
   ├─ 淡入效果？
   ├─ 动画循环？
   └─ 角色适配？

2. 准备相关资源
   ├─ 前后动画
   ├─ 不同角色模型
   └─ 参考视频/图片

3. 系统化测试
   ├─ 记录问题
   └─ 逐个解决
```

---

### 2. 利用 Timeline 精确定位问题

**技巧**：

```
发现问题 → 拖拽 Timeline 找到具体时间点 → 截图记录 → 修复

示例：
├─ 动画在 0.6s 时手臂穿模
├─ 拖拽 Timeline 到 0.6s
├─ 截图保存
├─ 调整动画或角色骨骼
└─ 再次预览验证
```

---

### 3. 多角色测试工作流

**推荐流程**：

```
1. 准备角色模型列表
   ├─ 标准身材
   ├─ 极端身材（最高/最矮/最胖/最瘦）
   └─ 特殊变体

2. 批量测试
   ├─ 为每个角色拖入测试
   ├─ 记录不适配的情况
   └─ 统一调整

3. 验证修复
   └─ 再次测试所有角色
```

---

### 4. 配合 Play Mode 使用

**组合使用**：

```
Preview 阶段：
├─ 快速预览基础效果
├─ 调整 Fade Duration
└─ 确定大致配置

Play Mode 阶段：
├─ 在实际游戏环境中测试
├─ 检查与游戏逻辑的配合
└─ 最终微调
```

**优势**：
- Preview 快速迭代
- Play Mode 最终验证
- 提高整体效率

---

## 常见问题 FAQ

### Q1: Preview 窗口关闭后设置会保存吗？

**A**: 不会。Preview Settings 是临时的，不会序列化到 Transition 中。

如果需要保存某个配置，应该修改 Transition Asset 本身。

---

### Q2: 如何同时预览多个 Transition？

**A**: 可以打开多个 Inspector 窗口：

```
1. 窗口 → General → Inspector (创建新窗口)
2. 锁定第一个 Inspector (点击锁图标)
3. 在第二个 Inspector 中打开另一个 Preview
```

---

### Q3: Preview 中的动画播放不流畅怎么办？

**A**: 可能的原因：

```
1. 角色模型过于复杂
   └─ 尝试使用简化版模型

2. 场景中有其他耗性能的操作
   └─ 关闭不必要的窗口

3. Timeline 拖拽导致跳帧
   └─ 正常现象，实际 Play Mode 不会有此问题
```

---

### Q4: 可以在 Preview 中测试 Mixer 吗？

**A**: 可以！Mixer Transition 也支持 Preview：

```
LinearMixer 或 Mixer2D:
├─ 可以拖拽参数滑块
├─ 实时查看混合效果
└─ 调整阈值坐标
```

---

### Q5: Preview 支持动画事件吗？

**A**: 部分支持：

```
✅ 可以看到事件标记在 Timeline 上
✅ 可以查看事件的时间点
❌ 不会实际触发事件回调（非 Play Mode）
```

---

## 故障排除

### 问题1：Preview 窗口无法打开

**可能原因**：
- Transition 配置有误
- 缺少必要的动画资源

**解决方法**：
```
1. 检查 Transition 的 Clip 字段是否为空
2. 确认 AnimationClip 资源有效
3. 重启 Unity 编辑器
```

---

### 问题2：拖入角色模型无效

**可能原因**：
- 模型没有正确的 Animator 组件
- 模型骨骼结构不匹配

**解决方法**：
```
1. 确保模型有 Animator 组件
2. 检查 Avatar 配置是否为 Humanoid
3. 确认骨骼映射正确
```

---

### 问题3：Timeline 拖拽无响应

**可能原因**：
- Inspector 窗口失去焦点
- 动画时长为 0

**解决方法**：
```
1. 点击 Inspector 窗口重新获得焦点
2. 检查动画片段是否有效
3. 确认 Fade Duration > 0
```

---

## 反馈与支持

### 报告问题

如果遇到 Bug 或有功能建议，请通过以下渠道反馈：

1. **GitHub Issues**：https://github.com/KybernetikGames/animancer/issues
2. **帮助页面**：查看 Animancer 官方文档的 Help 页面
3. **社区论坛**：Unity 论坛或 Discord 社区

### 获取帮助

**其他联系方式**：
- 查看官方文档：https://kybernetik.com.au/animancer/docs/
- 查看示例场景：Animancer 包含的 Examples 文件夹
- 社区支持：Unity Asset Store 评论区

---

## 总结

### 核心要点

1. **Preview 是强大的可视化工具**
   - 无需 Play Mode 即可预览动画
   - 实时调整参数查看效果
   - 支持多角色测试

2. **主要功能**
   - 场景预览窗口
   - Preview Settings（前后动画配置）
   - Timeline（精确时间控制）
   - Transition Inspector（参数查看）

3. **高级特性**
   - 拖拽角色模型测试
   - 设置不会被序列化
   - 自动查找相关动画

4. **最佳实践**
   - 预览前先规划
   - 利用 Timeline 精确定位
   - 多角色测试工作流
   - 配合 Play Mode 使用

### Preview 功能速查表

| 功能 | 操作 | 用途 |
|------|------|------|
| **打开 Preview** | 点击 [▶] 图标 | 开始预览 |
| **拖拽 Timeline** | 鼠标拖拽 | 查看特定时间点 |
| **切换角色** | 拖入模型 | 测试不同角色 |
| **返回 Preview** | Shift + D | 快速导航 |
| **调整参数** | 修改 Inspector | 实时预览效果 |

---

**文档抓取日期**：2025-01-24
**原文地址**：https://kybernetik.com.au/animancer/docs/manual/transitions/previews/
**Animancer 版本**：7.0+
**适用项目**：animator-third-person-controller (ShooterTPP)
