# Example 1
#
# from myhdl import block, Signal
#
# @block
# def top():
#
#     din = Signal(0)
#     dout = Signal(0)
#     clk = Signal(bool(0))
#     reset = Signal(bool(0))
#
#     channel_inst = channel(dout, din, clk, reset)
#
#     return channel_inst


# Example 2

from myhdl import block, Signal

@block
def top(n=8):

    din = [Signal(0) for i in range(n)]
    dout = [Signal(0) for j in range(n)]
    clk = Signal(bool(0))
    reset = Signal(bool(0))
    channel_inst = [None for i in range(n)]

    for i in range(n):
        channel_inst[i] = channel(dout[i], din[i], clk, reset)

    return channel_inst