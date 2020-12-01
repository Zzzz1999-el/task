从SQL Server数据库（或直接从.tbl数据文件）读取表lineitem到pandas中，设计表上的操作案例，如：

```sql
select
l_returnflag,
l_linestatus,
sum(l_extendedprice*(1-l_discount)*(1+l_tax)) as sum_charge,
avg(l_quantity) as avg_qty,
count(*) as count_order
from
lineitem
where
l_shipdate <= date '1998-12-01' 
group by
l_returnflag,
l_linestatus
order by
l_returnflag,
l_linestatus;
```

按l_returnflag和l_linestatus列的值分组统计满足`l_shipdate <= date '1998-12-01'`记录的聚集计算结果，聚集计算结果按l_returnflag,l_linestatus排序输出。

**命名格式**：学号-思考题9-姓名

**注意**：github的file中可正常使用markdown语法进行编辑，由于最后组长还需要把大家的技术文档整理成一个完整的文档提交给老师，所以请大家**直接在guihub上编写代码**，谢谢~

**上传完毕的同学请进入readme.md修改自己名字前的方括号**

- [x] 已完成示例
- [ ] 许赟辉
- [ ] 杨莹
- [ ] 姚雨薇
- [ ] 袁钊颖
- [ ] 张馨月
- [ ] 石佳鑫
