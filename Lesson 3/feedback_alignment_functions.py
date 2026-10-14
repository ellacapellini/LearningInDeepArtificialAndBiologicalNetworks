# Name: Ella Capellini 
# Email: ecapellini@student.ethz.ch
import torch
from torch.autograd import Function

class LinearFunctionFA(Function):
    @staticmethod
    def forward(ctx, A, W, B, b=None):
        ctx.save_for_backward(A, W, B, b)
        Z = A @ W.t()
        if b is not None:
            Z = Z + b
        return Z

    @staticmethod
    def backward(ctx, grad_Z):
        A, W, B, b = ctx.saved_tensors
        grad_A = None
        grad_W = None
        grad_B = None
        grad_b = None
        if ctx.needs_input_grad[0]:
            grad_A = grad_Z @ B.t()
        if ctx.needs_input_grad[1]:
            grad_W = grad_Z.t() @ A
        if b is not None and ctx.needs_input_grad[3]:
            grad_b = grad_Z.sum(dim=0)
        return grad_A, grad_W, grad_B, grad_b


def linear_function_fa(A, W, B, b=None):
    if b is None:
        return LinearFunctionFA.apply(A, W, B)
    else:
        return LinearFunctionFA.apply(A, W, B, b)

if __name__ == '__main__':
    pass