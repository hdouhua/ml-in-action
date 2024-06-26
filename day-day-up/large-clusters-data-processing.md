# 大规模数据处理

规模增长的技术思维（mindset of scaling）——必备！

常有的误区：
- 低估了数据处理的重要性。
- 低估了数据处理规模变大带来的复杂度。
- 高估了上手数据处理的难度。

学习使用一个新技术时，必须追问自己的几个问题：

>这个技术解决了哪些痛点？  
>别的技术为什么不能解决？  
>这个技术用怎样的方法解决问题？  
>采用这个技术真的是最好的方法吗？  
>如果不用这个技术，会怎样独立解决这类问题？  
>
>如果没有这些深层次的思考，就永远只是在赶技术的时髦而已，不会拥有影响他人的技术领导力。

## 数据处理技术的三个阶段

沿着时间线看一下超大规模数据处理的重要技术以及它们产生的年代：

<img src="https://static001.geekbang.org/resource/image/54/ca/54a0178e675d0054cda83b5dc89b1dca.png?wh=5000*3092" width="50%" />

超大规模数据处理的技术发展分为三个阶段：

- 石器时代

  MapReduce 诞生之前的时期。

- 青铜时代

  2003 年，MapReduce 的诞生标志了超大规模数据处理的第一次革命，而开创这段青铜时代的就是下面这篇论文《MapReduce: Simplified Data Processing on Large Clusters》。

  > MapReduce 被硅谷一线公司淘汰的“致命伤”：高昂的维护成本和无法达到用户期待的时间性能

- 蒸汽机时代

  到了 2014 年左右，Google 内部已经几乎没人写新的 MapReduce 了。

## 设计下一代数据处理技术

有向无环图（DAG）能为多个步骤的数据处理依赖关系，建立很好的模型。

在一个复杂的数据处理系统中，难的不是开发系统，而是异常处理。

站在 2008 年春夏之交来设计下一代大规模数据处理框架，一个基本的模型会是图中这样子的：

<img src="https://static001.geekbang.org/resource/image/53/2e/53aa1aad08b11e6c2db5cf8bb584572e.png?wh=4909*3085" width="40%" />

需要补充一些设计和使用大规模数据处理架构的基础知识。
深入剖析两个与这里的设计理念最接近的大数据处理框架：Apache Spark 和 Apache Beam。

## 实现大型电商热销榜

假设电商网站销售 10 亿件商品，已经跟踪了网站的销售记录：商品 id 和购买时间 {product_id, timestamp}，整个交易记录是 1000 亿行数据，TB 级。作为技术负责人，要怎样设计一个系统，根据销售记录统计去年销量前 10 的商品呢？

<img src="https://static001.geekbang.org/resource/image/3e/af/3eaea261df4257f0cff4509d82f211af.png?wh=1992*638?wh=1992*638" width="35%" />

Top K 算法当数据规模变大会遇到哪些问题呢？

- 第一，内存占用。
- 第二，磁盘 I/O 等延时问题。

### 大规模分布式解决方案

在每一个计算集群（统计商品销量的集群），分别计算、统计。最后在单一机器就可以汇总结果了。

### 大规模数据处理框架的功能要求

*如果这个世界一无所有，我会设计怎样的大规模数据处理框架？我们要经常做一些思维实验，试试带领一下技术的发展，而不是永远跟随别人的技术方向。*

两个最基本的需求是：

- 高度抽象的数据处理流程描述语言。能够用几行代码把业务逻辑描述清楚。
- 根据描述的数据处理流程，自动化的任务分配优化。

最理想情况下，作为用户，只想写两行代码：

第一行代码

```
sales_count = sale_records.Count()
```

第二行代码

```
top_k_sales = sales_count.TopK(k)
```

## 分布式系统的 SLA

SLA（Service-Level Agreement），也就是服务等级协议，指的是系统服务提供者（Provider）对客户（Customer）的一个服务承诺。这是衡量一个大型分布式系统是否“健康”的常见方法。

最常见的四个 SLA 指标：可用性、准确性、系统容量和延迟。

1. Availabilty

   可用性指的是系统服务能正常运行所占的时间百分比。

   服务中断（Service Outage）的时间：

   - 对于许多系统而言，4 个 9 的可用性（99.99％ Availability，或每年约 50 分钟的系统中断时间）即可以被认为是高可用性（High availability）。
   - 3 个 9 99.9% Availability 指的是一天当中系统服务将会有大约 86 秒的服务间断期。（ 24 × 60 × 60 × 0.001 = 86.4 秒）

