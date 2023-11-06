class Mutable:
    def __init__(self, value) -> None:
        self.val = value

    def get(self):
        return self.val
    
    def set(self, value):
        self.val = value

    def __str__(self) -> str:
        return str(self.val)
    
    def __repr__(self) -> str:
        return f'M: ({self.val})'
    
    def __iadd__(self, other):
        self.val += other
        return self
    
    def __isub__(self, other):
        self.val -= other
        return self
    
    def __imul__(self, other):
        self.val = self.val * other
        return self