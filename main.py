import os
import multiprocessing


def process1():
    from task1 import main
    print("ID of process running process1: {}".format(os.getpid()))
    main()


def process2():
    from task2 import main
    print("ID of process running process2: {}".format(os.getpid()))
    main()


if __name__ == "__main__":
    # printing main program process id
    print("ID of main process: {}".format(os.getpid()))

    # creating processes
    p1 = multiprocessing.Process(target=process1)
    p2 = multiprocessing.Process(target=process2)

    # starting processes
    p1.start()
    p2.start()

    # wait until processes are finished
    p1.join()
    p2.join()

    print("finished main process")
