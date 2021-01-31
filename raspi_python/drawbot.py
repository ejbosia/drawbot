import serial
from time import sleep
import os


# connect to the 3D printer
def connect(port = '/dev/ttyUSB0', baud_rate=115200):

    # open the serial connection
    ser = serial.Serial(port,baud_rate)
    sleep(2)

    # check if the connection is successful
    print(ser.name)

    # return the connection object
    return ser


# get all of the files in the target folder
def get_files():

    return next(os.walk(path)[2])


# allow the user to select a file
def enumerate_selection(items):


    for i,item in enumerate(items):
        print("\t", i, ": ", item)

    index = int(input("ENTER SELECTION"))

    print("SELECTED:", item[i])

    return i


def main():

    # make the serial connection
    ser = connect()

    # select a file
    files = next(os.walk("files"))[2]
    index = enumerate_selection()

    # read the input file
    file = open(files[index],'r')

    # send the file to print
    for line in file:
        print(line)
        ser.write((line+"\n").encode('utf-8'))


    ser.close()
    file.close()



if __name__ == "__main__":
    main()