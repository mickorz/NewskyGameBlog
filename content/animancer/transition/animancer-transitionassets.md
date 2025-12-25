---
title: "Animancer Transition Assets"
date: 2025-12-25
draft: false
---

# Animancer Transition Assets 官方文档

> 原文地址：https://kybernetik.com.au/animancer/docs/manual/transitions/assets/
> 抓取日期：2025-01-24

---

## 概述 (Overview)

**TransitionAsset** 是一个 `ScriptableObject`，它封装了**过渡配置**。可以理解为将 Transition 的配置数据保存为一个可重用的资源文件。

### 核心概念

```
TransitionAsset (ScriptableObject)
    ↓
包含 Transition 配置数据
    ↓
可以在多个脚本中引用
```

**优势**：
- ✅ **可重用性**：多个脚本可以共享同一个配置
- ✅ **集中管理**：所有动画配置统一存放
- ✅ **内存优化**：多个实例共享同一份数据
- ✅ **易于维护**：修改一处，所有引用自动更新

---

## 创建方法 (Creation Methods)

### 方法一：使用菜单功能

最常用的创建方式：

```
步骤：
1. 在 Project 窗口中右键
2. 选择 Assets → Create → Animancer → Transition Asset
3. 命名并配置
```

**示例**：
```
创建位置：Assets/Animations/Transitions/
文件名：Idle.asset
类型：Clip Transition
```

---

### 方法二：通过 Transition Library 创建

在 Transition Library 窗口中创建（Pro 版本功能）：

```
步骤：
1. 打开 Transition Library 窗口
2. 点击 "Create Transition" 按钮
3. 配置并保存为 Library 的子资源
```

**优势**：
- 自动添加到 Library 中
- 便于集中管理
- 支持批量创建

---

### 方法三：批量创建

从现有的 Animation Clips 批量创建：

```
步骤：
1. 在 Project 窗口中选中多个 Animation Clips 或 Animator Controllers
2. 右键 → Create Transition Asset
   或者
   菜单栏 → Assets → Create → Animancer → Transition Assets From Selection
3. 自动为每个选中的资源创建对应的 Transition Asset
```

**示例场景**：
```
选中以下动画片段：
├─ Rifle_Walk_F
├─ Rifle_Walk_B
├─ Rifle_Walk_L
└─ Rifle_Walk_R

批量创建后生成：
├─ WalkForward.asset
├─ WalkBackward.asset
├─ WalkLeft.asset
└─ WalkRight.asset
```

**批量创建的配置**：
- 自动使用选中的 AnimationClip
- 默认 Fade Duration：0.25s
- 默认 Speed：1
- 可以批量修改设置

---

### 方法四：通过代码创建

在编辑器脚本中动态创建：

```csharp
using UnityEngine;
using UnityEditor;
using Animancer;

public class TransitionAssetCreator
{
    [MenuItem("Tools/Create Transition Asset")]
    static void CreateTransitionAsset()
    {
        // 创建 TransitionAsset 实例
        TransitionAsset asset = ScriptableObject.CreateInstance<TransitionAsset>();

        // 配置 Transition
        ClipTransition transition = new ClipTransition();
        transition.Clip = /* 你的 AnimationClip */;
        transition.FadeDuration = 0.25f;
        transition.Speed = 1f;

        // 保存为资源文件
        string path = "Assets/Animations/NewTransition.asset";
        AssetDatabase.CreateAsset(asset, path);
        AssetDatabase.SaveAssets();

        Debug.Log($"创建 Transition Asset: {path}");
    }
}
```

**高级示例（批量创建）**：

