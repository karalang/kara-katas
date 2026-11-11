// LeetCode #1114: Print in Order -- the bench in Rust: OS threads in a
// `thread::scope`, two `mpsc` channels as the ★ arm's two one-shot
// channels, each end behind a `Mutex` since `Receiver` is not `Sync`.

use std::sync::mpsc::{channel, Receiver, Sender};
use std::sync::Mutex;
use std::thread;

struct Foo {
    first_tx: Mutex<Sender<()>>,
    first_rx: Mutex<Receiver<()>>,
    second_tx: Mutex<Sender<()>>,
    second_rx: Mutex<Receiver<()>>,
}

impl Foo {
    fn new() -> Self {
        let (first_tx, first_rx) = channel();
        let (second_tx, second_rx) = channel();
        Foo {
            first_tx: Mutex::new(first_tx),
            first_rx: Mutex::new(first_rx),
            second_tx: Mutex::new(second_tx),
            second_rx: Mutex::new(second_rx),
        }
    }

    fn first(&self, print_first: impl Fn()) {
        print_first();
        self.first_tx.lock().unwrap().send(()).unwrap();
    }

    fn second(&self, print_second: impl Fn()) {
        self.first_rx.lock().unwrap().recv().unwrap();
        print_second();
        self.second_tx.lock().unwrap().send(()).unwrap();
    }

    fn third(&self, print_third: impl Fn()) {
        self.second_rx.lock().unwrap().recv().unwrap();
        print_third();
    }
}

fn run(nums: &[i64]) -> String {
    let log = Mutex::new(String::new());
    let foo = Foo::new();
    thread::scope(|s| {
        for &k in nums {
            let (foo, log) = (&foo, &log);
            match k {
                1 => s.spawn(move || foo.first(|| log.lock().unwrap().push_str("first"))),
                2 => s.spawn(move || foo.second(|| log.lock().unwrap().push_str("second"))),
                _ => s.spawn(move || foo.third(|| log.lock().unwrap().push_str("third"))),
            };
        }
    });
    log.into_inner().unwrap()
}

fn main() {
    let orders: [[i64; 3]; 6] = [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]];
    let mut in_order = 0;
    let mut check: i64 = 0;
    for r in 0..10000 {
        let out = run(&orders[r * 7 % 6]);
        if out == "firstsecondthird" {
            in_order += 1;
        }
        check = (check * 31 + out.len() as i64) % 1000000007;
    }
    println!("10000 runs: {} printed in order, checksum {}", in_order, check);
}
