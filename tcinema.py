import asyncio
import socket
import aiohttp
import films
from player import play_video

tg_id = "" # Your telegram id for logs
bot_token = "" # your bot token from t.me/botfather. Just for log visiting

ip = "localhost" # don't change if you are testing on your computer
port = 2222

async def handle_client(conn, addr):
    try:
        async with aiohttp.ClientSession() as session:
            await session.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                params={
                    "chat_id": {tg_id},
                    "text": f"""<b>👁 New visitor\n\nIP: <code>{addr[0]}</code></b>""",
                    "parse_mode": "HTML"
                }
            )
    except:
        print("Can't send log message")
    print(f"Установлено соединение с {addr[0]}")
    conn.send("\x1b[2J\x1b[H".encode())
    conn.send(f"""\033[1mWelcome to\033[0m
  _____        ____   ___   _   _   _____   __  __      _    
 |_   _|      / ___| |_ _| | \ | | | ____| |  \/  |    / \   
   | |       | |      | |  |  \| | |  _|   | |\/| |   / _ \  
   | |    _  | |___   | |  | |\  | | |___  | |  | |  / ___ \ 
   |_|   (_)  \____| |___| |_| \_| |_____| |_|  |_| /_/   \_\ \n\n\n\r""".encode())

    conn.send("\033[91;1mWE SUPPORT ONLY LINUX TERMINALS OR WSL!!!\033[0m\n\n\r".encode())

    conn.send(f"Movies available:\n\n\r".encode())

    movies = await films.get_all()

    max_length = max(len(movie[1]) for movie in movies) + 3

    num_movies = len(movies)
    num_columns = 2
    movies_per_column = (num_movies + num_columns - 1) // num_columns

    for index in range(num_movies):
        movie_number = f"{index + 1}."
        movie_title = movies[index][1].ljust(max_length)
        formatted_movie = f"{movie_number} \033[1;36m{movie_title}\033[0m"

        column = index // movies_per_column

        conn.send(formatted_movie.ljust(max_length * num_columns).encode())

        if (index + 1) % movies_per_column == 0 or index == num_movies - 1:
            conn.send("\n\r".encode())

    while True:
        conn.send("\nEnter movie number to watch: ".encode())
        movie = await asyncio.to_thread(conn_makefile_readline, conn)
        movie = movie.strip()

        try:
            m = int(movie)
            if 0 < m < len(movies) + 1:
                break
        except:
            conn.send("Please enter correct!\r".encode())

    conn.send("\nStarts in:\n\r".encode())

    for i in range(5):
        conn.send((str(5 - i) + "...\n\r").encode())
        await asyncio.sleep(1)

    conn.send("\nLoading...\r".encode())

    await play_video(movies[int(movie) - 1][2], conn)
    conn.close()

def conn_makefile_readline(conn):
    f = conn.makefile("r")
    return f.readline()

async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)

    print(f"Server started!\nPort: {port}")

    loop = asyncio.get_event_loop()
    while True:
        conn, addr = await loop.sock_accept(server_socket)
        loop.create_task(handle_client(conn, addr))

if __name__ == "__main__":
    asyncio.run(main())