```csharp
using UnityEngine;
using UnityEditor;
using Animancer;
using System.IO;

public class BatchTransitionCreator
{
    [MenuItem("Tools/Batch Create Transitions")]
    static void BatchCreateTransitions()
    {
        // 获取选中的所有 AnimationClip
        AnimationClip[] clips = Selection.GetFiltered<AnimationClip>(SelectionMode.Assets);

        if (clips.Length == 0)
        {
            Debug.LogWarning("请先选中 AnimationClip");
            return;
        }

        // 创建保存目录
        string outputFolder = "Assets/Animations/Transitions";
        if (!AssetDatabase.IsValidFolder(outputFolder))
        {
            Directory.CreateDirectory(outputFolder);
        }

        foreach (AnimationClip clip in clips)
        {
            // 创建 TransitionAsset
            TransitionAsset asset = ScriptableObject.CreateInstance<TransitionAsset>();

            // 配置 ClipTransition
            ClipTransition transition = new ClipTransition
            {
                Clip = clip,
                FadeDuration = 0.25f,
                Speed = 1f
            };

            // 保存
            string assetPath = $"{outputFolder}/{clip.name}.asset";
            AssetDatabase.CreateAsset(asset, assetPath);

            Debug.Log($"创建: {assetPath}");
        }

        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh();

        Debug.Log($"批量创建完成！共创建 {clips.Length} 个 Transition Assets");
    }
}
```

---

## 使用方法对比 (Usage Comparison)

### 方式一：内联 Transitions (Inline Transitions)

**定义**：使用 `[SerializeReference]` 直接在脚本中序列化 Transition

**代码示例**：

```csharp
using Animancer;
using UnityEngine;

public class InlineTransitionExample : MonoBehaviour
{
    [SerializeField]
    private AnimancerComponent _Animancer;

    // 内联 Transition，直接在 Inspector 中配置
    [SerializeReference]
    private ITransition _IdleAnimation;

    [SerializeReference]
    private ITransition _WalkAnimation;

    void Update()
    {
        if (Input.GetKey(KeyCode.W))
        {
            _Animancer.Play(_WalkAnimation);
        }
        else
        {
            _Animancer.Play(_IdleAnimation);
        }
    }
}
```

**Inspector 中的显示**：
```
Inline Transition Example (Script)
├─ Animancer: [AnimancerComponent]
├─ Idle Animation:
│  ├─ Type: [下拉选择] ClipTransition
│  ├─ Clip: Rifle_Idle
│  ├─ Fade Duration: 0.25
│  └─ Speed: 1
└─ Walk Animation:
   ├─ Type: [下拉选择] ClipTransition
   ├─ Clip: Rifle_Walk_F
   ├─ Fade Duration: 0.25
   └─ Speed: 1
```

**特点**：
- ✅ 配置直接在脚本中，无需创建单独文件
- ✅ 设置简单直接
- ❌ 无法在多个脚本间共享
- ❌ 每个脚本都有独立的配置副本

---

### 方式二：基于资源的方式 (Asset-based Approach)

**定义**：使用 `[SerializeField]` 引用独立的 TransitionAsset 文件

**代码示例**：

```csharp
using Animancer;
using UnityEngine;

public class AssetBasedTransitionExample : MonoBehaviour
{
    [SerializeField]
    private AnimancerComponent _Animancer;

    // 引用外部的 TransitionAsset
    [SerializeField]
    private TransitionAsset _IdleAnimation;

    [SerializeField]
    private TransitionAsset _WalkAnimation;

    void Update()
    {
        if (Input.GetKey(KeyCode.W))
        {
            _Animancer.Play(_WalkAnimation);
        }
        else
        {
            _Animancer.Play(_IdleAnimation);
        }
    }
}
```

**Inspector 中的显示**：
```
Asset Based Transition Example (Script)
├─ Animancer: [AnimancerComponent]
├─ Idle Animation: [拖入 Idle.asset]
└─ Walk Animation: [拖入 WalkForward.asset]
```

**文件结构**：
```
Assets/
├─ Scripts/
│  └─ AssetBasedTransitionExample.cs
└─ Animations/
   └─ Transitions/
      ├─ Idle.asset
      └─ WalkForward.asset
```

**特点**：
- ✅ 可以在多个脚本间共享同一配置
- ✅ 集中管理，易于维护
- ✅ 内存优化（多个实例共享数据）
- ❌ 需要先创建资源文件
- ❌ 引用关系需要手动拖入

---

### 对比表格

