# Yair Cohen 318571718
import hashlib
import math

# this class holds all the data of a node in tree.
class Node:
    # constructor of the node.
    def __init__(self, data, low, high, l, r):
        self.left = l
        self.right = r
        self.parent= None
        self.data = data
        self.lower=low
        self.higher=high
    # setter method that sets the parent of the node.
    def setParent(self,p):
        self.parent = p

# this is the main function that gives service.
def merkleTreeCreatotr():
    isthereTree = False
    while True:
        strinput = input()
        inputlist = strinput.split(" ") # splitting the input.
        if inputlist[0] == "1":
            isthereTree = True
            tree = []
            numleaves = len(inputlist[1:])
            tree = creaTreeArrnode(inputlist[1:])# creates tree.
            addParents(tree) # sets the parents of every node.
        elif inputlist[0] == "2":
            if isthereTree:
                if int(inputlist[1]) >= numleaves: # checks if the index given is in range.
                    exit(-1)
                else:
                    proofOfInclusion(tree,int(inputlist[1])) # gets the proof of inclusion.
            else:
                exit(-1)
        elif inputlist[0] == "3":
            if checkInclusionPath(inputlist[1:]) == True: # checks if the path of the check is valid.
                checkInclusionValid(inputlist[1:]) # checs the proof of inclusion.
            else:
                exit(-1)
        elif inputlist[0] == "4":# gets a nonce with startinn zeroes according to the input.
            if isthereTree:
                try:
                    val = int(inputlist[1])
                    findNonce(tree, int(inputlist[1]))
                except ValueError:
                    exit(-1)
            else:
                exit(-1)
        elif inputlist[0] == "5":# close the program.
            exit(-1)
# checks the validilityof the path given.
def checkInclusionPath(str):
    i=2
    flag = True
    while i <len(str):
        if str[i] == 'l' or str[i] == 'r':
            flag=True
        else:
            flag=False
        i+=2
    return flag


# creates the merkle tree and returns it.
def creaTreeArrnode(list):
    num_leaves = len(list)
    num_nodes = num_leaves * 2 - 1
    tmp = num_leaves
    tree = []
    height = int(math.log2(num_leaves)) + 1
    n = 0
    while n < num_leaves:# goes over the leaves and adds them and adds them to the tree.
        tree.append(Node(list[n],n,n,None,None))
        n += 1
    j = 0
    n = num_leaves
    while n< num_nodes:# goes over the rest of the nodes and adds them to the tree.
        hashstr = tree[j].data + tree[j + 1].data
        tree.append(Node(hashlib.sha256(hashstr.encode()).hexdigest(), tree[j].lower, tree[j+1].higher, tree[j], tree[j+1]))
        n += 1
        j += 2
    print(tree[n-1].data)# prints the root.
    return tree[n-1] #return the root.

# adds the parent of every node.
def addParents(head):
    if head.left is not None:
        head.left.setParent(head)
        head.right.setParent(head)
        addParents(head.left)
        addParents(head.right)
    else:
        return


leafp = None

# this method return a leaf by its index.
def findInTree(head,index):
    if head is not None:
        if head.lower == index and head.higher==index:
            global leafp
            leafp = head
            return head
        elif head.left is not None:
            findInTree(head.left,index)
            findInTree(head.right,index)

# provide a proof of inclusion.
def proofOfInclusion(head,index):
    leafproof=findInTree(head,index)# gets the leaf.
    node = leafp
    strm = ""
    i =0
    while node.data != head.data: # if we havent reached the head.
        if checkROL(node)==0:#current node is left node meaning you need to get the right node.
            strm = strm + "l "
            strm = strm + node.parent.left.data + " "
        if checkROL(node) == 1:#current node is right node meaning you need to get the left node.
            strm = strm + "r "
            strm = strm +node.parent.right.data + " "
        node=node.parent
    print(strm) # prints the proof.

# a fuction that counts the leading zeroes in a string.
def countZeroes(str):
    count = 0
    i=0
    while i < len(str):
        if str[i] == '0':
            count+=1
        else:
            break
        i+=1
    return count

# find a nonce that if conacts to the root and hashes gives the desired amount of leading zeroes in the new result.
def findNonce(head,index):
    i=0
    run = True
    while run:
        hashstr = str(i) + head.data #hashlib.sha256(str(i).encode()).hexdigest()
        strn = hashlib.sha256(hashstr.encode()).hexdigest()
        if countZeroes(strn) >= int(index):
            print(str(i) + " " + strn)
            run = False
        i+=1

# checks wether a node is a leaft node or a right node returns zero or 1 or -1.
def checkROL(node):
    if node is not None:
        if node.parent.left.data == node.data:
            return 1 # if is a left node.
        if node.parent.right.data == node.data:
            return 0 # if it is right node.
    return -1# if it isnt one of the options.

# cheacs if the given proof of inclusion is correct or not.
def checkInclusionValid(list):
    tree_root = list[1]
    i=4
    if list[2]== 'r':
        hashstr = list[0]+list[3]
    if list[2] == 'l':
        hashstr = list[3] + list[0]
    hashstr = hashlib.sha256(hashstr.encode()).hexdigest()
    while i< len(list):
        if list[i] == 'r':
            hashstr =  hashstr + list[i+1]
            hashstr = hashlib.sha256(hashstr.encode()).hexdigest()
        if list[i] == 'l':
            hashstr = list[i+1] + hashstr
            hashstr = hashlib.sha256(hashstr.encode()).hexdigest()
        i +=2
    if hashstr==tree_root:# if its matches the root then its correct.
        print("True")
    else:
        print("False")


merkleTreeCreatotr()



# a test func for the tree.
# def creaTreeArr(list):
#     num_leaves = len(list)
#     num_nodes = num_leaves * 2 - 1
#     tmp = num_leaves
#     tree = []
#     height = int(math.log2(num_leaves)) + 1
#     n = 0
#     while n < num_leaves:
#         tree.append(list[n])
#         n += 1
#     j = 0
#     n = num_leaves
#     c = int(n + (num_leaves / 2))
#     hh = 1
#     while hh < height:
#         while n < c:
#             hashstr = tree[j] + tree[j + 1]
#             tree.append(hashlib.sha256(hashstr.encode()).hexdigest())
#             n += 1
#             j += 2
#         p = math.pow(2, hh + 1)
#         c = c + (num_leaves / p)
#         hh += 1
#     print(tree)
