forward:   Z = A @ W.t();  if b is not None: Z = Z + b;  return Z
backward:  grad_A = grad_Z @ B.t()       # B replaces W (the only difference from backprop)
           grad_W = grad_Z.t() @ A
           grad_b = grad_Z.sum(dim=0)