class Z:
    def __init__(self,c):
        self.z: complex = 0
        self.c: complex = c
        self.set = [0]

    def f(self):
        self.z = (self.z**2) + self.c
        self.set.append(self.z)


    def calc(self,esc,max):
        i = 0
        if max > 50:
            max = 50

        while i < max and abs(self.z) < esc:
            self.f()
            i += 1
