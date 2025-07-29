---
description: cherry studio使用「火山引擎」接入deepseekR1联网功能，喂饭教程。
hidden: true
icon: globe-pointer
---

# 火山引擎接入联网

### 1、登陆/注册 「火山引擎」 账号 <a href="#rclz7" id="rclz7"></a>

访问官网：[https://www.volcengine.com/](https://www.volcengine.com/)

<figure><img src="../.gitbook/assets/image (51).png" alt=""><figcaption><p>火山引擎官网</p></figcaption></figure>

### 2、创建 「可以联网的」 「我的应用」 <a href="#gvzaa" id="gvzaa"></a>

2.1、 登陆火山引擎，进入「火山方舟」页面，传送门：[https://console.volcengine.com/ark](https://console.volcengine.com/ark)

2.2、 **依次点击：**<mark style="color:red;">**「我的应用」 - 「创建应用」 - 「零代码」 - 「单聊」**</mark> &#x20;

<figure><img src="../.gitbook/assets/image (53).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (54).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (71).png" alt=""><figcaption></figcaption></figure>

### 3、填写信息并发布应用 <a href="#zzdfe" id="zzdfe"></a>

**应用名称**：按照要求随便起个名字即可。（带<mark style="color:red;">**\*必填**</mark>，其他可以不写）

<mark style="color:red;">**关键是：联网插件要点开（需要先开通）**</mark>

<figure><img src="../.gitbook/assets/image (56).png" alt=""><figcaption></figcaption></figure>

#### 3.1、 开通联网插件功能（注意费用和免费次数） <a href="#mwn38" id="mwn38"></a>

<figure><img src="../.gitbook/assets/image (57).png" alt=""><figcaption><p>点击立即购买，一步步执行到显示下面的界面，说明开通成功了。</p></figcaption></figure>

<figure><img src="../.gitbook/assets/image (58).png" alt=""><figcaption><p>注意状态，至此开通成功</p></figcaption></figure>

然后返回刚才的「填写应用信息」界面，继续操作。

<figure><img src="../.gitbook/assets/image (59).png" alt=""><figcaption></figcaption></figure>

#### 3.2、联网搜索「高级配置」说明 <a href="#sp6uz" id="sp6uz"></a>

根据实际情况选择，个人建议：

* 如果想要精准控制输入输出，可以用「**自定义调用**」联网；
* 如果嫌麻烦可以不修改，使用「**自动调用**」- 默认值；
* 如果不差钱，对信息时效性要求很高，可以「**强制开启**」。

<figure><img src="../.gitbook/assets/image (60).png" alt=""><figcaption></figcaption></figure>

#### 3.3、发布应用 <a href="#fe1gf" id="fe1gf"></a>

点击右上角「发布」按钮，应用创建成功。

<figure><img src="../.gitbook/assets/image (61).png" alt=""><figcaption></figcaption></figure>

### 4、获取 API Key <a href="#jtqlu" id="jtqlu"></a>

依次点击：**「API 调用指南」-「选择 API Key 并复制」-「查看并选择」**

把 API key 先复制下来，然后我们去 cherry studio 粘贴。 （操作详情，见下面界面）

<figure><img src="../.gitbook/assets/image (62).png" alt=""><figcaption></figcaption></figure>

注意：如果没有 API key，就在弹窗右上角 - 「**创建 API Key**」，然后复制API key就行了。

<figure><img src="../.gitbook/assets/image (63).png" alt=""><figcaption></figcaption></figure>

### 5、在 cherry studio 中使用 API Key 实现联网访问 deepseek-R1 <a href="#lrefj" id="lrefj"></a>

#### 5.1、打开 cherry studio - 「设置」- 「随便写名称」-「类型为： openAI」 <a href="#dvrbv" id="dvrbv"></a>

<figure><img src="../.gitbook/assets/image (64).png" alt="" width="375"><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (65).png" alt="" width="375"><figcaption></figcaption></figure>

#### 5.2、配置 url 和 key <a href="#mt8y0" id="mt8y0"></a>

<figure><img src="../.gitbook/assets/image (66).png" alt=""><figcaption></figcaption></figure>

<mark style="color:purple;">注意，找不到地址，或者不是北京的节点，可以在这个地方找到具体的地址，注意不要忘记“/”：</mark>

<figure><img src="../.gitbook/assets/image (67).png" alt=""><figcaption></figcaption></figure>

#### 5.3、添加模型名字 <a href="#qmh3i" id="qmh3i"></a>

注意，是复制下面那个小字为模型名字，否则会报错。

<figure><img src="../.gitbook/assets/image (68).png" alt=""><figcaption></figcaption></figure>

<figure><img src="../.gitbook/assets/image (69).png" alt=""><figcaption></figcaption></figure>

### 6、 效果预览 <a href="#peb2p" id="peb2p"></a>

<figure><img src="../.gitbook/assets/image (70).png" alt=""><figcaption></figcaption></figure>

