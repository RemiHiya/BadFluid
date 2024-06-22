
class Bad:
    def __init__(self, cap, scale, screen, rate = 1/30):
        self.time = 0
        self.frame = 0
        self.cap = cap
        self.scale = scale
        self.screen = screen
        self.rate = rate
    
    def next(self):
        self.frame += 1
        self.time += self.rate

    def render(self):
        pass