基于pandas操作实现多表连接操作

```sql
select
n_name,sum(l_extendedprice * (1 - l_discount)) as revenue
from
customer,orders,lineitem,supplier,nation,region
where
c_custkey = o_custkey
and l_orderkey = o_orderkey
and l_suppkey = s_suppkey
and c_nationkey = s_nationkey
and s_nationkey = n_nationkey
and n_regionkey = r_regionkey
and r_name = 'ASIA'
and o_orderdate >=  '1994-01-01'
and o_orderdate < '1995-01-01'
group by
n_name
order by
revenue desc;
```

重点研究如何实现Python的复杂表连接结构上的查询处理。

**命名格式**：学号-思考题10-姓名

**注意**：github的file中可正常使用markdown语法进行编辑，由于最后组长还需要把大家的技术文档整理成一个完整的文档提交给老师，所以请大家**直接在guihub上编写代码**，谢谢~

**上传完毕的同学请进入readme.md修改自己名字前的方括号**

- [x] 已完成示例
- [ ] 杨丹琼
- [x] 杨嘉欣
- [x] 于海洋
- [x] 张淼
- [x] 周林峻
- [ ] 马玥