2. Accuracy

   准确性指的是所设计的系统服务中，是否允许某些数据是不准确的或者是丢失了的。

   很多时候，系统架构会以错误率（Error Rate）来定义这一项 SLA。

   Error Rate = 可以用导致系统产生内部错误（Internal Error）的有效请求数，除以这期间的有效请求总数。

   硅谷一线公司所搭建的架构平台的准确性 SLA：

   - Google Cloud Platform 的 SLA 中，有着这样的准确性定义：每个月系统的错误率超过 5% 的时间要少于 0.1%，以每分钟为单位来计算。
   - 而亚马逊 AWS 云计算平台有着稍微不一样的准确性定义：以每 5 分钟为单位，错误率不会超过 0.1%。

   一般来说，可以采用性能测试（Performance Test）或者是查看系统日志（Log）两种方法来评估。

3. Capacity

   系统容量指的是系统能够支持的预期负载量是多少，一般会以每秒的请求数为单位来表示。

   Twitter 发布的一项数据：Twitter 系统可以响应 30 万的 QPS 来读取 Twitter Timelines。这里 Twitter 系统给出的就是他们对于系统容量 （Capacity）的 SLA。

   怎么给自己设计的系统架构定义出准确的 QPS 呢？

   - 第一种，是使用限流（Throttling）的方式。

     假设每台服务器都定义了一个每秒最多处理 1000 个请求的 RateLimiter，有 N 台服务器，在最理想的情况下的 QPS 可以达到 1000 \* N。

   - 第二种，是在系统交付前进行性能测试（Performance Test）。

     可以使用像 Apache JMeter 又或是 LoadRunner 这类型的工具对系统进行性能测试。这类工具可以测试出系统在峰值状态下可以应对的 QPS 是多少。

     这里的影响因素可能有命中缓存（Cache Hit）。此时，得到的 QPS 可能并不是真实的 QPS。

   - 第三种，是分析系统在实际使用时产生的日志（Log）。

     系统上线使用后，可以得到日志文件。一般的日志文件会记录每个时刻产生的请求，于是，可以通过系统每天在最繁忙时刻所接收到的请求数，来计算出系统可以承载的 QPS。

     不过，这种方法不一定可以得到系统可以承载的最大 QPS。

4. Latency

   系统在收到用户的请求到响应这个请求之间的时间间隔。
   
   在定义延迟的 SLA 时，常常看到系统的 SLA 会有 p95 或者是 p99 这样的延迟声明。这里的 p 指的是 percentile，也就是百分位的意思。如果说一个系统的 p95 延迟是 1 秒的话，那就表示在 100 个请求里面有 95 个请求的响应时间会少于 1 秒，而剩下的 5 个请求响应时间会大于 1 秒。

   为了降低系统的延迟，会将数据库中内容放进缓存（Cache）中，以此来减少数据库的读取时间。但总会有 5% 或者 1% 的用户抱怨产品的用户体验太差，因此在系统运行了一段时间后，得到了一些缓存命中率（Cache Hit Ratio）的信息后，需要通过优化缓存来提升用户体验。

### 小结

定义好一个系统架构的 SLA 对于一个优秀的架构师来说是必不可少的一项技能，也是一种基本素养。特别是当系统架构在不停迭代的时候，有了一个明确的 SLA，便可以知道下一代系统架构的改进目标，以及衡量优化后的系统架构是否比上一代的系统 SLA 更加优秀。

## 分布式系统的其它指标

### 可扩展性

分布式系统的核心指标可扩展性（Scalability）。
最基本而且最流行的增加系统容量的模型有两种: 水平扩展（Horizontal Scaling）和垂直扩展（Vertical Scaling）。

传统的关系型数据库因为表与表之间的数据有关联，经常要进行 Join 操作，所有数据要存放在单机系统中，很难支持水平扩展。而 NoSQL 型的数据库天生支持水平扩展，所以这类存储系统的应用越来越广，如 BigTable、MongoDB 和 Redis 等。

### 一致性

可用性对于任何分布式系统都很重要，要想提高单机系统的可用性，最简单的办法就是增加系统中机器节点的数量。这样即使有部分机器宕机了，其他的机器还在持续工作，所以整个系统的可用性就提高了。

