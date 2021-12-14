from myhdl import bin, intbv, Signal, modbv


a = intbv(-3)
print(bin(a, width=5))
b = a[5:]
print(b)
print(bin(b))
c = intbv(24)[5:]
print(bin(c))
print(c)
print(c.min)
print(c.max)
print(len(c))


count = Signal(modbv(0, min=0, max=2**8))
print(count)
count.next = count+1
print(count.next)  # == 1
print(count.next)  # == 1
print(count.next)  # == 1
print(count.next)  # == 1
