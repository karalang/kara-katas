// LeetCode #1195 bench: the ★ arm in Rust, over the same 3 runs of
// n = 200000 as the Kāra bench. Rust's standard library has no semaphore,
// so each is a count under a `Mutex` with a `Condvar`.

use std::sync::{Condvar, Mutex};
use std::thread;

struct Semaphore {
    permits: Mutex<i64>,
    freed: Condvar,
}

impl Semaphore {
    fn new(permits: i64) -> Semaphore {
        Semaphore { permits: Mutex::new(permits), freed: Condvar::new() }
    }

    fn acquire(&self) {
        let mut p = self.permits.lock().unwrap();
        while *p == 0 {
            p = self.freed.wait(p).unwrap();
        }
        *p -= 1;
    }

    fn release(&self) {
        *self.permits.lock().unwrap() += 1;
        self.freed.notify_one();
    }
}

struct FizzBuzz {
    n: i64,
    fizz_turn: Semaphore,
    buzz_turn: Semaphore,
    fizzbuzz_turn: Semaphore,
    number_turn: Semaphore,
}

impl FizzBuzz {
    fn new(n: i64) -> FizzBuzz {
        FizzBuzz {
            n,
            fizz_turn: Semaphore::new(0),
            buzz_turn: Semaphore::new(0),
            fizzbuzz_turn: Semaphore::new(0),
            number_turn: Semaphore::new(1),
        }
    }

    fn pass(&self, i: i64) {
        if i > self.n {
            return;
        }
        if i % 15 == 0 {
            self.fizzbuzz_turn.release();
        } else if i % 3 == 0 {
            self.fizz_turn.release();
        } else if i % 5 == 0 {
            self.buzz_turn.release();
        } else {
            self.number_turn.release();
        }
    }

    fn fizz(&self, print_fizz: impl Fn()) {
        for i in 1..=self.n {
            if i % 3 == 0 && i % 5 != 0 {
                self.fizz_turn.acquire();
                print_fizz();
                self.pass(i + 1);
            }
        }
    }

    fn buzz(&self, print_buzz: impl Fn()) {
        for i in 1..=self.n {
            if i % 5 == 0 && i % 3 != 0 {
                self.buzz_turn.acquire();
                print_buzz();
                self.pass(i + 1);
            }
        }
    }

    fn fizzbuzz(&self, print_fizzbuzz: impl Fn()) {
        for i in 1..=self.n {
            if i % 15 == 0 {
                self.fizzbuzz_turn.acquire();
                print_fizzbuzz();
                self.pass(i + 1);
            }
        }
    }

    fn number(&self, print_number: impl Fn(i64)) {
        for i in 1..=self.n {
            if i % 3 != 0 && i % 5 != 0 {
                self.number_turn.acquire();
                print_number(i);
                self.pass(i + 1);
            }
        }
    }
}

fn run(n: i64, order: &[i64]) -> Vec<String> {
    let fb = FizzBuzz::new(n);
    let out: Mutex<Vec<String>> = Mutex::new(Vec::new());
    thread::scope(|s| {
        for &role in order {
            let (fb, out) = (&fb, &out);
            match role {
                0 => s.spawn(move || fb.fizz(|| out.lock().unwrap().push("fizz".to_string()))),
                1 => s.spawn(move || fb.buzz(|| out.lock().unwrap().push("buzz".to_string()))),
                2 => s.spawn(move || fb.fizzbuzz(|| out.lock().unwrap().push("fizzbuzz".to_string()))),
                _ => s.spawn(move || fb.number(|i| out.lock().unwrap().push(i.to_string()))),
            };
        }
    });
    out.into_inner().unwrap()
}

fn main() {
    let mut check: i64 = 0;
    for order in [[0, 1, 2, 3], [3, 2, 1, 0], [1, 3, 0, 2]] {
        for line in run(200000, &order) {
            for b in line.bytes() {
                check = (check * 131 + b as i64) % 1000000007;
            }
            check = (check * 131 + 10) % 1000000007;
        }
    }
    println!("3 runs of n = 200000: checksum {check}");
}
