import serial
from time import sleep
import os

# connect to the 3D printer
def connect(port = '/dev/ttyACM0', baud_rate=115200):

    # open the serial connection
    ser = serial.Serial(port,baud_rate)
    sleep(2)

    # check if the connection is successful


    # return the connection object
    return ser

# get all of the files in the target folder
def get_files():
    path = os.path.join(os.getcwd(), "files")

    return next(os.walk(path)[2])


def enumerate_selection(files):

    print("SELECT A FILE")

    for i,f in enumerate(files):
        print("\t", i, ": ", f)

    try:
        index = int(input("ENTER SELECTION"))
        
    except:
        print("ERROR - invalid input")


def main():

    # make the serial connection
    connect()


    

    # read the input file
    file = open(,'r')





    






if __name__ == "__main__":
    main()