系统可用性提高了，但是新的问题出现了：如何保证系统中不同的机器节点在同一时间，接收到和输出的数据是一致的呢？这时就要引入一致性（Consistency）的概念。

几个在工程中常用的一致性模型：

- 强一致性（Strong Consistency）：系统中的某个数据被成功更新后，后续任何对该数据的读取操作都将得到更新后的值。所以在任意时刻，同一系统所有节点中的数据是一样的。
- 弱一致性（Weak Consistency）：系统中的某个数据被更新后，后续对该数据的读取操作可能得到更新后的值，也可能是更改前的值。但经过“不一致时间窗口”这段时间后，后续对该数据的读取都是更新后的值。
- 最终一致性（Eventual Consistency）：是弱一致性的特殊形式。存储系统保证，在没有新的更新的条件下，最终所有的访问都是最后更新的值。

在强一致性系统中，只要某个数据的值有更新，这个数据的副本都要进行同步，以保证这个更新被传播到所有备份数据库中。在这个同步进程结束之后，才允许服务器来读取这个数据。所以，强一致性一般会牺牲一部分延迟性，而且对于全局时钟的要求很高。比如，Google Cloud Spanner 就是一款具备强一致性的全球分布式企业级数据库服务。

在最终一致性系统中，无需等到数据更新被所有节点同步就可以读取。尽管不同的进程读同一数据可能会读到不同的结果，但是最终所有的更新会被按时间顺序同步到所有节点。所以，最终一致性系统支持异步读取，它的延迟比较小。比如，亚马逊云服务的 DynamoDB 就支持最终一致的数据读取。

分布式系统理论中还有很多别的一致性模型，如顺序一致性（Sequential Consistency），因果一致性（Casual Consistency）等。

>弱一致性是个很宽泛的概念，它是区别于强一致性而定义的。广义上讲，任何不是强一致的，而又有某种同步性的分布式系统，都可以说它是弱一致的。而最终一致性是弱一致性的一个特例，而且是最常被各种分布式系统用到的一个特例。

### 持久性

数据持久性（Data Durability）意味着数据一旦被成功存储就可以一直继续使用，即使系统中的节点下线、宕机或数据损坏也是如此。

想要提高持久性，数据复制是较为通用的做法。因为把同一份数据存储在不同的节点上，即使有节点无法连接，数据仍然可以被访问。

在分布式数据处理系统中，还有一个持久性概念是消息持久性。在分布式系统中，节点之间需要经常相互发送消息去同步以保证一致性。对于重要的系统而言，常常不允许任何消息的丢失。如 RabbitMQ、Kafka 等消息服务都能支持（或配置后支持）不同级别的消息送达可靠性。消息持久性包含两个方面：
1. 当消息服务的节点发生了错误，已经发送的消息仍然会在错误解决之后被处理；
2. 如果一个消息队列声明了持久性，那么即使队列在消息发送之后掉线，仍然会在重新上线之后收到这条消息。

## 批处理 vs 流处理

世界上的数据可以抽象成为两种：无边界数据（Unbounded Data）和有边界数据（Bounded Data）。

- 无边界数据是一种**不断增长**，可以说是**无限的数据集**。这种类型的数据，无法判定它们到底什么时候会停止发送。它的另一种表达叫“流数据（Streaming Data）”。

- 有边界数据是一种**有限的数据集**。这种数据更常见于已经保存好了的数据中。*有边界数据可以看作是无边界数据的一个子集。*

在处理大规模数据的时候，通常还会关心时域（Time Domain）的问题。任意数据都会有两种时域：事件时间（Event Time）和处理时间（Precessing Time）。
- 事件时间指的是一个数据实际产生的时间点。
- 处理时间指的是处理数据的系统架构实际接收到这个数据的时间点。

### 批处理

数据的批处理，可以理解为一系列相关联的任务按顺序（或并行）一个接一个地执行。批处理的输入是在一段时间内已经收集保存好的数据。每次批处理所产生的输出也可以作为下一次批处理的输入。

绝大部分情况下，批处理的输入数据都是有边界数据，同样的，输出结果也一样是有边界数据。所以在批处理中，关心的更多会是数据的事件时间。

批处理架构通常会被设计在以下这些应用场景中：

