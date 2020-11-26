#节点类
class Node(object):#name是字母，value是频数
    def __init__(self,name=None,value=None):
        self.name=name
        self.value=value
        self.left=None
        self.right=None
#哈夫曼树类
class HuffmanTree(object):
    #根据Huffman树的思想：以叶子节点为基础，反向建立Huffman树
    def __init__(self,char_weights=None,sentence=None):
        if char_weights:
            self.nodeList=[Node(k[0], k[1]) for k in char_weights]  #根据输入的字符及其频数生成叶子节点
        else :#根据输入的一段字符计算其频数生成叶子节点
            self.nodeList=[]
            for char in sentence:
                find=False#设一个标志位
                for node in self.nodeList:#如果列表中已经存在以该字符为名字的节点，则频数加一
                    if node.name==char:
                        node.value+=1
                        find=True
                        break
                if find==False:#如果不存在，则新建一个以这个char为名字的节点
                    self.nodeList.append(Node(char, 1))
        while len(self.nodeList) != 1:#不是根节点时
            self.nodeList.sort(key=lambda node: node.value, reverse=True)  #排序， key=lambda items: items[0]: 按照每个item的items[0]排序，reverse=True: 逆序排列。默认从小到大，逆序后从大到小
            sum = Node(value=(self.nodeList[-1].value + self.nodeList[-2].value))  # 最小权值树的权值和，加和得到的节点名字为空
            sum.left = self.nodeList.pop(-1)
            sum.right = self.nodeList.pop(-1)
            self.nodeList.append(sum)
            self.root=self.nodeList[0]
        self.L = [i for i in range(10)]# self.b用于保存每个叶子节点的Haffuman编码,range的值只需要不小于树的深度就行
        self.treeDict={}#新建一个词典，后面编码要用到
        self.pre(self.root,0)
    # 打印哈夫曼树，递归
    def pre(self,tree,length):
        node=tree
        if (not node):
            return
        elif node.name:
            print (node.name + '的编码为:')
            self.treeDict[node.name]= ''
            for i in range(length):
                print (self.L[i])
                self.treeDict[node.name]+=str(self.L[i])#生成以名字为键，对应编码为值的字典
            print ('\n')
            return
        self.L[length]=0
        self.pre(node.left, length + 1)
        self.L[length]=1
        self.pre(node.right, length + 1)
    def get_code(self,sentence):
        str=''
        for char in sentence:
            str+=self.treeDict[char]#直接从建立的字典里面查找得到对应的编码
        print('编码结果为：'+str)
        print('\n')
def encode(sentence):#编码
    tree = HuffmanTree(sentence=sentence)
    tree.get_code(sentence)
    return tree.root #根据sentence返回的树用在解码中
def decode(tree,code):#解码
    sentence=""
    pointer=tree#建立一个指针
    for idx,bit in enumerate(code):
        if bit=="0":#如果编码等于0，就找左子树
            if pointer.left.name:#如果左子树是叶节点
                sentence+= pointer.left.name
                pointer = tree#指针返回根节点
            else:
                pointer=pointer.left#否则指针指向该节点
        else:#如果编码等于1，找右子树
            if pointer.right.name:
                sentence += pointer.right.name
                pointer = tree
            else:
                pointer = pointer.right
    print("解码结果为："+sentence+"\n")

if __name__=='__main__':
    #输入的是字符及其频数
    #char_weights=[('C',2),('A',4),('S',2),('T',3),(';',3)]#输入的是字符及其频数
    sentence="CAS;CAT;SAT;AT"#输入的是一个sentence
    code="10111100011011100011001100011100"
    decode(encode(sentence), code)