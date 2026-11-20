// LeetCode #1226 bench: the ★ arm in Rust over the same 3 runs of n = 50000
// as the Kāra bench: an OS thread per philosopher, a `Mutex` for each fork,
// the lower-numbered fork taken first, the log under its own `Mutex`.
use std::sync::Mutex;
use std::thread;

struct DiningPhilosophers {
    forks: Vec<Mutex<i64>>,
}

impl DiningPhilosophers {
    fn new() -> DiningPhilosophers {
        DiningPhilosophers { forks: (0..5).map(|_| Mutex::new(0)).collect() }
    }

    fn wants_to_eat(
        &self,
        philosopher: usize,
        pick_left_fork: impl Fn(),
        pick_right_fork: impl Fn(),
        eat: impl Fn(),
        put_left_fork: impl Fn(),
        put_right_fork: impl Fn(),
    ) {
        let left = philosopher;
        let right = (philosopher + 4) % 5;
        let _first = self.forks[left.min(right)].lock().unwrap();
        let _second = self.forks[left.max(right)].lock().unwrap();
        pick_left_fork();
        pick_right_fork();
        eat();
        put_left_fork();
        put_right_fork();
    }
}

fn run(n: i64, order: &[usize]) -> Vec<(usize, i64, i64)> {
    let table = DiningPhilosophers::new();
    let log: Mutex<Vec<(usize, i64, i64)>> = Mutex::new(Vec::new());
    thread::scope(|s| {
        for &p in order {
            let (table, log) = (&table, &log);
            s.spawn(move || {
                for _ in 0..n {
                    table.wants_to_eat(
                        p,
                        || log.lock().unwrap().push((p, 1, 1)),
                        || log.lock().unwrap().push((p, 2, 1)),
                        || log.lock().unwrap().push((p, 0, 3)),
                        || log.lock().unwrap().push((p, 1, 2)),
                        || log.lock().unwrap().push((p, 2, 2)),
                    );
                }
            });
        }
    });
    log.into_inner().unwrap()
}

fn judge(n: i64, log: &[(usize, i64, i64)]) -> String {
    let mut holder = [-1i64; 5];
    let mut meals = [0i64; 5];
    for &(p, fork, op) in log {
        let f = if fork == 1 { p } else { (p + 4) % 5 };
        if op == 1 {
            if holder[f] != -1 {
                return format!("philosopher {p} picks up fork {f}, held by {}", holder[f]);
            }
            holder[f] = p as i64;
        } else if op == 2 {
            if holder[f] != p as i64 {
                return format!("philosopher {p} puts down fork {f}, not holding it");
            }
            holder[f] = -1;
        } else {
            if holder[p] != p as i64 || holder[(p + 4) % 5] != p as i64 {
                return format!("philosopher {p} eats without both forks");
            }
            meals[p] += 1;
        }
    }
    if meals.iter().any(|&m| m != n) {
        return format!("meals {meals:?}");
    }
    if holder.iter().any(|&h| h != -1) {
        return format!("forks left held {holder:?}");
    }
    "valid".to_string()
}

fn main() {
    let mut calls = 0;
    let mut valid = 0;
    for order in [[0, 1, 2, 3, 4], [4, 3, 2, 1, 0], [2, 0, 4, 1, 3]] {
        let log = run(50000, &order);
        calls += log.len();
        if judge(50000, &log) == "valid" {
            valid += 1;
        }
    }
    println!("3 runs of n = 50000: {calls} calls, {valid} valid");
}
