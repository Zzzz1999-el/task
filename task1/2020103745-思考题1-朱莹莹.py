
s = 0 #初始化累计和为0
p_size = [] #创建一个空列表存储p_size
p_container = [] #创建一个空列表存储p_container
p_retailprice = [] #创建一个空列表存储p_retailprice
f = open('D:\\硕士课程\\计算机基础\\part.tbl') #打开文件
for line in f.readlines(): #逐行读取
    line= line.rstrip() #去掉每行末尾空格
    line = line.split('|') #每行按"|"进行分隔，变成一个列表
    p_size.append(eval(line[5])) #存入每行对应p_size的部分，同时，将字符串变成数值
    p_container.append(line[6])  #存入每行对应p_scontainer的部分
    p_retailprice.append(eval(line[7]))#存入每行对应p_retailprice的部分，同时，将字符串变成数值
f.close()


bitmap = [] #创建一个空的位图列表
for i in range(len(p_size)): #筛选p_size＜15对应的index,满足条件的将对应位置的bitmap置为1，否则置为0
    if p_size[i] < 15 :
        bitmap.append(1)
    else :
        bitmap.append(0)
        
sum(bitmap) #查看此时bitmap中1的个数
#56606

for i in range(len(p_container)): #对满足条件1的index（对应bitmap=1）再次筛选，将p_container != “WRAP BOX”所对应的bitmap置为0
    if bitmap[i] == 1:
        if p_container[i] != "WRAP BOX":
            bitmap[i] = 0
            
sum(bitmap) #查看经过两轮筛选后bitmap中1的个数
#1413

for i in range(len(bitmap)): #对bitmap=1部分所对应的p_retailprice进行累加求和，存入s中
    if bitmap[i] == 1:
        s += p_retailprice[i]
print(s)
#2129994.780000001