| 特性 | 内联 Transitions | TransitionAssets |
|------|-----------------|------------------|
| **创建难度** | ⭐ 简单 | ⭐⭐ 需要创建文件 |
| **配置位置** | Inspector 中 | 独立的 .asset 文件 |
| **可重用性** | ❌ 不可重用 | ✅ 高度可重用 |
| **内存使用** | 每个脚本独立副本 | 多个脚本共享 |
| **维护难度** | ⭐⭐ 需要分别修改 | ⭐ 修改一处即可 |
| **适合场景** | 单一脚本使用 | 多脚本共享 |
| **项目规模** | 小型/原型 | 中大型项目 |

---

## 何时使用 Transition Assets (When to Use)

### ✅ 推荐使用 TransitionAsset 的场景

#### 1. **多个角色共享相同的动画配置**

**场景**：你有多个敌人类型，它们使用相同的动画资源

```csharp
// Enemy1.cs
public class Enemy1 : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private TransitionAsset _WalkAnimation; // 共享

    void Update()
    {
        _Animancer.Play(_WalkAnimation);
    }
}

// Enemy2.cs
public class Enemy2 : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private TransitionAsset _WalkAnimation; // 相同的资源

    void Update()
    {
        _Animancer.Play(_WalkAnimation);
    }
}
```

**好处**：
- 修改 `_WalkAnimation.asset` 会同时影响所有敌人
- 内存中只有一份配置数据
- 维护成本低

---

#### 2. **需要集中定义动画**

**场景**：团队协作，美术和程序分工明确

```
项目结构：
Assets/
├─ Animations/
│  └─ Transitions/
│     ├─ Player/
│     │  ├─ Idle.asset        ← 美术配置
│     │  ├─ Walk.asset        ← 美术配置
│     │  └─ Run.asset         ← 美术配置
│     └─ Enemy/
│        ├─ Idle.asset
│        └─ Patrol.asset
└─ Scripts/
   └─ PlayerController.cs     ← 程序员引用
```

**好处**：
- 美术可以独立调整动画配置
- 程序员只需引用，不需要了解细节
- 分工明确，提高效率

---

#### 3. **使用 Transition Libraries（Pro 功能）**

**场景**：需要管理大量动画，并设置动画间的过渡规则

```csharp
// 必须使用 TransitionAsset 才能在 Library 中管理
public class CharacterAnimations : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    // 这些 TransitionAsset 都在 Transition Library 中管理
    [SerializeField] private TransitionAsset _Idle;
    [SerializeField] private TransitionAsset _Walk;
    [SerializeField] private TransitionAsset _Run;
    [SerializeField] private TransitionAsset _Attack;

    void Update()
    {
        // Library 会自动处理过渡时长等细节
        if (Input.GetKey(KeyCode.W))
            _Animancer.Play(_Run);
        else
            _Animancer.Play(_Idle);
    }
}
```

**Library 的优势**：
- 自动管理动画间的过渡时长
- 可视化编辑过渡规则
- 支持别名系统

---

#### 4. **内存优化场景**

**场景**：大量相同类型的实体（如 100 个士兵）

```csharp
// Soldier.cs
public class Soldier : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    // 100 个士兵共享同一个 TransitionAsset
    [SerializeField] private TransitionAsset _MarchAnimation;

    void Start()
    {
        _Animancer.Play(_MarchAnimation);
    }
}
```

**内存对比**：
```
内联方式：
100 个士兵 × 每个独立配置 = 浪费内存

TransitionAsset 方式：
100 个士兵 → 共享 1 个配置 = 内存优化
```

---

### ❌ 不推荐使用 TransitionAsset 的场景

#### 1. **动画配置仅在单一脚本中使用**

```csharp
// 这种情况下，内联更简单
public class UniqueCharacter : MonoBehaviour
{
    [SerializeReference] private ITransition _UniqueAnimation; // 内联即可
}
```

---

#### 2. **快速原型开发**

在原型阶段，内联方式更快捷，无需创建额外文件。

---

#### 3. **动画配置需要频繁调整**

如果配置经常变化且不需要共享，内联方式更方便调试。

---

## 实战示例

