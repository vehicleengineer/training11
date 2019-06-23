# -*- coding: utf-8 -*-
"""CIFAR-10分类.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KVwiv5dzPaCjR2YfXJnr76xw3Vaodcz8
"""

#使用torchvision加载数据集
import torch as t
import torchvision as tv
import torchvision.transforms as transfroms
from torchvision.transforms import ToPILImage
show = ToPILImage() #该函数将Tensor转成Image,实现可视化

# 定义数据预处理
transform = transforms.Compose([transforms.ToTensor(),
                               transfroms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)), #归一化处理])
#加载训练集
trainset = tv.datasets.CIFAR10(
                  root='/home/cy/data/',
                  train=True,
                  download=True,
                  transform=transform)
                                
trainloader =t.utils.data.DataLoader(
                                    trainset,
                                    batch_size=4,
                                    shuffle=True,
                                    num_workers=2)
#加载测试数据集
testset = tv.datasets.CIFAR10(
                              '/home/cy/data/',
                              train=False,
                              download=True,
                              transform=transfrom)
                                
testloader = t.utils.data.DataLoader(
                                     testset,
                                     batch_size=4,
                                     shuffle=False,
                                     num_workers=2)
classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

#按下标访问Dataset数据集
(data, label) = trainset[100]
print(classes[label])

dataiter = iter(trainloader)
images, labels = dataiter.next()
print(' '.join('%11s'%classes[labels[j]] for j in range(4)))
show(tv.utils.make_grid((images+1)/2)).resize((400,100))

#定义网络
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
  def __init__(self):
    super(Net, self).__init__()
    self.conv1 = nn.Conv2d(3, 6, 5)
    self.conv2 = nn.Conv2d(6, 16, 5)
    self.fc1   = nn.Linear(16*5*5, 120)
    self.fc2   = nn.Linear(120, 84)
    self.fc3   = nn.Linear(84, 10)
    
  def forward(self, x):
    x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
    x = F.max_pool2d(F.relu(self.conv2(x)), 2)
    x = x.view(x.size()[0], -1)
    x = F.relu(self.fc1(x))
    x = F.relu(self.fc2(x))
    x = self.fc3(x)
    return x
  
net = Net()
print(net)

#define loss function and optimizer
from torch import optim
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

# 训练网络，输入数据+前向传播+反向传播+更新参数
for epoch in range(2):
  running_loss = 0.0
  for i, data in enumerate(trainloader, 0):
    
    #输入数据
    inputs, labels = data
    inputs, labels = Variable(inputs), Variable(labels)
    
    #梯度清零
    optimizer.zero_grad()
    
    #forward + backward
    outputs = net(inputs)
    loss = criterion(outputs, labels)
    loss.backward()
    
    #update params
    optimizer.step()
    
    #打印log信息
    running_loss += loss.data[0]
    if i % 2000 == 1999:
      print('[%d, %5d] loss: %.3f' \
#            % (epoch+1, i+1, running_loss / 2000))
      running_loss = 0.0
      
print('Finished Training')

#观察网络训练的效果
dataiter = iter(testloader)
images, labels = dataiter.next()
print('实际的label: ', ' '.join(\
                            '%08s'%classes[labels[j]] for j in range(4)))
show(tv.utils.make_grid(images / 2 - 0.5)).resize((400,100))

#计算图片在每个分类上的分数
outputs = net(Variable(images))
#得分最高的类
_, predicted = t.max(outputs.data, 1)

print('预测结果：', ' '.join('%5s'\
#                        % classes[predicted[j]] for j in range(4)))

#计算整个测试集的效果
correct = 0
total = 0
for data in testloader:
  images, labels = data
  outputs = net(Variable(images))
  _, predicted = t.max(outputs.data, 1)
  total += labels.size(0)
  correct = += (predicted == labels).sum()
  
print('1000张测试集中的准确率为：%d %%' % (100 * correct / total))