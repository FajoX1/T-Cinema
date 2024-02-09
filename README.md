# T-Cinema

T-Cinema is a simple terminal-based movie server, allowing users to connect via telnet or a TCP client, choose movies from a list, and watch them in the terminal.

## Installation

1. Clone the repository to your local machine:

<code>
git clone https://github.com/fajox1/t-cinema
</code>

2. Install the required dependencies:

<code>
pip install -r requirements.txt
</code>

3. Create directory "films" and put films there

4. Open tcinema.db and put films data

4. Start the server:

<code>
python3 tcinema.py
</code>

4. Open a new terminal and connect to the server:

<code>
telnet localhost 2222
</code>

## Usage

1. Connect to the server using <code>telnet</code> or another TCP client.
2. Choose a movie from the list of available movies by entering its corresponding number.
3. Enjoy watching the movie in the terminal!

## System Requirements

- Python 3.6 and above
- Linux terminal or Windows Subsystem for Linux (WSL)

## <div align='center'>Developer - <a href="https://t.me/vecax">@fajox</a></div>