### 示例1：多角色共享动画系统

**场景**：敌人和 NPC 共享基础动画

```csharp
using Animancer;
using UnityEngine;

public class SharedAnimationCharacter : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    // 共享的基础动画
    [SerializeField] private TransitionAsset _Idle;
    [SerializeField] private TransitionAsset _Walk;
    [SerializeField] private TransitionAsset _Run;

    protected virtual void Update()
    {
        float speed = GetMovementSpeed();

        if (speed < 0.1f)
            _Animancer.Play(_Idle);
        else if (speed < 3f)
            _Animancer.Play(_Walk);
        else
            _Animancer.Play(_Run);
    }

    protected virtual float GetMovementSpeed()
    {
        return 0f; // 由子类实现
    }
}

// 敌人类
public class Enemy : SharedAnimationCharacter
{
    protected override float GetMovementSpeed()
    {
        return /* 敌人的移动速度 */ 2f;
    }
}

// NPC 类
public class NPC : SharedAnimationCharacter
{
    protected override float GetMovementSpeed()
    {
        return /* NPC 的移动速度 */ 1.5f;
    }
}
```

**文件结构**：
```
Assets/
├─ Animations/
│  └─ Transitions/
│     └─ Shared/
│        ├─ Idle.asset       ← 所有角色共享
│        ├─ Walk.asset       ← 所有角色共享
│        └─ Run.asset        ← 所有角色共享
└─ Scripts/
   ├─ SharedAnimationCharacter.cs
   ├─ Enemy.cs
   └─ NPC.cs
```

---

### 示例2：动画配置管理器

**场景**：集中管理所有角色的动画配置

```csharp
using Animancer;
using UnityEngine;

[CreateAssetMenu(menuName = "Game/Animation Config")]
public class AnimationConfig : ScriptableObject
{
    [Header("移动动画")]
    public TransitionAsset Idle;
    public TransitionAsset Walk;
    public TransitionAsset Run;
    public TransitionAsset Sprint;

    [Header("战斗动画")]
    public TransitionAsset Attack1;
    public TransitionAsset Attack2;
    public TransitionAsset Attack3;

    [Header("受击动画")]
    public TransitionAsset HitLight;
    public TransitionAsset HitHeavy;
    public TransitionAsset Death;
}

// 使用示例
public class Player : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;
    [SerializeField] private AnimationConfig _AnimConfig;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            _Animancer.Play(_AnimConfig.Attack1);
        }
    }
}
```

**好处**：
- 所有动画配置集中在一个 ScriptableObject 中
- 易于维护和查找
- 支持创建多个配置（如玩家配置、敌人配置）

---

## 最佳实践

### 1. **文件组织结构**

推荐的目录结构：

```
Assets/
└─ Animations/
   └─ Transitions/
      ├─ Player/
      │  ├─ Movement/
      │  │  ├─ Idle.asset
      │  │  ├─ Walk.asset
      │  │  └─ Run.asset
      │  ├─ Combat/
      │  │  ├─ Attack1.asset
      │  │  └─ Attack2.asset
      │  └─ Special/
      │     └─ Death.asset
      ├─ Enemy/
      │  └─ ...
      └─ Shared/
         └─ CommonAnimations/
```

**命名规范**：
- 清晰描述用途：`PlayerIdle.asset` 而不是 `Anim1.asset`
- 包含状态信息：`WalkForward.asset`、`WalkBackward.asset`
- 使用前缀区分类型：`Player_`, `Enemy_`, `NPC_`

---

### 2. **创建时机**

**何时创建 TransitionAsset**：
- ✅ 项目初期规划好动画列表后立即创建
- ✅ 发现多处需要相同配置时立即重构
- ✅ 准备使用 Transition Library 之前

**何时使用内联**：
- ✅ 原型开发阶段
- ✅ 确认只在一个脚本中使用
- ✅ 配置频繁变化的测试动画

---

### 3. **版本控制**

**.gitignore 配置**：
```gitignore
# 不要忽略 TransitionAsset
# *.asset  ← 不要这样做

# 可以忽略自动生成的 meta 文件（如果需要）
# *.meta
```

