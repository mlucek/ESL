#example 1

# import random
# from myhdl import block, instance, Signal, intbv, delay, always_comb
#
#
# @block
# def mux(z, a, b, sel):
#
#     """ Multiplexer.
#
#     z -- mux output
#     a, b -- data inputs
#     sel -- control input: select a if asserted, otherwise b
#
#     """
#
#     @always_comb
#     def comb():
#         if sel == 1:
#             z.next = a
#         else:
#             z.next = b
#
#     return comb
#
#
# random.seed(5)
# randrange = random.randrange
#
# @block
# def test_mux():
#
#     z, a, b, sel = [Signal(intbv(0)) for i in range(4)]
#
#     mux_1 = mux(z, a, b, sel)
#
#     @instance
#     def stimulus():
#         print("z a b sel")
#         for i in range(12):
#             a.next, b.next, sel.next = randrange(8), randrange(8), randrange(2)
#             yield delay(10)
#             print("%s %s %s %s" % (z, a, b, sel))
#
#     return mux_1, stimulus
#
# tb = test_mux()
# tb.run_sim()

#Example 2


# import random
# from myhdl import block, always, instance, Signal, \
#     ResetSignal, modbv, delay, StopSimulation, always_seq
#
#
#
# @block
# def inc(count, enable, clock, reset):
#     """ Incrementer with enable.
#
#     count -- output
#     enable -- control input, increment when 1
#     clock -- clock input
#     reset -- asynchronous reset input
#     """
#
#     @always_seq(clock.posedge, reset=reset)
#     def seq():
#         if enable:
#             count.next = count + 1
#
#     return seq
#
# random.seed(1)
# randrange = random.randrange
#
# ACTIVE_LOW, INACTIVE_HIGH = 0, 1
#
# @block
# def testbench():
#     m = 3
#     count = Signal(modbv(0)[m:])
#     enable = Signal(bool(0))
#     clock  = Signal(bool(0))
#     reset = ResetSignal(0, active=0, isasync=True)
#
#     inc_1 = inc(count, enable, clock, reset)
#
#     HALF_PERIOD = delay(10)
#
#     @always(HALF_PERIOD)
#     def clockGen():
#         clock.next = not clock
#
#     @instance
#     def stimulus():
#         reset.next = ACTIVE_LOW
#         yield clock.negedge
#         reset.next = INACTIVE_HIGH
#         for i in range(16):
#             enable.next = min(1, randrange(3))
#             yield clock.negedge
#         raise StopSimulation()
#
#     @instance
#     def monitor():
#         print("enable  count")
#         yield reset.posedge
#         while 1:
#             yield clock.posedge
#             yield delay(1)
#             print("   %s      %s" % (int(enable), count))
#
#     return clockGen, stimulus, inc_1, monitor
#
# tb = testbench()
# tb.run_sim()

#Example 3

from myhdl import block, always, instance, Signal, ResetSignal, delay, StopSimulation, always_seq, intbv, enum


ACTIVE_LOW = 0
FRAME_SIZE = 8
t_state = enum('SEARCH', 'CONFIRM', 'SYNC')

@block
def framer_ctrl(sof, state, sync_flag, clk, reset_n):

    """ Framing control FSM.

    sof -- start-of-frame output bit
    state -- FramerState output
    sync_flag -- sync pattern found indication input
    clk -- clock input
    reset_n -- active low reset

    """

    index = Signal(intbv(0, min=0, max=FRAME_SIZE)) # position in frame

    @always_seq(clk.posedge, reset=reset_n)
    def FSM():
        if reset_n == ACTIVE_LOW:
            sof.next = 0
            index.next = 0
            state.next = t_state.SEARCH

        else:
            index.next = (index + 1) % FRAME_SIZE
            sof.next = 0

            if state == t_state.SEARCH:
                index.next = 1
                if sync_flag:
                    state.next = t_state.CONFIRM

            elif state == t_state.CONFIRM:
                if index == 0:
                    if sync_flag:
                        state.next = t_state.SYNC
                    else:
                        state.next = t_state.SEARCH

            elif state == t_state.SYNC:
                if index == 0:
                    if not sync_flag:
                        state.next = t_state.SEARCH
                sof.next = (index == FRAME_SIZE-1)

            else:
                raise ValueError("Undefined state")

    return FSM


ACTIVE_LOW = 0

@block
def testbench():

    sof = Signal(bool(0))
    sync_flag = Signal(bool(0))
    clk = Signal(bool(0))
    reset_n = ResetSignal(1, active=ACTIVE_LOW, isasync=True)
    state = Signal(t_state.SEARCH)

    frame_ctrl_0 = framer_ctrl(sof, state, sync_flag, clk, reset_n)

    @always(delay(10))
    def clkgen():
        clk.next = not clk

    @instance
    def stimulus():
        for i in range(3):
            yield clk.negedge
        for n in (12, 8, 8, 4):
            sync_flag.next = 1
            yield clk.negedge
            sync_flag.next = 0
            for i in range(n-1):
                yield clk.negedge
        raise StopSimulation()

    return frame_ctrl_0, clkgen, stimulus

tb = testbench()
tb.config_sim(trace=True)
tb.run_sim()