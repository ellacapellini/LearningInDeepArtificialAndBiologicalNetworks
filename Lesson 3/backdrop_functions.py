# LinearFunction
forward:   Z = A @ W.t();  if b is not None: Z = Z + b;  return Z
backward:  grad_A = grad_Z @ W
           grad_W = grad_Z.t() @ A
           grad_b = grad_Z.sum(dim=0)

# SigmoidFunction
forward:   A = torch.sigmoid(Z);  return A
backward:  s = torch.sigmoid(Z);  grad_Z = grad_A * s * (1 - s)

# MSELossFunction
forward:   L = 0.5 * ((A - T) ** 2).sum() / A.shape[0];  return L
backward:  grad_A = grad_L * (A - T) / A.shape[0]
           grad_T = -grad_L * (A - T) / A.shape[0]
           return grad_A, grad_T          # this return was commented out in the template