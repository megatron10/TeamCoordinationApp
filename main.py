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


def process3():
    from task3 import main

    print("ID of process running process3: {}".format(os.getpid()))
    main()


def process4():
    from task4 import main

    print("ID of process running process4: {}".format(os.getpid()))
    main()


def process5():
    from task5 import main

    print("ID of process running process5: {}".format(os.getpid()))
    main()


def process6():
    from task6 import main

    print("ID of process running process6: {}".format(os.getpid()))
    main()


if __name__ == "__main__":
    # printing main program process id
    print("ID of main process: {}".format(os.getpid()))

    # creating processes
    p1 = multiprocessing.Process(target=process1)
    p2 = multiprocessing.Process(target=process2)
    p3 = multiprocessing.Process(target=process3)
    p4 = multiprocessing.Process(target=process4)
    p5 = multiprocessing.Process(target=process5)
    p6 = multiprocessing.Process(target=process6)

    # starting processes
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()

    # wait until processes are finished
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()

    print("finished main process")
