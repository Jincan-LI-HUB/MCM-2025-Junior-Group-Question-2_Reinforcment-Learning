# gnn_model.py
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, global_mean_pool
from torch_geometric.data import Data, DataLoader

class DivisibilityGNN(nn.Module):
    def __init__(self, hidden_dim=64, output_dim=100):
        super().__init__()
        self.conv1 = GCNConv(1, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = F.relu(self.conv1(x, edge_index))
        x = F.relu(self.conv2(x, edge_index))
        x = global_mean_pool(x, data.batch)
        return self.fc(x)

def build_divisibility_graph():
    """
    构建 1~100 的整除图：i <-> j if i|j or j|i
    """
    edge_index = []
    for i in range(1, 101):
        for j in range(i+1, 101):
            if j % i == 0 or i % j == 0:
                edge_index.append([i-1, j-1])  # 0-indexed
                edge_index.append([j-1, i-1])

    edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
    x = torch.ones((100, 1))  # 每个节点一个特征（可扩展）
    data = Data(x=x, edge_index=edge_index)
    return data

# 示例用法
if __name__ == "__main__":
    gnn = DivisibilityGNN()
    graph_data = build_divisibility_graph()
    graph_data.batch = torch.zeros(100, dtype=torch.long)  # 单图
    embedding = gnn(graph_data)
    print("GNN 输出维度:", embedding.shape)  # [1, 100]