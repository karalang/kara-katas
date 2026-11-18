// LeetCode #1188: Design Bounded Blocking Queue -- the bench in Rust: the ★
// arm's two counting semaphores and a lock. Rust's standard library has no
// semaphore, so each is a count under a `Mutex` with a `Condvar`.

use std::collections::VecDeque;
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

struct BoundedBlockingQueue {
    slots: Semaphore,
    items: Semaphore,
    values: Mutex<VecDeque<i64>>,
}

impl BoundedBlockingQueue {
    fn new(capacity: i64) -> BoundedBlockingQueue {
        BoundedBlockingQueue {
            slots: Semaphore::new(capacity),
            items: Semaphore::new(0),
            values: Mutex::new(VecDeque::new()),
        }
    }

    fn enqueue(&self, element: i64) {
        self.slots.acquire();
        self.values.lock().unwrap().push_back(element);
        self.items.release();
    }

    fn dequeue(&self) -> i64 {
        self.items.acquire();
        let element = self.values.lock().unwrap().pop_front().unwrap();
        self.slots.release();
        element
    }

    fn size(&self) -> i64 {
        self.values.lock().unwrap().len() as i64
    }
}

fn run(round: i64) -> i64 {
    let queue = BoundedBlockingQueue::new(16);
    let total = Mutex::new(0i64);
    thread::scope(|s| {
        for p in 0..4i64 {
            let queue = &queue;
            s.spawn(move || {
                for k in 0..2500i64 {
                    queue.enqueue((round * 7919 + p * 10007 + k * 31) % 1000);
                }
            });
        }
        for _ in 0..4 {
            let (queue, total) = (&queue, &total);
            s.spawn(move || {
                let mut sum = 0;
                for _ in 0..2500 {
                    sum += queue.dequeue();
                }
                *total.lock().unwrap() += sum;
            });
        }
    });
    let sum = *total.lock().unwrap();
    sum + 1000 * queue.size()
}

fn main() {
    let rounds = 100;
    let mut check: i64 = 0;
    for round in 0..rounds {
        check = (check * 131 + run(round)) % 1000000007;
    }
    println!("{} rounds of 4 producers and 4 consumers moving 10000 values through 16 places: checksum {}", rounds, check);
}
