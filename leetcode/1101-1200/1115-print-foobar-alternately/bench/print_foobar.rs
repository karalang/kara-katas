// LeetCode #1115: Print FooBar Alternately -- the bench in Rust: OS
// threads in a `thread::scope`, two `sync_channel(1)`s as the ★ arm's two
// turn channels, each end behind a `Mutex` since `Receiver` is not
// `Sync`.

use std::sync::mpsc::{sync_channel, Receiver, SyncSender};
use std::sync::Mutex;
use std::thread;

struct FooBar {
    n: usize,
    foo_tx: Mutex<SyncSender<()>>,
    foo_rx: Mutex<Receiver<()>>,
    bar_tx: Mutex<SyncSender<()>>,
    bar_rx: Mutex<Receiver<()>>,
}

impl FooBar {
    fn new(n: usize) -> Self {
        let (foo_tx, foo_rx) = sync_channel(1);
        let (bar_tx, bar_rx) = sync_channel(1);
        foo_tx.send(()).unwrap();
        FooBar {
            n,
            foo_tx: Mutex::new(foo_tx),
            foo_rx: Mutex::new(foo_rx),
            bar_tx: Mutex::new(bar_tx),
            bar_rx: Mutex::new(bar_rx),
        }
    }

    fn foo(&self, print_foo: impl Fn()) {
        for _ in 0..self.n {
            self.foo_rx.lock().unwrap().recv().unwrap();
            print_foo();
            self.bar_tx.lock().unwrap().send(()).unwrap();
        }
    }

    fn bar(&self, print_bar: impl Fn()) {
        for _ in 0..self.n {
            self.bar_rx.lock().unwrap().recv().unwrap();
            print_bar();
            self.foo_tx.lock().unwrap().send(()).unwrap();
        }
    }
}

fn run(n: usize, bar_first: bool) -> String {
    let log = Mutex::new(String::new());
    let fb = FooBar::new(n);
    thread::scope(|s| {
        let (fb, log) = (&fb, &log);
        let foo = move || fb.foo(|| log.lock().unwrap().push_str("foo"));
        let bar = move || fb.bar(|| log.lock().unwrap().push_str("bar"));
        if bar_first {
            s.spawn(bar);
            s.spawn(foo);
        } else {
            s.spawn(foo);
            s.spawn(bar);
        }
    });
    log.into_inner().unwrap()
}

fn main() {
    let want = "foobar".repeat(200);
    let mut alternating = 0;
    let mut check: i64 = 0;
    for r in 0..1000i64 {
        let out = run(200, r % 2 == 1);
        if out == want {
            alternating += 1;
        }
        check = (check * 31 + out.len() as i64 + r) % 1000000007;
    }
    println!("1000 runs of 200 rounds: {} alternating, checksum {}", alternating, check);
}
