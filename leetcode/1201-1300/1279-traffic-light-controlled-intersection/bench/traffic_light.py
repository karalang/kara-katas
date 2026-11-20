# LeetCode #1279 bench, in Python: the ★ arm (the green road behind a
# lock, held while a car turns its light and crosses) over 2000 runs of 20
# cars, a thread for each car, on random roads and started in a random
# order; each run's log judged by the statement read literally.
import threading


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


def run(directions, order):
    light = TrafficLight()
    log = []
    lock = threading.Lock()

    def push(e):
        with lock:
            log.append(e)

    def task(i, road, direction):
        light.car_arrived(i, road, direction, lambda: push((0, road)), lambda: push((1, i)))

    threads = []
    for i in order:
        direction = directions[i]
        road = 1 if direction <= 2 else 2
        t = threading.Thread(target=task, args=(i, road, direction))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    return log


def judge(directions, log):
    green = 1
    crossed = [False] * len(directions)
    for kind, x in log:
        if kind == 0:
            if x == green:
                return False
            green = x
        else:
            road = 1 if directions[x] <= 2 else 2
            if road != green or crossed[x]:
                return False
            crossed[x] = True
    return all(crossed)


def main():
    cars = 0
    valid = 0
    for _ in range(2000):
        directions = [next_random() % 4 + 1 for _ in range(20)]
        order = list(range(20))
        for i in range(19, 0, -1):
            j = next_random() % (i + 1)
            order[i], order[j] = order[j], order[i]
        log = run(directions, order)
        cars += sum(1 for k, _ in log if k == 1)
        if judge(directions, log):
            valid += 1
    print(f"2000 runs of 20 cars: {cars} cars crossed, {valid} valid")


main()
