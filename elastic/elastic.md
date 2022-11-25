# elastic

* [RESTful CRUD](#restful-crud)
* [QUERY](#query)
    * [term 查询](#term-查询)
    * [match 类查询](#match-类查询)
      * [match_phrase](#match_phrase)
      * [multi_match](#multi_match)
    * [bool 查询](#bool-查询)
    * [排序](#排序)
    * [聚合](#聚合)
* [mappings](#mappings)
    * [映射定义了什么](#映射定义了什么)
    * [映射类型](#映射类型)
    * [字段的数据类型](#字段的数据类型)
    * [映射分类](#映射分类)
    * [copy_to](#copy_to)
    * [ignore_above](#ignore_above)
* [settings](#settings)
* [分析 analyze](#分析-analyze)
    * [分析器](#分析器)
      * [标准分析器 —— ES 的默认分析器](#标准分析器--es-的默认分析器)
      * [简单分析器](#简单分析器)
      * [空白分析器：whitespace analyzer](#空白分析器whitespace-analyzer)
      * [自定制一个模式分析器](#自定制一个模式分析器)
      * [多语言分析器](#多语言分析器)
      * [雪球分析器：snowball analyzer](#雪球分析器snowball-analyzer)
    * [字符过滤器 charFilter](#字符过滤器-charfilter)
    * [分词器 tokenizer](#分词器-tokenizer)
      * [UAX URL 电子邮件分词器（UAX RUL email tokenizer）](#uax-url-电子邮件分词器uax-rul-email-tokenizer)
      * [路径层次分词器：path hierarchy tokenizer](#路径层次分词器path-hierarchy-tokenizer)
      * [path_hierarchy](#path_hierarchy)
    * [分词过滤器](#分词过滤器)
      * [自定义分词过滤器](#自定义分词过滤器)
      * [多个分词过滤器](#多个分词过滤器)
* [建议器 suggester](#建议器-suggester)
* [集群 recovery](#集群-recovery)
    * [减少集群 full restart 造成的数据来回拷贝](#减少集群-full-restart-造成的数据来回拷贝)
    * [减少主副本之间的数据复制](#减少主副本之间的数据复制)
    * [特大热索引为何恢复慢](#特大热索引为何恢复慢)
* [索引模板](#索引模板)
* [索引别名](#索引别名)
    * [解决什么问题](#解决什么问题)
    * [创建别名 add](#创建别名-add)
    * [查询别名](#查询别名)
    * [删除别名 remove](#删除别名-remove)
    * [多个索引指向同一别名](#多个索引指向同一别名)
    * [过滤器别名](#过滤器别名)
    * [与路由一起使用](#与路由一起使用)
    * [写索引](#写索引)
* [路由 routing](#路由-routing)
    * [自定义路由](#自定义路由)
    * [通过路由查询文档](#通过路由查询文档)
    * [删除文档](#删除文档)
* [transport](#transport)
    * [nettytransport](#nettytransport)
      * [建立连接的过程](#建立连接的过程)
      * [处理请求的过程](#处理请求的过程)
* [cluster discovery 概述](#cluster-discovery-概述)
    * [节点探测 discovery faultdetection](#节点探测-discovery-faultdetection)
    * [discovery ping 机制](#discovery-ping-机制)
      
## RESTful CRUD

- PUT
- GET
- POST
- DELETE

## QUERY

> 关于 kibana KQL，请查询 [文档](https://www.elastic.co/guide/en/kibana/7.9/kuery-query.html)
> 

1.  query string 查询字符串

```
GET /movies/_search?q=title:beautiful
```

2. query DSL 结构化查询

```json
GET /movies/_search
{
  "query": {
    "match": {
      "title": "beautiful"
    }
  }
}
```

默认情况下，ES 在对文档分析期间（将文档分词后保存到倒排索引中），会对文档进行分词，比如默认的标准分析器会对文档进行：

- 删除大多数的标点符号。
- 将文档分解为单个词条，我们称为 token。
- 将 token 转为**小写**。

测试文档生成时的分析期间，查看标准分析器的分词

```json
POST _analyze
{
  "analyzer": "standard",
  "text": "Beautiful Mind"
}
// 结果
["beautiful", "mind"]
```

**不要使用 term 对类型是 text 的字段进行查询，要查询 text 类型的字段，请改用 match 查询。**

### term 查询

term 是代表完全匹配，也就是**精确搜索**，搜索前不会再对搜索词进行分词，所以我们的搜索词必须是文档分词集合中的一个。

```json
GET test/_search
{
  "query": {
    "term": {
        "title": "beautiful mind"
    }
  }
}
```

ES 会将 keyword 类型的字段当成一个 token 保存到倒排索引上，因此可以将 term 和 keyword 结合使用。

使用 terms 查询多个精确的值

```json
GET /movies/_search
{
  "query": {
    "terms": {
      "title": [
        "beautiful",
        "mind"
      ]
    }
  }
}
```

### match 类查询

match 查询会先对搜索词进行分词，分词完毕后再逐个对分词结果进行匹配，是**分词匹配搜索**，match 搜索还有两个相似功能的变种，一个是 match_phrase，一个是 multi_match。

返回整个文档

```json
{
  "query": {
    "match_all": {}
  }
}
```

只要文档中包含 beautiful 或 mind 任意一个词，都会被搜索到

```json
{
  "query": {
    "match": {
      "title": "beautiful mind"
    }
  }
}
```

文档中既有 beautiful 又有 mind 

```json
{
  "query": {
    "match": {
      "title": {
        "query": "beautiful mind",
        "operator": "and"
      }
    }
  }
}
```

#### match_phrase

按短语搜索。match_phrase 搜索方式和 match 类似，先对搜索词建立索引，并要求所有分词必须在文档中出现(类似于 match operator 为 and 的查询)，除此之外，还必须满足分词在文档中出现的顺序和搜索词中一致且各搜索词之间必须紧邻，因此 match_phrase 也可以叫做**紧邻搜索**。英文中以空格分词。

搜索"中国.*?世界"，? 代表中间隔几个词，可以用 slop 来表示，没有指明 slop 默认是0。

```json
{
  "query": {
    "match_phrase": {
      "title": {
        "query": "中国世界",
        "slop": 2
      }
    }
  }
}
```

前缀查询

```json
{
  "query": {
    "match_phrase_prefix": {
      "title": "bea",
      "max_expansions": 1
    }
  }
}
```

>max_expansions: 设置最大的前缀扩展数量

#### multi_match

当我们想对多个字段进行匹配，其中一个字段包含分词就能被搜索到。

用 match 来多字段查询

```json
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "title": "beautiful"
          }
        },
        {
          "match": {
            "desc": "beautiful"
          }
        }
      ]
    }
  }
}
```

用 multi_match 来查询

```json
{
  "query": {
    "multi_match": {
      "query": "beautiful",
      "fields": [
        "title",
        "desc"
      ]
    }
  }
}
```

multi_match 甚至可以当做 match_phrase 和 match_phrase_prefix 来使用，只需要指定 type 类型即可

```json
{
  "query": {
    "multi_match": {
      "query": "gi",
      "fields": [
        "title"
      ],
      "type": "phrase_prefix"
    }
  }
}

{
  "query": {
    "multi_match": {
      "query": "girl",
      "fields": [
        "title"
      ],
      "type": "phrase"
    }
  }
}
```

### bool 查询


### 排序

```json
GET /movies/_search
{
  "query":{
    "terms": {
      "title": ["beautiful", "mind"]
    }
  },
  "sort": [
    {
      "year": {
        "order": "desc"
      }
    }
  ],
  "from": 0,
  "size":3
}
```

### 聚合

聚合函数的使用，一定是先查出结果，然后对结果使用聚合函数做处理

aggs: max, min, avg, sum

## mappings

`GET /movies` 的返回值，主要由两部分组成
- 第一部分是与索引类型相关的，包括该索引是否有别名 aliases，然后就是 mappings 信息，索引各字段的详细映射关系都收集在 properties 中。
- 第二部分是关于索引的 settings 设置，包括该索引的创建时间、主副分片的信息、UUID 等等。

```json
//GET /movies
//=>
//GET /movies/_settings
//GET /movies/_mapping
{
  "movies" : {
    "aliases" : { },
    "mappings" : {
      "properties" : {
        // 。。。       
        "title" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "year" : {
          "type" : "long"
        }
      }
    },
    "settings" : {
      "index" : {
        "creation_date" : "1630396758361",
        "number_of_shards" : "1",
        "number_of_replicas" : "1",
        "uuid" : "i5c1FqylSoSV0rK1buF1GA",
        "version" : {
          "created" : "7090399"
        },
        "provided_name" : "movies"
      }
    }
  }
}
```

mappings一旦创建，则无法修改。因为 Lucene 生成倒排索引后就不能改了。

### 映射定义了什么

- 哪些字符串应该被视为全文字段。
- 哪些字段包含数字、日期或地理位置。
- 定义日期的格式。
- 自定义的规则，用来控制动态添加字段的的映射。

### 映射类型
- 元字段（meta-fields）：元字段用于自定义如何处理文档关联的元数据，例如包括文档的
   - _index
   - _type
   - _id
   - _source
- 字段或属性（field or properties）：映射类型包含与文档相关的字段或者属性的列表。

### 字段的数据类型

- 简单类型
   - 文本（text）
   - 关键字（keyword）
   - 日期（date）
   - 整型（long）
   - 双精度（double）
   - 布尔（boolean）
   - ip
- 支持 JSON 的层次结构性质的类型，如对象或嵌套。
- 特殊类型
   - geo_point
   - geo_shape
   - completion

### 映射分类

它们由 dynamic 属性控制。

- 动态映射（dynamic mapping）
   - dynamic：true
   - 这也是 ES 的默认设置——允许添加新的字段

- 静态映射（explicit mapping）
   - dynamic：false
   - 当有新增字段时，仍会存储该字段，但查询会忽略该字段。（因为 ES 不会主动的添加新的映射关系）

- 严格模式（strict mappings）
   - dynamic：strict
   - 当有新增的字段，会抛出异常。

### copy_to

该属性允许我们将多个字段的值复制到组字段中，然后可以对组字段进行查询。

```json
PUT test_copy_to

```

### ignore_above

长度超过 ignore_above 设置的字符串将不会被索引，也就是不能够被搜索到。

```json
PUT test_mapping
{
  "mappings": {
    "properties": {
      "t1": {
        "type": "keyword",
        "ignore_above": 5
      },
      "t2": {
        "type": "keyword",
        "ignore_above": 10
      }
    }
  }
}
```

当字段类型设置为 text 之后， ignore_above 参数的限制就失效了

```json
PUT test_mapping2
{
  "mappings": {
    "properties": {
      "t1": {
        "type": "keyword",
        "ignore_above": 5
      },
      "t2": {
        "type": "text", // 后面的 ignore_above 设置失效
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 10
          }
        }
      }
    }
  }
}
```

## settings

在创建一个索引的时候，我们可以在 settings 中指定分片信息。

```json
{
  "settings": {
    "number_of_replicas": 1,
    "number_of_shards": 5
  }
}
```

## 分析 analyze

当数据被发送到 ES ，加入到倒排索引之前，做了什么？

1. 字符过滤：使用字符过滤器转变字符。
2. 分词：将文本分为单个或多个分词。
3. 分词过滤：使用分词过滤器转变每个分词。
4. 分词索引：最终将分词存储在 Lucene 倒排索引中。

![analysis-processing](https://img2018.cnblogs.com/blog/1168165/201903/1168165-20190325122716354-856391461.bmp)

### 分析器

#### 标准分析器 —— ES 的默认分析器

包括标准分词器、标准分词过滤器、小写转换分词过滤器和停用词分词过滤器。

```json
POST _analyze
{
  "analyzer": "standard",
  "text":"To be or not to be,  That is a question ———— 莎士比亚"
}
```

#### 简单分析器

仅使用了小写转换分词，这意味着在非字母处进行分词，并将分词自动转换为小写。这个分词器对于亚洲语言来说效果不佳，因为亚洲语言不是根据空白来分词的，因此一般用于欧洲言中。

#### 空白分析器：whitespace analyzer

停用词分析器：stop analyzer
和简单分析器的行为接近，但1在分词流中额外的过滤了停用词。

模式分析器：pattern analyzer
允许指定一个分词切分模式。但是通常更佳的方案是使用定制的分析器，组合现有的模式分词器和所需要的分词过滤器更加合适。

#### 自定制一个模式分析器

```json
PUT /custom_analyzer
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_email_analyzer": {
          "type": "pattern",
          "pattern": "\\W|_",
          "lowercase": true
        }
      }
    }
  }
}
```

#### 多语言分析器

```json
POST /_analyze
{
  "analyzer": "chinese",
  "text":"我是中国人，中华民族是最伟大的民族之一！"
}
```

#### 雪球分析器：snowball analyzer

除了使用标准的分词和分词过滤器，也使用了小写分词过滤器和停用词过滤器，除此之外，它还是用了雪球词干器对文本进行词干提取。

### 字符过滤器 charFilter

对字符流进行处理。ES 提供的三种字符过滤器：

1. HTML字符过滤器（HTML Strip Char Filter）

从文本中去除HTML元素。

```json
POST _analyze
{
  "tokenizer": "keyword",
  "char_filter": ["html_strip"],
  "text":"<p>I&apos;m so <b>happy</b>!</p>"
}
```
2. 映射字符过滤器（Mapping Char Filter）

接收键值的映射，每当遇到与键相同的字符串时，它就用该键关联的值替换它们。

3. 模式替换过滤器（Pattern Replace Char Filter）

使用正则表达式匹配并替换字符串中的字符。要注意可能发生性能问题！

### 分词器 tokenizer

#### UAX URL 电子邮件分词器（UAX RUL email tokenizer）

uax_url_email

#### 路径层次分词器：path hierarchy tokenizer

#### path_hierarchy

### 分词过滤器

常见分词过滤器（token filter）

- ASCII折叠分词过滤器（ASCII Folding Token Filter）
将前127个ASCII字符(基本拉丁语的Unicode块)中不包含的字母、数字和符号 Unicode 字符转换为对应的 ASCII 字符。
- 扁平图形分词过滤器（Flatten Graph Token Filter）
接受任意图形标记流。例如由同义词图形标记过滤器生成的标记流，并将其展平为适合索引的单个线性标记链。这是一个有损的过程。
- 长度标记过滤器（Length Token Filter）
会移除分词流中太长或者太短的标记，它是可以在 settings 中配置的。
- 小写分词过滤器（Lowercase Token Filter）
将分词规范化为小写，它通过language 参数支持希腊语、爱尔兰语和土耳其语小写标记过滤器。
- 大写分词过滤器（Uppercase Token Filter）
将分词规范为大写。

#### 自定义分词过滤器

#### 多个分词过滤器

## 建议器 suggester

ES 设计了4种 suggester ：

- 词条建议器（term suggester）

   对于给定文本的每个词条，该键议器从索引中抽取要建议的关键词，这对于短字段（如分类标签）很有效。
- 词组建议器（phrase suggester）

   我们可以认为它是词条建议器的扩展，为整个文本（而不是单个词条）提供了替代方案，它考虑了各词条彼此临近出现的频率，使得该建议器更适合较长的字段，比如商品的描述。
- 完成建议器（completion suggester）

   该建议器根据词条的前缀，提供自动完成的功能（智能提示，有点最左前缀查询的意思），为了实现这种实时的建议功能，它得到了优化，工作在内存中。所以，速度要比之前说的match_phrase_prefix快的多！
- 上下文建议器（context suggester）

   它是完成建议器的扩展，允许我们根据词条或分类亦或是地理位置对结果进行过滤。

## 集群 recovery

recovery 指的是一个索引的分片分配到另外一个节点的过程，一般在快照恢复、索引复制分片的变更、节点故障或重启时发生，由于 master 节点保存整个集群相关的状态信息，因此可以判断哪些分片需要再分配及分配到哪个节点，例如：
- 如果某个主分片在，而复制分片所在的节点挂掉了，那么master需要另行选择一个可用节点，将这个主分片的复制分片分配到可用节点上，然后进行主从分片的数据复制。
- 如果某个主分片所在的节点挂掉了，复制分片还在，那么master会主导将复制分片升级为主分片，然后再做主从分片数据复制。
- 如果某个分片的主副分片都挂掉了，则暂时无法恢复，而是要等持有相关数据的节点重新加入集群后，master才能主持数据恢复相关操作。

recovery 过程要消耗额外的资源，CPU、内存、节点间的网络带宽等，可能导致集群的服务性能下降，甚至部分功能暂时无法使用，所以，有必要了解在 recovery 的过程和其相关的配置，来减少不必要的消耗和问题。

### 减少集群 full restart 造成的数据来回拷贝

有时候，可能会遇到集群整体重启的情况，比如硬件升级、不可抗力的意外等，那么再次重启集群会带来一个问题：某些节点优先起来，并优先选举出了主节点，有了主节点，该主节点会立刻主持 recovery 的过程；但此时，这个集群数据还不完整（还有其他的节点没有起来）；当整个集群恢复后，其各个节点的数据分布，显然是不均衡的（先启动的节点把数据恢复了，后起来的节点内删除了无效的数据），这时，master 就会触发 Rebalance 的过程，将数据在各个节点之间挪动，这个过程又消耗了大量的网络流量。所以，我们需要合理的设置/优化 recovery 相关参数。

例如，A 节点的主分片对应的复制分片所在的 B 节点还没起来，但主节点会将 A 节点的几个没有复制分片的主分片重新拷贝到可用的 C 节点上。而当 B 节点成功起来了，自检时发现在自己节点存储的 A 节点主分片对应的复制分片已经在 C 节点上出现了，就会直接删除自己节点中“失效”的数据（A 节点的那几个复制分片）。。。

- 在集群启动过程中，一旦有了多少个节点成功启动，就执行 recovery 过程：

```yaml
# 所有节点都算在内
gateway.expected_nodes: 3
# 有几个 master 节点启动成功
gateway.expected_master_nodes: 3
# 有几个 data 节点启动成功
gateway.expected_data_nodes: 3
```

- 当集群在期待的节点数条件满足之前，等待时长超过 gateway.recover_after_time 指定的时间，则会根据以下条件判断是否执行 recovery 的过程：

```yaml
gateway.recover_after_nodes: 3
gateway.recover_after_master_nodes: 3
gateway.recover_after_data_nodes: 3
```

- 配置说明

```yaml
gateway.expected_nodes: 5
gateway.recover_after_time: 5m
gateway.recover_after_data_nodes: 3
```

集群在 5 分钟内，有 5 个节点加入集群，或者 5 分钟后有 3 个以上的 data 节点加入集群，都会启动 recovery 的过程。

### 减少主副本之间的数据复制

如果不是 full restart ，而是重启单个节点，也会造成不同节点之间来复制，为了避免这个问题，可以在重启之前，关闭集群的shard allocation 。

```json
PUT _cluster/settings
{
  "transient": {
    "cluster.routing.allocation.enable": "none"
  }
}
# 节点重启后，再重新打开
PUT _cluster/settings
{
  "transient": {
    "cluster.routing.allocation.enable": "all"
  }
}
```

如果要重启一个包含大量热索引的节点，可以按照以下步骤执行重启过程，让 recovery 过程瞬间完成：

- 暂停数据写入
- 关闭集群的 shard allocation
- 手动执行 POST /_flush/synced
- 重启节点
- 重新开启集群的 shard allocation
- 等待 recovery 完成，当集群的 health status 是 green 后
- 重新开启数据写入

### 特大热索引为何恢复慢

对于冷索引，由于数据不再更新，利用 synced flush 可以快速的从本地恢复数据，而对于热索引，特别是 shard 很大的热索引，除了 synced flush 派不上用场，从而需要大量跨节点拷贝 segment file 以外， translog recovery 可能是导致慢的更重要的原因。

**translog recovery**

当节点重启后，从主分片恢复数据到复制分片需要经历 3 个阶段：
   - 第一阶段，对于主分片上的 segment file 做一个快照，然后拷贝到复制分片所在的节点，在数据拷贝期间，不会阻塞索引请求（写入请求），新增的索引操作会记录到 translog 中（理解为于临时文件）。
   - 第二阶段，对于 translog 做一个快照，此快照包含第一阶段新增的索引请求，然后重放快照里的索引操作，这个阶段仍然不会阻塞索引请求，新增索引操作记录到 translog 中。
   - 第三阶段，为了能达到主副分片完全同步，阻塞新索引请求，然后重放上一阶段新增的 translog 操作。

在整个 recovery 过程完成之前， translog 是不能被清除掉的。如果 shard 比较大，第一阶段会耗时很长，会导致此阶段产生的 translog 很大，重放 translog 要比简单的文件拷贝耗时更长，因此第二阶段的 translog 耗时也显著的增加了。到了第三阶段，需要重放的 translog 可能会比第二阶段更多，特别需要注意的是第三阶段是会阻塞新索引请求的，在对写入实时性要求很高的场合，这就会导致性能下降，非常影响用户体验。

因此，要加快特大热索引恢复速度，最好是参照[减少主副本之间的数据复制]()

## 索引模板

```json
PUT _template/2021
{
  "index_patterns": [
    "20*",
    "movie*"
  ],
  "settings": {
    "number_of_shards": 2,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "keyword"
      },
      "description": {
        "type": "keyword"
      }
    }
  }
}
```

## 索引别名

### 解决什么问题

在开发中，随着业务需求的迭代，为了适应新的业务逻辑，可能就要对原有的索引做一些修改，比如对某些字段做调整，甚至是重建索引。而做这些操作的时候，可能会对业务造成影响，甚至是停机调整等问题。索引别名就是来解决这些问题。

索引别名就像一个快捷方式或是软连接，可以指向一个或多个索引，也可以给任意一个需要索引名的 API 来使用。别名的应用为程序提供了极大地灵活性，下面这些操作：

- 在运行的集群中可以无缝的从一个索引切换到另一个索引。
- 可以给多个索引分组。
- 给索引的一个子集创建视图，没错我们可以简单将es中的索引理解为关系型- 数据库中的视图。
- 可以与路由搭配使用。

### 创建别名 add
```json
POST _aliases
{
  "actions": [
    {
      "add": {
        "index": "test1",
        "alias": "a1"
      }
    }
  ]
}
```

### 查询别名
```
GET {{baseUrl}}/test1/_alias
GET {{baseUrl}}/_aliases
```

### 删除别名 remove
```json
POST _aliases
{
  "actions": [
    {
      "remove": {
        "index": "test1",
        "alias": "a1"
      }
    }
  ]
}
```

### 多个索引指向同一别名

```json
{
  "actions": [
    {"add": {"index": "test1", "alias": "a1"}},
    {"add": {"index": "test2", "alias": "a1"}},
    {"add": {"index": "test3", "alias": "a1"}}
  ]
}
# 数组方式
{
  "actions": [
    {"add": {"indices": ["test1", "test2", "test3"], "alias": "a2"}}
  ]
}
# glob pattern
{
  "actions": [
    {"add": {"index": "test*", "alias": "a3"}}
  ]
}
```

### 过滤器别名

带有过滤器的别名提供了创建相同索引的不同视图的简单方法。

```json
{
  "actions": [
    {
      "add": {
        "index": "test4",
        "alias": "a4",
        "filter": {
          "term": {
            "year": 2019
          }
        }
      }
    }
  ]
}
```

### 与路由一起使用

除了单独使用别名，还可以将别名与路由值关联，以避免不必要的分片操作。

### 写索引
？

## 路由 routing

当索引一个文档的时候，文档会被存储到一个主分片中。那么，ES 如何知道一个文档应该存放到哪个分片中呢？

这个过程是根据下面公式决定的：

```
shard = hash(routing) % number_of_primary_shards
```

routing 是一个可变值，默认是文档的 _id ，也可以是自定义的值。hash 函数将 routing 值哈希后生成一个数字，然后这个数字再除以 number_of_primary_shards （主分片的数量）得到余数，这个分布在 [0, number_of_primary_shards - 1] 之间的余数，就是文档存放的分片位置。

由上面的公式也解释了为什么在创建索引时，主分片的数量一经定义就不能改变。如果主分片数量变化了，那么之前所有的路由值都会无效，文档就再也找不到了。

路由分配算法会将所有的文档平均分布在所有的主分片上，而不会产生某个分片数据过大而导致集群不平衡的情况。

向一个有 100 个主分片的索引的集群发送查询某篇文档的请求时，当请求发送到集群时，集群都做了什么？

- 这个请求会被集群交给主节点。
- 主节点接收这个请求后，将这个查询请求广播到这个索引的每个分片上（包含主、复制分片）。
- 每个分片都执行这个搜索请求，并将结果返回。
- 结果在主节点上合并、排序后返回给用户。

这里面有个些问题。因为在存储文档时，通过 hash 算法将文档平均分布在各分片上，导致了 ES 也不确定文档的位置，所以它必须将这个请求广播到所有的分片上去执行。

为了避免不必要的查询，就引入了自定义的路由模式，使我查询更具目的性。
查询从

```
请求来了，索引下的所有分片都要检查一下自己是否有符合条件的文档
```

转变为

```
请求来了，分片3、5 把文档给我返回
```

### 自定义路由

所有的文档 API（ get 、 index 、 delete 、 bulk 、 update 以及 mget ）都接受一个叫做 routing 的路由参数 ，通过这个参数我们可以自定义文档到分片的映射

### 通过路由查询文档

### 删除文档

查询多个路由

忘了路由值

## transport

transport是集群间通信的基础，它有两种实现：

- localtransport，主要用于 jvm 中的节点通信，因为在同一个 jvm 上的网络模拟， localtransport 的实现也相对简单，但实际用处在 ES 中有限。
- nettytransport，一种基于 netty 实现的 transport ，同样用于节点间的通信。

### nettytransport

transport 是集群通信的基本通道，无论是集群的状态信息，还是索引请求信息，都由 transport 传送。ES 定义了包括 transport 接口在内的所有基础接口， NettyTransport 也实现了该接口。

简单介绍一下 Netty 的使用依赖三个模块：

- ServerBootStrap，启动服务。
- ClientBootStrap，启动客户端并建立于服务端的连接。
- MessageHandler，负责主要的业务逻辑。

#### 建立连接的过程

- NettyTransport 在 doStart 方法中调用 ServerBootStrap 和 ClientBootStrap 并绑定 ip；
- bindServerBootstrap 将本地 ip 绑定到 netty 同时设定好 export host 。然后启动 client 和 server 的过程将 mergedSettings 注入到 channelpipeline 中，至此启动过程结束，但需要注意的是，现在 client 端并未连接 server 端，这个连接过程是在节点启动后才进行连接。
- 在每个 server 和 client 之间都有5个连接，每个连接承担着不同的任务。

#### 处理请求的过程

为了保证信息传输， ES 定义了一个19个字节长度的信息头：
```
HEADER_SIZE = 2 + 4 + 8 + 1 + 4
```
以 ES 开头，紧接着是 4 个字节的 int 类型信息长度，然后是 8 个字节的 long 类型的信息 id，再是 1 个字节的 status，最后是 4 个字节int 类型的 version。所有节点间的信息交互都以这个19个字节的头部开始。同时，es 对于节点间的所有 action 都定义了名字，如对 master 的周期检测型 action。每个 action 对应着相应的 messagehandler。

请求处理的过程：

- 信息通过 request 方法发送到目标节点。
- 目标节点的 messageHandler 收到该信息，确定是 request 还是 response ，然后将它们转发给 transportServicedAdapter，transportServicedAdapter 根据 request 或 response 类型交给对应的 handler 处理并反馈。

## cluster discovery 概述

ES 的 cluster 实现了自己的发现机制 Zen ，discovery 的功能包括：

- mater 选举
- master 错误探测
- cluster 中节点探测
- 单播广播的 ping

discovery 是可配置模块，除了默认机制 Zen，还有支持其他机制包括：

- Azure classic discovery 插件方式，广播
- EC2 discovery 插件方式，广播
- Google Compute Engine (GCE) discovery 插件方式，广播
- Zen discovery 默认实现，广播/单播

### 节点探测 discovery faultdetection

在 ES 的设计中，一个集群必须有一个主节点（master node）。用来处理请求、索引的创建、修改、节点管理等。

当有了 master 节点，该节点就要对各子节点进行周期性（心跳机制）的探测，保证整个集群的健康。

主节点和各节点之间都会进行心跳检测，比如 mater 要确保各节点健康状况、是否宕机等，而子节点也要要确保 master 的健康状况，一旦 master 宕机，各子节点要重新选举新的 master 。

这种相互间的心跳检测就是 faultdetection 。

### discovery ping 机制

ping 是 ES 中集群发现的基本手段，通过在局域网中广播或者指定 ping 的某些节点（单播）获取集群信息和节点加入集群等操作。 ZenDiscovery 机制实现了两种 ping 机制：

- 广播，当 ES 实例启动的时候，它发送了广播的 ping 请求到地址 224.2.2.4:54328 。而其他的 ES 实例使用同样的集群名称响应了这个请求。

广播的原理很简单，当一个节点启动后向局域网发送广播信息，任何收到节点只要集群名称和该节点相同，就会对此广播作出回应。这样这个节点就能获取集群相关的信息。

当节点在分布在多个网段时，广播模式就失效了

广播使用了 java 的 multicastsocket 

- 单播，各节点通过单播列表来发现彼此从而加入同一个集群。

单播使用的是 nettytransport


### 

```
/_cat/allocation
/_cat/shards
/_cat/shards/{index}
/_cat/master
/_cat/nodes
/_cat/indices
/_cat/indices/{index}
/_cat/segments
/_cat/segments/{index}
/_cat/count
/_cat/count/{index}
/_cat/recovery
/_cat/recovery/{index}
/_cat/health
/_cat/pending_tasks
/_cat/aliases
/_cat/aliases/{alias}
/_cat/thread_pool
/_cat/plugins
/_cat/fielddata
/_cat/fielddata/{fields}
```