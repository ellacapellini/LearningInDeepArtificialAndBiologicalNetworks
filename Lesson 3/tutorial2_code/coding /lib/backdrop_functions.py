# Name: Ella Capellini 
# Email: ecapellini@student.ethz.ch
import torch
from torch.autograd import Function
class LinearFunction(Function):
    @staticmethod
    def forward(ctx, A, W, b=None):
        ctx.save_for_backward(A, W, b)
        Z = A @ W.t()
        if b is not None:
            Z = Z + b
        return Z
    @staticmethod
    def backward(ctx, grad_Z):
        A, W, b = ctx.saved_tensors
        grad_A = None
        grad_W = None
        grad_b = None
        if ctx.needs_input_grad[0]:
            grad_A = grad_Z @ W
        if ctx.needs_input_grad[1]:
            grad_W = grad_Z.t() @ A
        if b is not None and ctx.needs_input_grad[2]:
            grad_b = grad_Z.sum(dim=0)
        return grad_A, grad_W, grad_b

def linear_function(A, W, b=None):
    if b is None:
        return LinearFunction.apply(A, W)
    else:
        return LinearFunction.apply(A, W, b)

class SigmoidFunction(Function):
    @staticmethod
    def forward(ctx, Z):
        ctx.save_for_backward(Z)
        A = torch.sigmoid(Z)
        return A
    @staticmethod
    def backward(ctx, grad_A):
        Z, = ctx.saved_tensors
        grad_Z = None
        if ctx.needs_input_grad[0]:
            s = torch.sigmoid(Z)
            grad_Z = grad_A * s * (1 - s)
        return grad_Z

sigmoid_function = SigmoidFunction.apply

class MSELossFunction(Function):
    @staticmethod
    def forward(ctx, A, T):
        ctx.save_for_backward(A, T)
        L = 0.5 * ((A - T) ** 2).sum() / A.shape[0]
        return L
    @staticmethod
    def backward(ctx, grad_L):
        A, T = ctx.saved_tensors
        grad_A = None
        grad_T = None
        if ctx.needs_input_grad[0]:
            grad_A = grad_L * (A - T) / A.shape[0]
        if ctx.needs_input_grad[1]:
            grad_T = -grad_L * (A - T) / A.shape[0]
        return grad_A, grad_T

mse_loss = MSELossFunction.apply

if __name__ == '__main__':
    pass