- 日志分析：日志系统是在一定时间段（日，周或年）内收集的，而日志的数据处理分析是在不同的时间内执行，以得出有关系统的一些关键性能指标。
- 计费应用程序：计费应用程序会计算出一段时间内一项服务的使用程度，并生成计费信息，例如银行在每个月末生成的信用卡还款单。
- 数据仓库：数据仓库的主要目标是根据收集好的数据事件时间，将数据信息合并为静态快照（static snapshot），并将它们聚合为每周、每月、每季度的报告等。

### 流处理

数据的流处理可以理解为系统需要接收并处理一系列连续不断变化的数据。流处理的输入数据基本上都是无边界数据。而流处理系统中是关心数据的事件时间还是处理时间，将视具体的应用场景而定。

流处理的特点应该是要足够快、低延时，以便能够处理来自各种数据源的大规模数据。流处理所需的响应时间更应该以毫秒（或微秒）来进行计算。
流处理速度如此之快的根本原因是因为它在数据到达磁盘之前就对其进行了分析。

当流处理架构拥有在一定时间间隔（毫秒）内产生逻辑上正确的结果时，这种架构可以被定义为实时处理（Real-time Processing）。
而如果一个系统架构可以接受以分钟为单位的数据处理时间延时，也可以把它定义为准实时处理（Near real-time Processing）。

流处理架构通常都会被设计在以下这些应用场景中：
- 实时监控：捕获和分析各种来源发布的数据，如传感器，新闻源，点击网页等。
- 实时商业智能：智能汽车，智能家居，智能病人护理等。
- 销售终端（POS）系统：像是股票价格的更新，允许用户实时完成付款的系统等。

在如今的开源架构生态圈中，如 Apache Kafka、Apache Flink、Apache Storm、Apache Samza 等，都是流行的流处理架构平台。

## Workflow 设计模式

举一个例子来理解数据处理流程：根据活跃在街头的美团外卖电动车的数量来预测美团的股价。流程如下，整个数据处理流程又会需要至少 10 个处理模块，每一个处理模块的输出结果都将会成为下一个处理模块的输入数据：

<img src="https://static001.geekbang.org/resource/image/bb/a7/bb5bac6c66bca6c3d16172046a84e5a7.jpg?wh=1898*1226" width="50%" />

常用的四种工作流系统的设计模式

### 复制模式（Copier Pattern）

复制模式通常是将单个数据处理模块中的数据，完整地复制到两个或更多的数据处理模块中，然后再由不同的数据处理模块进行处理。

<img src="https://static001.geekbang.org/resource/image/5f/3b/5fa7f641e5d2fd2ca79644c3e3a04f3b.jpg?wh=1752*1100" width="50%" />

应用场景：对同一个数据集采取多种不同的数据处理转换，可以优先考虑采用复制模式。

举例：YouTube 视频平台中，视频平台很多时候都会提供不同分辨率的视频。4K 或 1080P 的视频可以提供给网络带宽很高的用户。而在网络很慢的情况下，视频平台系统会自动转换成低分辨率格式的视频，像 360P 这样的视频给用户。

### 过滤模式（Filter Pattern）

过滤模式的作用是过滤掉不符合特定条件的数据。在数据集通过了这个数据处理模块后，数据集会缩减到只剩下符合条件的数据。

<img src="https://static001.geekbang.org/resource/image/2e/6c/2ed81b389597b6de86300ef19f95bb6c.jpg?wh=1164*690" width="50%" />

应用场景：针对一个数据集中某些特定的数据采取数据处理时，可以优先考虑采用过滤模式。

举例：在商城会员系统中，系统通常会根据用户的消费次数、用户消费金额还有用户的注册时间，将用户划分成不同的等级。假设现在商城有五星会员（Five-stars Membership）、金牌会员（Golden Membership）和钻石会员（Diamond Membership）。而系统现在打算通过邮件，只针对身份是钻石会员的用户发出钻石会员活动邀请。

### 分离模式（Splitter Pattern）

如果在处理数据集时并不想丢弃里面的任何数据，而是想把数据分类为不同的类别来进行处理时，就需要用到分离模式来处理数据。

<img src="https://static001.geekbang.org/resource/image/f2/93/f2e872adf258737f35a9121cf89fad93.jpg?wh=1490*798" width="50%" />

应用场景：分离模式并不会过滤任何数据，只是将原来的数据集分组。*同样的数据是可以被划分到不同的数据处理模块。*

