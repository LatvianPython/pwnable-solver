import socket
import hashlib


def connect(hostname, port):
    s = socket.socket()
    s.connect((hostname, port))
    return s


def read_until(s, marker):
    response = ''
    while True:
        received_data = s.recv(1024).decode('utf-8')
        response += received_data
        if marker in response or len(received_data) == 0:
            return response


BLOCK_SIZE = 16


def send(username, pwd):
    s = connect('pwnable.kr', 9006)
    read_until(s, 'Input your ID')
    s.send((username + '\n').encode('utf-8'))
    read_until(s, 'Input your PW')
    s.send((pwd + '\n').encode('utf-8'))
    data = read_until(s, ')')
    data = data[data.find('(') + 1:data.rfind(')')]
    response = read_until(s, 'you are not authenticated user')
    s.close()
    return data, response


def main():
    valid_chars = '_etaoinshrdlcumwfgypbvkjxqz-1234567890'
    predicted_len = 49
    guessed_cookie = ''
    found_cookie = False
    max_padding = 16 * int(50 / 16 + 1) - 4
    offset = int(max_padding / 16)
    for j in range(len(guessed_cookie), max_padding):
        if found_cookie:
            break
        encrypted_data = send('a' * (max_padding - j), 'a' * 1)[0]
        correct = encrypted_data[32 * offset: 32 + 32 * offset]

        for i in valid_chars:
            encrypted_data = send('a' * (max_padding - j), 'a-' + guessed_cookie + i)[0]
            test_data = encrypted_data[32 * offset: 32 + 32 * offset]
            if correct == test_data:
                guessed_cookie += i
                if len(guessed_cookie) == predicted_len:
                    found_cookie = True
                print('{}\r'.format(guessed_cookie), end='')
                break

    print('---------------------------------------')
    print(guessed_cookie)
    print('---------------------------------------')

    user = 'admin'
    pw = hashlib.sha256((user + guessed_cookie).encode('utf-8')).hexdigest()

    print(send(user, pw)[1])


if __name__ == '__main__':
    main()
