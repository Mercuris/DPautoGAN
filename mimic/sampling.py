import torch
from torch.utils.data import DataLoader, TensorDataset
import numpy as np

class IIDBatchSampler:
    def __init__(self, dataset, minibatch_size, iterations):
        self.length = len(dataset)
        self.minibatch_size = minibatch_size
        self.iterations = iterations

    def __iter__(self):
        for _ in range(self.iterations):
            indices = np.where(torch.rand(self.length) < (self.minibatch_size / self.length))[0]
            if indices.size > 0:
                yield indices

    def __len__(self):
        return self.iterations

class EquallySizedAndIndependentBatchSampler:
    def __init__(self, dataset, minibatch_size, iterations):
        self.length = len(dataset)
        self.minibatch_size = minibatch_size
        self.iterations = iterations

    def __iter__(self):
        for _ in range(self.iterations):
            yield np.random.choice(self.length, self.minibatch_size)

    def __len__(self):
        return self.iterations

def get_data_loaders(minibatch_size, microbatch_size, iterations):
    def minibatch_loader(dataset):
        return DataLoader(
            dataset,
            batch_sampler=IIDBatchSampler(dataset, minibatch_size, iterations)
        )

    def microbatch_loader(minibatch):
        return DataLoader(
            minibatch,
            batch_size=microbatch_size,
            drop_last=True,
        )

    return minibatch_loader, microbatch_loader

