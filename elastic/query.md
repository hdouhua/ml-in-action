# query

## term

term 查询是基于词项的查询，而且当设置为 term 查询时， ES 不会对这个词做任何处理，但是在文本进行分词时，通常都会将大写转为小写，这个时候就会出现查不出来的情况。如下:

```
PUT /my_test/_bulk
{ "index": { "_id": 1 }}
{ "desc":"I am Pantheon" }
{ "index": { "_id": 2 }}
{ "desc":"I am not Pantheon" }
{ "index": { "_id": 3 }}
{ "desc":"I am Leo" }

GET /my_test/_mapping

GET /my_test/_search
{
  "query": {
    "match_all": {}
  }
}

# 用了 standard 分词器，会 lowercase 处理
GET /my_test/_analyze
{
  "field": "desc",
  "text": "Pantheon"
}

# 没有结果
GET /my_test/_search
{
  "query": {
    "term": {
      "desc": {
        "value": "Pantheon"
      }
    }
  }
}

# 需要给字段额外添加的一个元数据信息`.keyword`，这样在生成文档时 ES 也会将该字段原封不动的保存到 keyword 属性中去。这样下面这个语句可以查询出来
# 将字段设置成 keyword 的时候，查询时已有的值不会被分词。
# term查询keyword字段： term不会分词。而keyword字段也不分词。需要完全匹配才可。
GET /my_test/_search
{
  "query": {
    "term": {
      "desc.keyword": {
        "value": "Pantheon"
      }
    }
  }
}

GET /my_test/_search
{
  "query": {
    "term": {
      "desc": {
        "value": "pantheon"
      }
    }
  }
}
```

## match 和 match_phase

match 和 match_phase 查询都是属于`全文查询`，全文查询**会给当前的句子进行分词**。通常来讲，索引的时候怎么分词，查询的时候就是用的什么分词器，不设置会使用默认分词器。


```
GET /my_test/_search
{
  "profile": false, 
  "query": {
    "match": {
      "desc": "I am Pantheon"
    }
  }
}

GET /my_test/_search
{
  "query": {
    "match": {
      "desc": {
        "query": "I am Pantheon",
        "operator": "and"
      }
    }
  }
}

GET /my_test/_search
{
  "query": {
    "match_phrase": {
      "desc": "I am Pantheon"
    }
  }
}

GET /my_test/_search
{
  "query": {
    "match_phrase": {
      "desc": {
        "query": "I am Pantheon",
        "slop": 1
      }
    }
  }
}
```

## 总结

这三种查询是对分词组合不同的玩法，
term 查询只查分词，不会对查询语句做任何处理。
match 查询，对查询语句分词后，查询文档是否包含分词项。
match_phase 是对查询语句分词后，各词项间隔距离多少的玩法。