举例：还是商城会员系统，系统现在打算通过邮件，针对全部的会员用户发出与他们身份相符的不同活动的邀请。也就是按照会员等级分组，然后发送相应的活动内容。

### 合并模式（Joiner Pattern）

合并模式会将多个不同的数据集转换集中到一起，成为一个总数据集，然后将这个总的数据集放在一个工作流中进行处理。

<img src="https://static001.geekbang.org/resource/image/a4/4e/a4827ed21e8af58d30371e8ecf1e744e.jpg?wh=1404*970" width="50%" />

举例：还是预测美团的股价的例子，数据接入处理模块里，输入数据有自己团队在街道上拍摄到的美团外卖电动车图片和第三方公司提供的美团外卖电动车图片。先整合所有数据，然后进行其它数据处理。

## 发布/订阅模式

在处理大规模数据中十分流行的一种设计模式：发布 / 订阅模式（Publish/Subscribe Pattern），也称为 Pub/Sub。

### 消息

在分布式架构里，架构中的各个组件（Component）需要相互联系沟通。组件可以是后台的数据库，可以是前端的浏览器，也可以是服务终端（Service Endpoint）。各个组件间就是通过发送消息互相通讯的。

### 消息队列

消息队列在发布 / 订阅模式中起的是一个 *持久化缓冲（Durable Buffer）* 的作用。
消息的发送方可以发送任意消息至这个消息队列中，消息队列在接收到消息之后会将消息保存好，直到消息的接收方确认已经从这个队列拿到了这个消息，才会将这条消息从消息队列中删除。

### 发布 / 订阅模式

发布 / 订阅模式指的是消息的发送方可以将消息异步地发送给一个系统中不同组件，而无需知道接收方是谁。在发布 / 订阅模式中，发送方被称为发布者（Publisher），接收方则被称作订阅者（Subscriber）。

- 发布者将消息发送到消息队列中，订阅者可以从消息队列里取出自己感兴趣的消息。
- 在发布 / 订阅模式里，可以有任意多个发布者发送消息，也可以有任意多个订阅者接收消息。

<u>只是简单地在消息发送方和消息接收方中间多加了一个消息队列 —— 如此简单的架构，为何会如此流行？</u>下面用一个实例来解释。

假设，开发一个移动支付 App ，开始公司里有支付开发团队和反欺诈团队。每次有交易发生的时候，反欺诈团队需要知道交易的金额、地点、时间这些数据，以便实时分析这次的交易是否存在欺诈行为。

反欺诈团队如何获取交易数据？一种可能的方式是反欺诈团队将自己需要的数据格式定义在 API 中告诉支付团队，每次有交易产生的时候，支付系统要调用欺诈预防系统 API 发出通知。

一段时间过后，公司希望和商家一起合作推动一项优惠活动，不同的商家会有不同的优惠。公司希望能够精准投放优惠活动的广告给感兴趣的用户，所以又成立了一个新部门广告推荐组。而广告推荐组也需要从支付开发团队里获取交易数据。

这个时候可能的选择：一种选择是批处理方式，另一种选择是发布 / 订阅模式。

批处理方式会从数据库中一次性读取全部用户的交易数据来进行推荐分析。这需要开放支付交易数据库的权限给广告推荐组，推荐组每次大量读取数据时，可能也会造成数据库性能下降。同时，考虑到广告推荐组可能有一些其它的需求，需要按照之前反欺诈团队的做法，每次有交易产生的时候要调用广告推荐组 API 发出通知。

整个系统运行模式如下：

<img src="https://static001.geekbang.org/resource/image/5d/39/5de2522f2f436141dbf802ff2a19a439.jpg?wh=617*361" width="50%" /><br/>

到此，应该明白了。每一次有一个新的系统想从支付团队里读取数据的话，都要双方开会讨论，定义一个新的 API，然后修改支付团队现有的系统，将 API 加入系统中。另外这些 API 通常都是同步调用的，过多的 API 调用会让系统的延迟越来越大。
这种设计模式被称作观察者模式（Observer Pattern），系统中的各个组件紧耦合（Tightly Coupled）。

若采用发布 / 订阅模式来重新设计：作为消息发布者的支付团队无需过多考虑以后有多少其它的团队需要读取交易数据，只需要设计好自己提供的数据内容与格式，在每次交易发生时发送消息进消息队列中即可。任何对这些数据感兴趣的团队只需要从消息队列中自行读取便可。

整个系统就如下图所示：

