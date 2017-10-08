import array

from ola.ClientWrapper import ClientWrapper

wrapper = None
loop_count = 0
TICK_INTERVAL = 1200  # in ms


def DmxSent(state):
    if not state.Succeeded():
        wrapper.Stop()


def SendDMXFrame():
    wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)

    # compute frame here
    data = array.array('B')
    global loop_count
    data.extend([loop_count % 255, loop_count % 255, loop_count % 255])
    loop_count += 1

    # send
    wrapper.Client().SendDmx(1, data, DmxSent)


wrapper = ClientWrapper()
wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)
wrapper.Run()
