import imghdr
import io

# with open('test_pic.jpeg', 'rb') as pic:
with open('start.sh', 'rb') as pic:
    file = io.BytesIO(pic.read())
    print(imghdr.what(file))
    #print(pic.read().hex())
