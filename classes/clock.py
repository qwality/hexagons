class Clock:
    def __init__(self, tick_speed, framerate):
        self.tick_speed = tick_speed
        self.frame_rate = framerate
        self.__tick     = 0
        self.paused     = False
        self.running    = True

    @property
    def tick(self) -> bool:
        tick = self.__tick >= self.frame_rate
        if tick: self.__tick = 1
        return tick
    
    def __enter__(self):
        return self.tick

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.tick: self.__tick += self.tick_speed