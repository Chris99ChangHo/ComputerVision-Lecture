import torch
import torch.nn.functional as F
from torch import nn, optim
from torch.utils.data import DataLoader
from torchvision.datasets import MNIST
from torchvision.transforms import ToTensor
from torchmetrics import Accuracy # pip install torchmetrics

# 데이터 수집
mnist_trainset = MNIST(
    root='data', train=True, download=True,
    transform=ToTensor()
    )
# print(mnist_trainset.data)
train_loader = DataLoader(mnist_trainset, batch_size=128)

# 모델 정의
model = nn.Sequential(
    nn.Flatten(),
    nn.Linear(784, 128), # 28*28=784 pixels in MNIST images and 128 neurons in the hidden layer => 784x128 weights + 128 biases = 100480 parameters 
    nn.Sigmoid(),
    nn.Linear(128, 10), # 128 neurons in the hidden layer and 10 classes in MNIST => 128x10 weights + 10 biases = 1290 parameters 
    nn.Softmax(dim=1)
)
# print(model)
# 학습, 예측
num_epochs = 10
loss_fn = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)
metric = Accuracy(task='multiclass', num_classes=10)
model.train()
for i in range(num_epochs):
    for j, (x, y) in enumerate(train_loader):
        y_hat = model(x) # logit = y_hat
        y = F.one_hot(y, num_classes=10).float() # one-hot encoding
        # print(x.dtype, y.dtype, y_hat.dtype) # torch.float32 torch.int64 torch.float32
        # break
        loss = loss_fn(y_hat, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        acc = metric(y_hat, y)
        if j % 100 == 0:
            print(f'Epoch: {str(i).zfill(2)}, iter: {str(j).zfill(2)}, Loss: {loss:>7f}, accuracy: {acc:>2f}') 