<img src="https://static001.geekbang.org/resource/image/f2/00/f2f3daa13f6db54f96c1c18f61a93200.jpg?wh=617*348" width="50%" /><br/>

### 优缺点

几个优点：
- 松耦合（Loose Coupling）：消息的发布者和消息的订阅者在开发的时候完全不需要事先知道对方的存在，可以独立地进行开发。
- 高伸缩性（High Scalability）：发布 / 订阅模式中的消息队列可以独立的作为一个数据存储中心存在。在分布式环境中，消息队列可以扩展至上千个服务器中。
- 系统组件间通信更加简洁：因为不需要为每一个消息的订阅者准备专门的消息格式，只要知道了消息队列中保存消息的格式，发布者就可以按照这个格式发送消息，订阅者也只需要按照这个格式接收消息。

自身的缺点：
例如，在整个数据模式中，不能保证发布者发送的数据一定会送达订阅者。如果要保证数据一定送达的话，需要开发者自己实现响应机制。

在硅谷，很多大型云平台都是运用这个发布 / 订阅数据处理模式。例如，Google Cloud Pub/Sub 平台，Amazon Simple Notification Service（SNS）。被 Linkedin、Uber 等硅谷大厂所广泛使用的开源平台 Apache Kafka 也是搭建在发布 / 订阅数据处理模式之上的。连 Redis 也支持原生的发布 / 订阅模式。

Apache Kafka 作为一个被在硅谷大厂与独角兽广泛使用的开源平台，简单介绍一下：
- 消息的发送方被称为 Producer，消息的接收方被称为 Consumer，而消息队列被称为 Topic。
- Apache Kafka 在判断消息是否被接收方接收时，利用了 Log offset 机制。
  >什么是 Log offset 机制呢？举个例子来解释：  
  >假设发送方连续发送了 5 条数据到消息队列 Topics 中，这 5 条消息被编号为 10000、10001、10002、10003 和 10004。如果接收方读取数据之后回应消息队列它接收的 Log offset 是 10000、10001 和 10003，那么消息队列就会认为接收方最多只接收了消息 10000 和 10001，剩下的消息 10002、10003 和 10004 则会继续发送给接收方，直到接收方回应接收了消息 10002、10003 和 10004。

### 适用场景

- 系统的发送方需要向大量的接收方广播消息。
- 系统中某一个组件需要与多个独立开发的组件或服务进行通信，而这些独立开发的组件或服务可以使用不同的编程语言和通信协议。
- 系统的发送方在向接收方发送消息之后无需接收方进行实时响应。
- 系统中对数据一致性的要求只需要支持数据的最终一致性（Eventual Consistency）模型。

要注意的一点是：
如果系统的发送方在向接收方发送消息之后，需要接收方进行实时响应，那么绝大多数情况下，都不要考虑使用发布 / 订阅的数据处理模式。

## CAP 定理

CAP Theorem ，在设计分布式系统架构时都会讨论到的一个定理。

