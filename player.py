import asyncio
import imageio
import numpy as np
from PIL import Image

async def rgb_to_ascii(frame):
    ascii_frame = []
    for row in frame:
        ascii_row = []
        for pixel in row:
            r, g, b = pixel[:3]
            ascii_char = "  "
            ascii_row.append(f"\033[48;2;{r};{g};{b}m{ascii_char}\033[0m")
        ascii_frame.append(ascii_row)
    return np.array(ascii_frame)

async def resize_frame(frame, new_width):
    ratio = min(new_width / frame.shape[1], 1)
    new_height = int(frame.shape[0] * ratio)
    return np.array(Image.fromarray(frame).resize((new_width, new_height)))

async def play_video(file, channel):
    new_width = 53
    reader = imageio.get_reader('./films/' + file)
    try:
        channel.send('\x1b[2J\x1b[H'.encode())
        for frame in reader:
            resized_frame = await resize_frame(frame, new_width=new_width)
            ascii_frame = await rgb_to_ascii(resized_frame)
            channel.send('\x1b[H'.encode())
            for row in ascii_frame:
                channel.send(''.join(row).encode())
                channel.send('\r\n'.encode())
            await asyncio.sleep(1/55)
    except KeyboardInterrupt:
        pass
    finally:
        reader.close()
