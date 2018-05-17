import threading
import time


def sum_double(num_list):
    s = 0
    for num in num_list:
        s = num * 2
    print("sum_double done with sum:", s)


def sum_square(num_list):
    s = 0
    for num in num_list:
        s += num * num
    print("sum_square done with sum:", s)


def main():
    num_list = list(range(10000000))

    print("WITHOUT THREADING\n")

    t1 = time.time()
    print("Start time: ", t1)

    sum_double(num_list)    # 01
    sum_double(num_list)    # 02
    sum_double(num_list)    # 03
    sum_double(num_list)    # 04
    sum_double(num_list)    # 05
    sum_double(num_list)    # 06
    sum_double(num_list)    # 07
    sum_double(num_list)    # 08
    sum_double(num_list)    # 09
    sum_double(num_list)    # 10

    sum_square(num_list)    # 01
    sum_square(num_list)    # 02
    sum_square(num_list)    # 03
    sum_square(num_list)    # 04
    sum_square(num_list)    # 05
    sum_square(num_list)    # 06
    sum_square(num_list)    # 07
    sum_square(num_list)    # 08
    sum_square(num_list)    # 09
    sum_square(num_list)    # 10

    t2 = time.time()
    print("Finish time: ", t2)

    print("\nNOW WITH THREADING\n")

    thr_d1 = threading.Thread(target=sum_double, args=(num_list,))
    thr_d2 = threading.Thread(target=sum_double, args=(num_list,))
    thr_d3 = threading.Thread(target=sum_double, args=(num_list,))
    thr_d4 = threading.Thread(target=sum_double, args=(num_list,))
    thr_d5 = threading.Thread(target=sum_double, args=(num_list,))
    thr_d6 = threading.Thread(target=sum_double, args=(num_list,))
    thr_d7 = threading.Thread(target=sum_double, args=(num_list,))
    thr_d8 = threading.Thread(target=sum_double, args=(num_list,))
    thr_d9 = threading.Thread(target=sum_double, args=(num_list,))
    thr_d10 = threading.Thread(target=sum_double, args=(num_list,))

    thr_s1 = threading.Thread(target=sum_square, args=(num_list,))
    thr_s2 = threading.Thread(target=sum_square, args=(num_list,))
    thr_s3 = threading.Thread(target=sum_square, args=(num_list,))
    thr_s4 = threading.Thread(target=sum_square, args=(num_list,))
    thr_s5 = threading.Thread(target=sum_square, args=(num_list,))
    thr_s6 = threading.Thread(target=sum_square, args=(num_list,))
    thr_s7 = threading.Thread(target=sum_square, args=(num_list,))
    thr_s8 = threading.Thread(target=sum_square, args=(num_list,))
    thr_s9 = threading.Thread(target=sum_square, args=(num_list,))
    thr_s10 = threading.Thread(target=sum_square, args=(num_list,))

    t3 = time.time()
    print("Start time: ", t3)

    thr_d1.run()
    thr_d2.run()
    thr_d3.run()
    thr_d4.run()
    thr_d5.run()
    thr_d6.run()
    thr_d7.run()
    thr_d8.run()
    thr_d9.run()
    thr_d10.run()

    thr_s1.run()
    thr_s2.run()
    thr_s3.run()
    thr_s4.run()
    thr_s5.run()
    thr_s6.run()
    thr_s7.run()
    thr_s8.run()
    thr_s9.run()
    thr_s10.run()

    t4 = time.time()
    print("Finish time: ", t4)

    print("\n")

    print("Normally time needed: ", t2 - t1)
    print("Threading time needed: ", t4 - t3)


if __name__ == '__main__':
    main()