>CAP 这个概念最初是由埃里克·布鲁尔博士（Dr. Eric Brewer）在 2000 年的 ACM 年度学术研讨会（[Towards Robust Distributed Systems](https://people.eecs.berkeley.edu/~brewer/cs262b-2004/PODC-keynote.pdf)）上提出的。在两年之后，塞思·吉尔伯特（Seth Gilbert）和麻省理工学院的南希·林奇教授（Nancy Ann Lynch）在他们的论文“Brewer’s conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services”中证明了这一概念。

在任意的分布式系统中，一致性（Consistency），可用性（Availability）和分区容错性（Partition-tolerance）这三种属性最多只能同时存在两个属性。

### C 属性：一致性

一致性在这里指的是线性一致性（Linearizability Consistency）。在线性一致性的保证下，所有分布式环境下的操作都像是在单机上完成的一样，

以一个具体例子来说明：

假设一个分布式的购物系统，在这个系统中，商品的存货状态（“有货状态”或者“无货状态”）分别保存在服务器 A 和服务器 B 中。在最开始的时候，服务器 A 和服务器 B 都会显示商品为有货状态。

等一段时间过后，商品卖完了，后台就必须将这两台服务器上的商品状态更新为无货状态。因为是在分布式的环境下，商品状态的更新在服务器 A 上完成了，显示为无货状态。而服务器 B 的状态因为网络延迟的原因更新还未完成，还是显示着有货状态。这时，恰好有两个用户使用着这个购物系统，先后发送了一个查询操作（Query Operation）到后台服务器中查询商品状态。假设是用户 CA 先查询的，这个查询操作被发送到了服务器 A 上面，并且成功返回了商品是无货状态的。用户 CB 在随后也对同一商品进行查询，而这个查询操作被发送到了服务器 B 上面，并且成功返回了商品是有货状态的。

对于整个系统来说，商品的系统状态应该为无货状态，而这两次成功完成的查询给出了不一致的结果，这个分布式的购物系统并不满足论文里所讲到的线性一致性。

### A 属性：可用性

可用性的概念比较简单，在这里指的是在分布式系统中，任意非故障的服务器都必须对客户的请求产生响应。
当系统满足可用性的时候，不管出现什么状况（除非所有的服务器全部崩溃），都能返回消息。也就是说，当客户端向系统发送请求，只要系统背后的服务器有一台还未崩溃，那么这个未崩溃的服务器必须最终响应客户端。

### P 属性：分区容错性

它分为两个部分，“分区”和“容错”。在一个分布式系统里，如果出现一些故障，可能会使得部分节点之间无法连通。由于这些故障节点无法联通，造成整个网络就会被分成几块区域，从而使数据分散在这些无法连通的区域中的情况，可以认为这就是发生了分区错误。

如果访问的数据只在 SeverA 中保存，当系统出现分区错误，在不能直接连接 SeverA 时，就无法获取数据。要“分区容错”，意思是即使出现这样的“错误”，系统也需要能“容忍”。也就是说，就算错误出现，系统也必须能够返回消息。

分区容错性，在这里指的是系统允许网络丢失从一个节点发送到另一个节点的任意多条消息。在现代网络通信中，节点出现故障或者网络出现丢包这样的情况是时常会发生的。如果没有了分区容错性，也就是说系统不允许这些节点间的通讯出现任何错误的话，那日常所用到的很多系统就不能再继续工作了。

### 小结

在大部分情况下，系统设计都会保留 P 属性，而在 C 和 A 中二选一。
在日常所用到的开发架构中，有哪些系统是属于 CP 系统，有哪些是 AP 系统又有哪些是 CA 系统呢？
- CP 系统：Google BigTable, HBase, MongoDB, Redis, MemCacheDB，这些存储架构都是放弃了高可用性（High Availablity）而选择 CP 属性的。
- AP 系统：Amazon Dynamo 系统以及它的衍生存储系统 Apache Cassandra 和 Voldemort 都是属于 AP 系统
- CA 系统：Apache Kafka 是一个比较典型的 CA 系统。(此处是指 Kafka Replication 不保证 P。严格来说，Kafka 放弃 P，支持 CA，是因为 Kafka 原理中当出现单个 Broke 宕机，将要出现分区的时候，直接将该 Broke 从集群中剔除，确保整个集群不会出现 P 现象)

对 CAP 要明确如下的事实:
1. 对于一个分布式系统而言，节点故障和网络故障属于常态
2. 如果出现网络故障，会造成节点分区
3. 分布式系统在存在节点分区的情况下，C 和 A 是冲突的

通过上面的事实可以推断出，如果想设计出一个 CA 系统，必须保证网络不出现分区才有可能，怎样保证网络不出现分区呢，一是单台机器，二是将所有节点放在同个数据中心中可以假定网络出现分区的概率很低。

辅助理解 CAP 的知识如下:
1. 对于分布式系统而言，最简单可以分为两种:
   - 所有节点通过都可以通过某种策略对外提供服务，是对等的
   - 所有节点通过一个 master 对外提供服务，甚至是一个单点的 master
2. 探讨系统 CAP 的前提应该是系统在能提供服务的情况下的 CAP，如果存在 master 单点，但是有很多从属 worker 的话，这时的可用性探讨需要划分为 worker 故障和 master 故障来看
3. A 就是指集群中即便挂掉几个机器但是集群对外还是正常运行，P 就是指即便机器间无法通讯了但是集群对外还是正常运行。

*CAP Theorem is like the old joke about software projects: you can have it on TIME, in BUDGET, or CORRECT. Pick any two*  
*CAP 三者互相制衡，应该是看侧重哪两个，而不是选了哪两个，不是两个 100 分剩下的一个 0 分，本质上都要兼顾的。*

## reference

[course](https://time.geekbang.org/column/intro/100025301)
