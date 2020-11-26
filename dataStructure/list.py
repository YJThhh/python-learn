class SequenceList(object):#类=方法+属性   方法：__init__、remove、get、set、traval、insert   属性：num、data、max
    def __init__(self, size):
        # 初始化顺序表
        self.num = 0 #当前顺序表有几个非空值
        self.max = size
        self.data = [None] * self.max

    def insert(self, index, value):#任意位置插入
        if not isinstance(index, int):
            raise IndexError
        else:
            if 0 <= index <= self.num:
                for i in range(self.num,index,-1):
                    self.data[i]=self.data[i-1]
                self.data[index]=value
                self.num += 1
            else:
                raise IndexError

    def set(self,index,value):  #改
        if not isinstance(index, int):
            raise IndexError
        else:
            if 0 <= index < self.num:
                self.data[index]=value
            else:
                raise IndexError

    def get(self,index):   #查
        if not isinstance(index, int):
            raise IndexError
        else:
            print(self.data[index])
            return self.data[index]

    def remove(self,index):
        if not isinstance(index, int):
            raise IndexError
        else:
            if 0 <= index < self.num:
                for i in range(index,self.num):
                    self.data[i]=self.data[i+1]
                self.num-=1#等于self.num=self.num-1

    def travel(self):  #遍历
        print("/////////////////////")
        for i in range(self.num):
            print("第"+str(i)+"位ID是："+self.data[i].ID)
            print("第"+str(i)+"位name是："+self.data[i].name)
            print("第"+str(i)+"位计算机是："+str(self.data[i].computer))
            print("第"+str(i)+"位英语是："+str(self.data[i].english))
            print("\n")
class StudentSequenceList(SequenceList=10): #继承SequenceList   方法：__init__、remove、get、set、traval、insert、对成绩排序（新增）、返回不及格学生（新增）、输出70~90（新增）   属性：num、data、max
    #一、 子类不重写__init__ ， 实例化子类时，会自动调用父类定义的__init__
    #二、 子类重写了__init__时，实例化子类，就不会调用父类已经定义的__init__
    #三、为了能使用或扩展父类的行为，要显示调用父类的__init__方法，有以下两种调用方式。
    def sort(self):#排序:冒泡排序（从小到大）
        #（5，4），6，8，1➡ 4，（5，6），8，1 ➡ 4，5，（6，8），1 ➡ 4，5，6，（8，1）➡ 4，5，6，1，8   第一轮 比较了4次
        #（4，5），6，1，8 ➡ 4，（5，6），1，8 ➡ 4，5，（6，1），8 ➡ 4，5，1，6，8 第二轮 比较了3次
        #（4，5），1，6，8 ➡ 4，（5，1），6，8 ➡ 4，1，5，6，8 第三轮 比较了2次
        #（4，1），5，6，8 ➡ 1，4，5，6，8 第四轮 比较了1次
        #排序5个数 比较4轮 第一轮4次


        for i in range(self.num-1):  #轮数  self.num=5  0 1 2 3 4
            for j in range((self.num- 1) - i ):  # 这里之所以 n-1 还需要 减去 i 是因为每一轮冒泡最大的元素都会冒泡到最后，无需再比较
                if (self.data[j].computer+self.data[j].english) > (self.data[j+1].computer+self.data[j+1].english): #从小到大
                    self.data[j], self.data[j+1] = self.data[j+1],self.data[j]




class Student(object):
    def __init__(self,ID,name,computer,english):
        self.ID=ID
        self.name=name
        self.computer=computer
        self.english=english
if __name__ == '__main__':#满足 脚本直接执行
    stu1=Student("s20200674","xmy",100,100)
    stu2=Student("s20200151","yjt",101,80)
    stu3=Student("s20200232","zhr",60,60)
    stu4=Student("s20200410","ld",59,80)

    studentList=StudentSequenceList(10)

    studentList.insert(0,stu1)
    studentList.insert(1,stu2)
    studentList.insert(2,stu3)
    studentList.insert(3,stu4)

    studentList.travel()

    studentList.sort()

    studentList.travel()
    a=1
