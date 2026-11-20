# LeetCode #1279: Traffic Light Controlled Intersection -- Python mirror of
# the ★ arm: the green road behind a lock, held while a car turns its
# light green if it must and crosses; a thread for each car.
import threading
import time


class TrafficLight:
    def __init__(self):
        self.lock = threading.Lock()
        self.green = 1

    def car_arrived(self, car_id, road_id, direction, turn_green, cross_car):
        with self.lock:
            if self.green != road_id:
                turn_green()
                self.green = road_id
            cross_car()


seed = 1279


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def run(cars, directions, order):
    light = TrafficLight()
    log = []
    log_lock = threading.Lock()

    def push(event):
        with log_lock:
            log.append(event)

    def car_task(car, road, direction):
        def cross():
            push((1, car))
            time.sleep(0)
            push((2, car))
        light.car_arrived(car, road, direction, lambda: push((0, road)), cross)

    threads = []
    for i in order:
        car = cars[i]
        direction = directions[i]
        road = 1 if direction <= 2 else 2
        t = threading.Thread(target=car_task, args=(car, road, direction))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    return log


def judge(cars, directions, log):
    green = 1
    inside = [0, 0, 0]
    state = [0] * len(cars)
    for kind, x in log:
        if kind == 0:
            if x == green:
                return False
            green = x
            continue
        if x not in cars:
            return False
        i = cars.index(x)
        road = 1 if directions[i] <= 2 else 2
        if kind == 1:
            if state[i] != 0 or road != green or inside[3 - road] > 0:
                return False
            inside[road] += 1
            state[i] = 1
        else:
            if state[i] != 1:
                return False
            inside[road] -= 1
            state[i] = 2
    return all(s == 2 for s in state)


def arrival_order(times):
    order = [(times[i], next_random(), i) for i in range(len(times))]
    order.sort()
    return [i for _, _, i in order]


def b(x):
    return "true" if x else "false"


def main():
    a = run([1, 3, 5, 2, 4], [2, 1, 2, 4, 3], arrival_order([10, 20, 30, 40, 50]))
    bb = run([1, 2, 3, 4, 5], [2, 4, 3, 3, 1], arrival_order([10, 20, 30, 40, 40]))
    ok_a = judge([1, 3, 5, 2, 4], [2, 1, 2, 4, 3], a)
    ok_b = judge([1, 2, 3, 4, 5], [2, 4, 3, 3, 1], bb)
    print(f"examples: {sum(1 for k, _ in a if k == 2)} and {sum(1 for k, _ in bb if k == 2)} cars crossed, valid {b(ok_a)} {b(ok_b)}")
    cars_seen = 0
    valid = 0
    for _ in range(1000):
        n = next_random() % 20 + 1
        cars = list(range(1, n + 1))
        directions = [next_random() % 4 + 1 for _ in range(n)]
        times = sorted(next_random() % 10 for _ in range(n))
        log = run(cars, directions, arrival_order(times))
        cars_seen += sum(1 for k, _ in log if k == 2)
        if judge(cars, directions, log):
            valid += 1
    print(f"1000 random problems: {cars_seen} cars crossed, {valid} valid")
    cars = list(range(1, 21))
    verdicts = []
    for pattern in range(3):
        directions = [i % 2 + 1 if pattern == 0 else i % 2 + 3 if pattern == 1 else i % 4 + 1 for i in range(20)]
        log = run(cars, directions, arrival_order([0] * 20))
        verdicts.append(judge(cars, directions, log))
    print(f"20 cars on road A, on road B and on both: valid {b(verdicts[0])} {b(verdicts[1])} {b(verdicts[2])}")


main()
