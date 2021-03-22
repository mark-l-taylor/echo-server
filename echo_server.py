import socket
import sys
import traceback


def server(log_buffer=sys.stderr):
    # set an address for our server
    address = ('127.0.0.1', 10000)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    # Running an example several times with too small delay between executions, could lead to this error:
    # OSError: [Errno 98] Address already in use
    # This is because the previous execution has left the socket in a TIME_WAIT state, and can’t be immediately reused.
    # There is a socket flag to set, in order to prevent this, socket.SO_REUSEADDR

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    # bind your new sock 'sock' to the address
    sock.bind(address)
    # begin listening
    sock.listen(1)

    try:
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while True:
            print('waiting for a connection', file=log_buffer)

            # Make a new socket when a client connects
            conn, addr = sock.accept()
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                # the inner loop will receive messages sent by the client in
                # buffers.  When a complete message has been received, the
                # loop will exit
                while True:
                    # Receive 16 bytes of data from the client
                    data = conn.recv(16)
                    print('received "{0}"'.format(data.decode('utf8')))

                    # send the data back to the client
                    conn.sendall(data)
                    print('sent "{0}"'.format(data.decode('utf8')))


                    # Check if all of the data has been recieved.
                    if len(data) < 16:
                        break

            except Exception as e:
                traceback.print_exc()
                sys.exit(1)
            finally:
                # Close the connection
                conn.close()
                print(
                    'echo complete, client connection closed', file=log_buffer
                )

    except KeyboardInterrupt:
        # Close the socket
        sock.close()
        print('quitting echo server', file=log_buffer)


if __name__ == '__main__':
    server()
    sys.exit(0)
