# exercise 1


# from myhdl import block, delay, always, now
#
# @block
# def HelloWorld():
#
#     @always(delay(10))
#     def say_hello():
#         print("%s Hello World!" % now())
#
#     return say_hello
#
#
# inst = HelloWorld()
# inst.run_sim(30)

# exercise 2
#
# from myhdl import block, Signal, delay, always, now
#
# @block
# def HelloWorld():
#
#     clk = Signal(0)
#
#     @always(delay(10))
#     def drive_clk():
#         clk.next = not clk
#
#     @always(clk.posedge)
#     def say_hello():
#         print("%s Hello World!" % now())
#
#     return drive_clk,  say_hello
#
#
# inst.run_sim(50)
# inst = HelloWorld()

# exercise 3

from myhdl import block, always, now, Signal, delay, instance

@block
def ClkDriver(clk, period=20):

    lowTime = int(period / 2)
    highTime = period - lowTime

    @instance
    def drive_clk():
        while True:
            yield delay(lowTime)
            clk.next = 1
            yield delay(highTime)
            clk.next = 0

    return drive_clk


@block
def Hello(clk, to="World!"):

    @always(clk.posedge)
    def say_hello():
        print("%s Hello %s" % (now(), to))

    return say_hello


@block
def Greetings():

    clk1 = Signal(0)
    clk2 = Signal(0)

    clkdriver_1 = ClkDriver(clk1)  # positional and default association
    clkdriver_2 = ClkDriver(clk=clk2, period=19)  # named association
    hello_1 = Hello(clk=clk1)  # named and default association
    hello_2 = Hello(to="MyHDL", clk=clk2)  # named association

    return clkdriver_1, clkdriver_2, hello_1, hello_2


inst = Greetings()
inst.run_sim(50)