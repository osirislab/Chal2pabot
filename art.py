import pyfiglet
from colorama import Fore, Style

def color(s, c):
    return Fore.__dict__[c.upper()] + s + Style.RESET_ALL

plus = color('[+]', 'green')
warning = color('[*]', 'yellow')
minus = color('[-]', 'red')

def gen_ascii(message, font='slant', width=200, c=None, frame=None):
    """
    creates ascii art
    example usage:
    generate(
        'message',
        font='small',
        width=100,
        c='yellow',
        frame='blue'
    )
    :param message: message to be converted into ascii characters
    :param font: ascii art font
    :param width: size of the font
    :param c: c of the text
    :param frame: c of the frame (if none given, no frame created)
    :return: generated ascii text
    """
    raw_ascii = pyfiglet.figlet_format(message, font=font, width=width)
    split_ascii = raw_ascii.split('\n')
    if c is not None:
        for index in range(len(split_ascii)):
            split_ascii[index] = color(split_ascii[index], c=c)
    if frame is None:
        return '\n'.join(split_ascii)
    split_ascii.pop()
    horizontal_frame = color('-' * (len(split_ascii[0]) - 5), frame)
    framed_ascii_arr = [horizontal_frame]
    left_bar = color('| ', frame)
    right_bar = color(' |', frame)
    for index in range(len(split_ascii)):
        framed_ascii_arr.append(left_bar + split_ascii[index] + right_bar)
    framed_ascii_arr.append(horizontal_frame)
    return '\n'.join(framed_ascii_arr)
