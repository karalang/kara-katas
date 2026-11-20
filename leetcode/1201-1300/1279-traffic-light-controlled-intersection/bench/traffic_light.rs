// LeetCode #1279 bench, in Rust: the ★ arm (the green road behind a
// `Mutex`, held while a car turns its light and crosses) over 2000 runs of
// 20 cars, a thread for each car, on random roads and started in a random
// order; each run's log judged by the statement read literally.

use std::sync::Mutex;
use std::thread;

struct TrafficLight {
    green: Mutex<i64>,
}

impl TrafficLight {
    fn new() -> Self {
        TrafficLight { green: Mutex::new(1) }
    }

    fn car_arrived(&self, _car_id: i64, road_id: i64, _direction: i64, turn_green: impl Fn(), cross_car: impl Fn()) {
        let mut g = self.green.lock().unwrap();
        if *g != road_id {
            turn_green();
            *g = road_id;
        }
        cross_car();
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn run(directions: &[i64], order: &[usize]) -> Vec<(i64, i64)> {
    let light = TrafficLight::new();
    let log: Mutex<Vec<(i64, i64)>> = Mutex::new(Vec::new());
    thread::scope(|s| {
        for &i in order {
            let direction = directions[i];
            let road = if direction <= 2 { 1 } else { 2 };
            let (light, log) = (&light, &log);
            s.spawn(move || {
                light.car_arrived(i as i64, road, direction, || log.lock().unwrap().push((0, road)), || log.lock().unwrap().push((1, i as i64)));
            });
        }
    });
    log.into_inner().unwrap()
}

fn judge(directions: &[i64], log: &[(i64, i64)]) -> bool {
    let mut green = 1;
    let mut crossed = vec![false; directions.len()];
    for &(kind, x) in log {
        if kind == 0 {
            if x == green {
                return false;
            }
            green = x;
        } else {
            let x = x as usize;
            let road = if directions[x] <= 2 { 1 } else { 2 };
            if road != green || crossed[x] {
                return false;
            }
            crossed[x] = true;
        }
    }
    crossed.iter().all(|&c| c)
}

fn main() {
    let mut seed = 1279i64;
    let mut cars = 0;
    let mut valid = 0;
    for _ in 0..2000 {
        let directions: Vec<i64> = (0..20).map(|_| next_random(&mut seed) % 4 + 1).collect();
        let mut order: Vec<usize> = (0..20).collect();
        for i in (1..20).rev() {
            let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
            order.swap(i, j);
        }
        let log = run(&directions, &order);
        cars += log.iter().filter(|&&(k, _)| k == 1).count();
        if judge(&directions, &log) {
            valid += 1;
        }
    }
    println!("2000 runs of 20 cars: {} cars crossed, {} valid", cars, valid);
}
