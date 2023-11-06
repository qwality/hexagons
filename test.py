from pygame import Vector2,Surface
x, y = Vector2(0,1)

print(x, y)

a,b,c,d = *(0,1), *(2,3)
print(a,b,c,d)
print(Vector2(1))

a = Vector2(5,4)
a.update(6,4)

print(Vector2(2,3) * Vector2(5,6))
a = Surface((0,0))
