# agents/policy_net.py
import torch
import torch.nn as nn

class SimplePolicy(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(102, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, 100)
        )

    def forward(self, x):
        return self.fc(x)