from rainbow.devices import Camera
from rainbow.graph import Session, Input, CV2Function, Selector, BufferWrite, BufferRead, BufferSetHead
from rainbow.graph import MultiBufferWrite, MultiBufferRead, MultiBufferSetHeads
from rainbow.buffering import Buffer, MultiBuffer

import cv2
import numpy as np


def gray_graph():
    camera = Camera(0)
    gray_function = lambda im: cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # Define operations
    camera_op = Input(camera)
    gray_op = CV2Function(gray_function)

    # Chain operations
    _input = camera_op()
    gray = gray_op(_input)

    # Define output
    final_ops = [gray]
    return final_ops

def channel_delay_graph():
    camera = Camera(0)
    buffer_b = Buffer(360)
    buffer_g = Buffer(360)
    buffer_r = Buffer(360)
    split_function = lambda im: cv2.split(im)
    merge_function = lambda b, g, r: cv2.merge((b, g, r))
    hflip = lambda im: cv2.flip(im, 1)

    # Define operations
    camera_op = Input(camera)
    hflip_op = CV2Function(hflip)
    split_op = CV2Function(split_function)

    select_b_op = Selector(0)
    write_b_op = BufferWrite(buffer_b)
    set_head_b_op = BufferSetHead(buffer_b, lambda: 0)
    read_b_op = BufferRead(buffer_b)

    select_g_op = Selector(1)
    write_g_op = BufferWrite(buffer_g)
    set_head_g_op = BufferSetHead(buffer_g, lambda: 5)
    read_g_op = BufferRead(buffer_g)

    select_r_op = Selector(2)
    write_r_op = BufferWrite(buffer_r)
    set_head_r_op = BufferSetHead(buffer_r, lambda: 10)
    read_r_op = BufferRead(buffer_r)

    merge_op = CV2Function(merge_function)

    # Chain operations
    _input = camera_op()
    hflip = hflip_op(_input)
    split = split_op(hflip)
    select_b = select_b_op(split)
    select_g = select_g_op(split)
    select_r = select_r_op(split)

    write_b = write_b_op(select_b)
    write_g = write_g_op(select_g)
    write_r = write_r_op(select_r)

    set_head_b = set_head_b_op(write_b)
    set_head_g = set_head_g_op(write_g)
    set_head_r = set_head_r_op(write_r)

    read_b = read_b_op(set_head_b)
    read_g = read_g_op(set_head_g)
    read_r = read_r_op(set_head_r)

    merge = merge_op([read_b, read_g, read_r])

    final_ops = [merge]
    return final_ops

def pixelbuffer_delays():
    # Functions
    camera = Camera(0)
    resolution = (320,240)
    camera.set_resolution(*resolution)
    n_pixels = resolution[0] * resolution[1]

    random_kernel = np.random.randint(0,3, n_pixels)
    set_heads_function = lambda: random_kernel
    split_function = lambda im: [pix for pix in im.reshape((-1, 3))]
    concat_function = lambda a: np.array(a).reshape(resolution[::-1] + (3,))

    buffers = MultiBuffer(n_pixels, 100)

    # Operations
    camera_op = Input(camera)
    split_op = CV2Function(split_function)
    write_op = MultiBufferWrite(buffers)
    set_head_op = MultiBufferSetHeads(buffers, set_heads_function)
    read_op = MultiBufferRead(buffers)
    concat_op = CV2Function(concat_function)

    # Chain
    _input = camera_op()
    split = split_op(_input)
    write = write_op(split)
    set_head = set_head_op(write)
    read = read_op(set_head)
    concat = concat_op(read)

    final_ops = [concat]
    return final_ops


def display_session(session):
    for result in session:
        # Display the resulting frame
        im = result[0]
        cv2.imshow('frame', im)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

"""
TODO:
- Per-pixel frame buffer with individual time delays
- - Time delays are related to neighboring pixels'
"""

if __name__ == '__main__':
    # outputs = gray_graph()
    # outputs = channel_delay_graph()
    outputs = pixelbuffer_delays()
    session = Session(outputs)
    display_session(session)