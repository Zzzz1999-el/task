基于列表的列存储模型，设计布尔型数组的位图索引结构，在part表的P_CONTAINER列上设计一个位图索引，即每个位图表示P_CONTAINER列中某个值对应的位置，例如'JUMBO BOX'对应一个布尔型数组位图，'LG CAN'对应一个布尔型数组位图，执行`p_container='JUMBO BOX' or p_container='LG CAN'`时通过位图运算输出满足条件的记录的数量（计数操作）。
在part表的P_CONTAINER列上为每个成员值创建一个位图，查询输入两个字符串，通过位图计算满足条件（或条件）的记录数量并输出。

**命名格式**：学号-思考题7-姓名

**注意**：github的file中可正常使用markdown语法进行编辑，由于最后组长还需要把大家的技术文档整理成一个完整的文档提交给老师，所以请大家**直接在guihub上编写代码**，谢谢~

**上传完毕的同学请进入readme.md修改自己名字前的方括号**

- [x] 已完成示例
- [ ] 赵玉冰
- [ ] 郑畅
- [ ] 郑宏铭