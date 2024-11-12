import torch
from torch import nn, optim
from torchvision.datasets import MNIST
from torchvision.transforms import ToTensor
from torchinfo import summary

train_data = MNIST(root='data', train=True, download=True, transform=ToTensor())
test_data = MNIST(root='data', train=False, download=True, transform=ToTensor())
train_loader = torch.utils.data.DataLoader(train_data, batch_size=128)
test_loader = torch.utils.data.DataLoader(test_data, batch_size=128)

model = nn.Sequential(
    nn.Conv2d(in_channels=1, out_channels=6, kernel_size=5, padding=2),
    nn.ReLU(),
    nn.MaxPool2d(2, stride=2),
    nn.Conv2d(6, 16, 5),
    nn.ReLU(),
    nn.MaxPool2d(2, stride=2),
    nn.Conv2d(16, 120, 5),
    nn.ReLU(),
    nn.Flatten(),
    nn.Linear(in_features=120, out_features=84),
    nn.ReLU(),
    nn.Linear(84, 10)

)

print(summary(model, (16, 1, 28, 28))) # 작동하는지 확인하려고 추가한 코드

# Conv2d hyperparameters
# positional arguments: in_channels, out_channels, kernel_size
# keyword arguments: stride, padding
# MaxPool2d hyperparameters
# positional arguments: kernel_size
# keyword arguments: stride
# Linear hyperparameters
# positional arguments: in_features, out_features