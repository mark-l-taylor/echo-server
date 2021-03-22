import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):
    server_address = ('localhost', 10000)
    # instantiate a TCP socket with IPv4 Addressing
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)
    # Connect your socket to the server
    sock.connect(server_address)
    # you can use this variable to accumulate the entire message received back
    # from the server
    received_message = b''

    # this try/finally block exists purely to allow us to close the socket
    # when we are finished with it
    try:
        print('sending "{0}"'.format(msg), file=log_buffer)
        # send your message to the server
        sock.sendall(msg.encode('utf-8'))
        # accumulate the 16 byte chunks of data from the server
        while True:
            chunk = sock.recv(16)
            print('received "{0}"'.format(chunk.decode('utf8')), file=log_buffer)
            received_message += chunk
            if len(chunk) < 16:
                break
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    finally:
        # close the client socket
        sock.close()
        print('closing socket', file=log_buffer)

        # return the entire reply you received from the server as the return value of this function.
        print('Complete Recieved Message: {}'.format(received_message.decode('utf8')))
        return received_message.decode('utf8')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