**团队协作**：
- TransitionAsset 应该提交到版本控制
- 避免多人同时修改同一个 Asset
- 使用描述性的提交信息

---

### 4. **性能优化**

**预加载常用动画**：
```csharp
public class AnimationPreloader : MonoBehaviour
{
    [SerializeField] private TransitionAsset[] _CommonAnimations;

    void Awake()
    {
        // 预加载，避免运行时卡顿
        foreach (var transition in _CommonAnimations)
        {
            if (transition != null)
            {
                // 预加载逻辑
            }
        }
    }
}
```

---

## 常见问题 FAQ

### Q1: 内联 Transitions 和 TransitionAsset 可以混用吗？

**A**: 可以！根据实际需求选择：

```csharp
public class MixedExample : MonoBehaviour
{
    [SerializeField] private AnimancerComponent _Animancer;

    // 共享的动画使用 Asset
    [SerializeField] private TransitionAsset _SharedWalk;

    // 角色特有的动画使用内联
    [SerializeReference] private ITransition _UniqueSkill;

    void Update()
    {
        if (Input.GetKey(KeyCode.W))
            _Animancer.Play(_SharedWalk);      // Asset
        else if (Input.GetKeyDown(KeyCode.E))
            _Animancer.Play(_UniqueSkill);     // Inline
    }
}
```

---

### Q2: 修改 TransitionAsset 会影响所有引用它的地方吗？

**A**: 是的！这是 TransitionAsset 的核心优势：

```
修改 Idle.asset 的 Fade Duration 从 0.25 → 0.5
    ↓
所有引用 Idle.asset 的脚本自动生效
```

---

### Q3: 如何批量修改 TransitionAsset 的设置？

**A**: 使用编辑器脚本：

```csharp
[MenuItem("Tools/Batch Update Fade Duration")]
static void BatchUpdateFadeDuration()
{
    string[] guids = AssetDatabase.FindAssets("t:TransitionAsset");

    foreach (string guid in guids)
    {
        string path = AssetDatabase.GUIDToAssetPath(guid);
        TransitionAsset asset = AssetDatabase.LoadAssetAtPath<TransitionAsset>(path);

        if (asset != null)
        {
            // 修改 Fade Duration
            // asset.FadeDuration = 0.5f; // 需要访问内部 Transition
            EditorUtility.SetDirty(asset);
        }
    }

    AssetDatabase.SaveAssets();
}
```

---

### Q4: TransitionAsset 可以嵌套吗？

**A**: TransitionAsset 本身不支持嵌套，但可以通过其他方式实现类似功能：

```csharp
// 使用 ClipTransitionSequence
[SerializeField] private ClipTransitionSequence _ComboAttack;
// 其中包含多个 Transition 配置
```

---

### Q5: 删除 TransitionAsset 会导致引用丢失吗？

**A**: 是的！删除前请确认：

1. 使用 "Find References In Scene" 查找所有引用
2. 考虑重命名而不是删除
3. 做好版本控制备份

---

## 总结

### 核心要点

1. **TransitionAsset 是可重用的配置容器**
   - 封装 Transition 数据
   - 可在多个脚本间共享

2. **四种创建方法**
   - 菜单创建
   - Library 创建
   - 批量创建
   - 代码创建

3. **两种使用方式**
   - 内联：简单快捷，适合单一使用
   - Asset：可重用，适合共享场景

4. **何时使用 Asset**
   - 多角色共享配置
   - 集中管理动画
   - 使用 Transition Library
   - 内存优化需求

### 选择指南

```
是否需要在多个地方使用相同配置？
├─ 是 → 使用 TransitionAsset
└─ 否 → 使用内联 Transition
    ├─ 但未来可能需要共享？
    │  ├─ 是 → 提前创建 Asset
    │  └─ 否 → 保持内联
```

---

**文档抓取日期**：2025-01-24
**原文地址**：https://kybernetik.com.au/animancer/docs/manual/transitions/assets/
**Animancer 版本**：7.0+
**适用项目**：animator-third-person-controller (ShooterTPP)
