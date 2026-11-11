// LeetCode #1116: Print Zero Even Odd -- the bench in Rust: OS threads in
// a `thread::scope`, three `sync_channel(1)`s as the ★ arm's three turn
// channels, each end behind a `Mutex` since `Receiver` is not `Sync`.

use std::sync::mpsc::{sync_channel, Receiver, SyncSender};
use std::sync::Mutex;
use std::thread;

struct Turn {
    tx: Mutex<SyncSender<()>>,
    rx: Mutex<Receiver<()>>,
}

impl Turn {
    fn new() -> Self {
        let (tx, rx) = sync_channel(1);
        Turn { tx: Mutex::new(tx), rx: Mutex::new(rx) }
    }
    fn wait(&self) {
        self.rx.lock().unwrap().recv().unwrap();
    }
    fn pass(&self) {
        self.tx.lock().unwrap().send(()).unwrap();
    }
}

struct ZeroEvenOdd {
    n: i64,
    zero_turn: Turn,
    even_turn: Turn,
    odd_turn: Turn,
}

impl ZeroEvenOdd {
    fn new(n: i64) -> Self {
        let z = ZeroEvenOdd { n, zero_turn: Turn::new(), even_turn: Turn::new(), odd_turn: Turn::new() };
        z.zero_turn.pass();
        z
    }

    fn zero(&self, print_number: impl Fn(i64)) {
        for i in 1..=self.n {
            self.zero_turn.wait();
            print_number(0);
            if i % 2 == 1 {
                self.odd_turn.pass();
            } else {
                self.even_turn.pass();
            }
        }
    }

    fn even(&self, print_number: impl Fn(i64)) {
        for i in (2..=self.n).step_by(2) {
            self.even_turn.wait();
            print_number(i);
            self.zero_turn.pass();
        }
    }

    fn odd(&self, print_number: impl Fn(i64)) {
        for i in (1..=self.n).step_by(2) {
            self.odd_turn.wait();
            print_number(i);
            self.zero_turn.pass();
        }
    }
}

fn run(n: i64, order: &[usize]) -> String {
    let log = Mutex::new(String::new());
    let z = ZeroEvenOdd::new(n);
    thread::scope(|s| {
        for &k in order {
            let (z, log) = (&z, &log);
            let say = move |x: i64| log.lock().unwrap().push_str(&x.to_string());
            match k {
                0 => s.spawn(move || z.zero(say)),
                1 => s.spawn(move || z.even(say)),
                _ => s.spawn(move || z.odd(say)),
            };
        }
    });
    log.into_inner().unwrap()
}

fn main() {
    let orders: [[usize; 3]; 6] = [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]];
    let mut want = String::new();
    for i in 1..=200 {
        want.push_str(&format!("0{}", i));
    }
    let mut right = 0;
    let mut check: i64 = 0;
    for r in 0..1000i64 {
        let out = run(200, &orders[(r % 6) as usize]);
        if out == want {
            right += 1;
        }
        check = (check * 31 + out.len() as i64 + r) % 1000000007;
    }
    println!("1000 runs over 1 to 200: {} in order, checksum {}", right, check);
}
