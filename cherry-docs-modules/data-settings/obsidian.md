---
description: 数据设置→Obsidian配置
icon: gem
---

# Obsidian 配置教程

Cherry Studio 支持与 Obsidian 联动，将完整对话或单条对话导出到 Obsidian 库中。

{% hint style="warning" %}
该过程无需安装额外的 Obsidian 插件。但由于 Cherry Studio 导入到 Obsidian 采用的原理与 Obsidian Web Clipper 类似，因此建议用户最好将 Obsidian 升级至最新版本（当前 Obsidian 版本至少应大于 **1.7.2**），以免[如果对话过长造成导入失败](https://github.com/obsidianmd/obsidian-clipper/releases/tag/0.7.0)。
{% endhint %}

## 最新教程

{% hint style="info" %}
相比旧版导出到 Obsidian，新版导出到 Obsidian 功能可以自动选择库路径，不再需要手动输入库名、文件夹名。
{% endhint %}

### 第一步：配置 Cherry Studio

打开 Cherry Studio &#x7684;_&#x8BBE;置_ →  _数据设置_ → _Obsidian 配&#x7F6E;_&#x83DC;单，下拉框中会自动出现在本机打开过的 Obsidian 库名，选择你的目标 Obsidian 库：

<figure><img src="../.gitbook/assets/image (142).png" alt=""><figcaption></figcaption></figure>

### 第二步：导出对话

#### 导出完整对话

回到 Cherry Studio 的对话界面，右键点击对话，选&#x62E9;_&#x5BFC;出_，点&#x51FB;_&#x5BFC;出到 Obsidian_：

<figure><img src="../.gitbook/assets/image (143).png" alt=""><figcaption></figcaption></figure>

此时会弹出一个窗口，用于调整这条导出到 Obsidian 中的对话笔记的 **Properties（属性）、**&#x6240;放置在Obsidian的**文件夹位置**以及导出到 Obsidian 中的**处理方式：**

* **保管库**：点击下拉菜单可以选择其他 Obsidian 库
* **路径**：点击下拉菜单可以选择存放导出对话笔记的文件夹
* 作为 Obsidian 笔记属性（Properties）：
  * 标签（tags）
  * 创建时间（created）
  * 来源（source）
* 导出到 Obsidian 中的**处理方式**有以下三种可选：
* 导出到 Obsidian 中的**处理方式**有以下三种可选：
  * **新建（如果存在就覆盖）**：在**路径**处填写的`文件夹` 里新建一篇对话笔记，如果存在同名笔记则会覆盖旧笔记
  * **前置**：在已存在同名笔记的情况下，将选中的对话内容导出添加到该笔记的开头
  * **追加**：在已存在同名笔记的情况下，将选中的对话内容导出添加到该笔记的末尾

{% hint style="info" %}
只有第一种方式会附带 Properties（属性），后两种方式不会附带 Properties（属性）。
{% endhint %}

<figure><img src="../.gitbook/assets/image (144).png" alt=""><figcaption><p>配置笔记属性</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (145).png" alt=""><figcaption><p>选择路径</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (146).png" alt=""><figcaption><p>选择处理方式</p></figcaption></figure>

选择完所有选项后，点击确定即可导出完整对话到对应的 Obsidian 库的对应文件夹。

#### 导出单条对话

对于单条对话的导出，则点击对话下方&#x7684;_&#x4E09;条杠菜单_，选&#x62E9;_&#x5BFC;出_，点&#x51FB;_&#x5BFC;出到 Obsidian_：

<figure><img src="../.gitbook/assets/image (147).png" alt=""><figcaption><p>导出单条对话</p></figcaption></figure>

之后也会弹出与导出完整对话时一样的窗口，要求你配置**笔记属性**与**笔记的处理方式**，一样按照[上方的教程](obsidian.md#dao-chu-wan-zheng-dui-hua)完成即可。

### 导出成功

🎉 到这里，恭喜你完成了 Cherry Studio 联动 Obsidian 的所有配置，并完整地将导出流程走了一遍，enjoy yourselves!

<figure><img src="../.gitbook/assets/image (140).png" alt=""><figcaption><p>导出到 Obsidian</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (139).png" alt=""><figcaption><p>查看导出结果</p></figcaption></figure>



***

## 旧教程（适用于Cherry Studio\<v1.1.13）

### 第一步：准备 Obsidian

打开 Obsidian 库，创建一个用于保存导出对话的`文件夹`（图中以 Cherry Studio 文件夹为例）：

<figure><img src="../.gitbook/assets/image (127).png" alt=""><figcaption></figcaption></figure>

注意记住左下角框出来的文字，这里是你的`保管库`名。

### 第二步：配置 Cherry Studio

在 Cherry Studio &#x7684;_&#x8BBE;置_ →  _数据设置_ → _Obsidian 配&#x7F6E;_&#x83DC;单中，输入在[第一步](obsidian.md#di-yi-bu)中获取到的`保管库`名与`文件夹`名：

<figure><img src="../.gitbook/assets/image (129).png" alt=""><figcaption></figcaption></figure>

`全局标签`处是可选的，可设定所有对话导出后在 Obsidian 中的标签，按需填写。

### 第三步：导出对话

#### 导出完整对话

回到 Cherry Studio 的对话界面，右键点击对话，选&#x62E9;_&#x5BFC;出_，点&#x51FB;_&#x5BFC;出到 Obsidian_。

<figure><img src="../.gitbook/assets/image (138).png" alt=""><figcaption><p>导出完整对话</p></figcaption></figure>

此时会弹出一个窗口，用于调整这条导出到 Obsidian 中的对话笔记的 **Properties（属性）**，以及导出到 Obsidian 中的**处理方式**。导出到 Obsidian 中的**处理方式**有以下三种可选：

* **新建（如果存在就覆盖）**：在[第二步](obsidian.md#di-er-bu)中填写的`文件夹` 里新建一篇对话笔记，如果存在同名笔记则会覆盖旧笔记
* **前置**：在已存在同名笔记的情况下，将选中的对话内容导出添加到该笔记的开头
* **追加**：在已存在同名笔记的情况下，将选中的对话内容导出添加到该笔记的末尾

<figure><img src="../.gitbook/assets/image (137).png" alt=""><figcaption><p>配置笔记属性</p></figcaption></figure>

{% hint style="info" %}
只有第一种方式会附带 Properties（属性），后两种方式不会附带 Properties（属性）。
{% endhint %}

#### 导出单条对话

对于单条对话的导出，则点击对话下方&#x7684;_&#x4E09;条杠菜单_，选&#x62E9;_&#x5BFC;出_，点&#x51FB;_&#x5BFC;出到 Obsidian_。

<figure><img src="../.gitbook/assets/image (141).png" alt=""><figcaption><p>导出单条对话</p></figcaption></figure>

之后也会弹出与导出完整对话时一样的窗口，要求你配置**笔记属性**与**笔记的处理方式**，一样按照[上方的教程](obsidian.md#dao-chu-wan-zheng-dui-hua)完成即可。

### 导出成功

🎉 到这里，恭喜你完成了 Cherry Studio 联动 Obsidian 的所有配置，并完整地将导出流程走了一遍，enjoy yourselves!

<figure><img src="../.gitbook/assets/image (140).png" alt=""><figcaption><p>导出到 Obsidian</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (139).png" alt=""><figcaption><p>查看导出结果</p></figcaption></figure>
