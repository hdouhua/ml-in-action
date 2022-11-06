import org.apache.spark.rdd.RDD

// 第一步，读取内容

// 设置数据文件的根目录
val rootPath: String = "/home/dao/spk"
val file: String = s"${rootPath}/wikiOfSpark.txt"
 
// 读取文件内容
val lineRDD: RDD[String] = spark.sparkContext.textFile(file)


// 第二步，分词

// 以行为单位做分词，分词之后会有很多空字符串
val wordRDD: RDD[String] = lineRDD.flatMap(line => line.split(" "))

// 过滤掉空字符串
val cleanWordRDD: RDD[String] = wordRDD.filter(word => !word.equals(""))


// 第三步，分组计数

// 把RDD元素转换为（Key，Value）的形式
val kvRDD: RDD[(String, Int)] = cleanWordRDD.map(word => (word, 1))

// 按照单词做分组计数
val wordCounts: RDD[(String, Int)] = kvRDD.reduceByKey((x, y) => x + y)


// 打印词频最高的5个词汇
wordCounts.map{case (k, v) => (v, k)}.sortByKey(false).take(5)
