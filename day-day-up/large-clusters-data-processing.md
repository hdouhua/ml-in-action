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

超大规模数据处理的技术发展分为三个阶段：石器时代，青铜时代，蒸汽机时代。

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

假设你的电商网站销售 10 亿件商品，已经跟踪了网站的销售记录：商品 id 和购买时间 {product_id, timestamp}，整个交易记录是 1000 亿行数据，TB 级。作为技术负责人，你会怎样设计一个系统，根据销售记录统计去年销量前 10 的商品呢？

<img src="https://static001.geekbang.org/resource/image/3e/af/3eaea261df4257f0cff4509d82f211af.png?wh=1992*638?wh=1992*638" width="35%" />

Top K 算法当数据规模变大会遇到哪些问题呢？

- 第一，内存占用。
- 第二，磁盘 I/O 等延时问题。

### 大规模分布式解决方案

在每一个计算集群（统计商品销量的集群），分别计算、统计。最后在单一机器就可以汇总结果了。

### 大规模数据处理框架的功能要求

*如果这个世界一无所有，你会设计怎样的大规模数据处理框架？你要经常做一些思维实验，试试带领一下技术的发展，而不是永远跟随别人的技术方向。*

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

## 分布式系统的其它三指标

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

>弱一致性是个很宽泛的概念，它是区别于强一致性而定义的。广义上讲，任何不是强一致的，而又有某种同步性的分布式系统，我们都可以说它是弱一致的。而最终一致性是弱一致性的一个特例，而且是最常被各种分布式系统用到的一个特例。

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

## reference

[course](https://time.geekbang.org/column/intro/100025301)