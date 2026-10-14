// LeetCode #622: Design Circular Queue -- Rust mirror of the Kāra bench.
//
// The ★ arm's ring with a start and a count, on the same script and
// queues.

struct MyCircularQueue {
    data: Vec<i64>,
    head: i64,
    count: i64,
}

impl MyCircularQueue {
    fn new(k: i64) -> MyCircularQueue {
        MyCircularQueue { data: vec![0; k as usize], head: 0, count: 0 }
    }

    fn en_queue(&mut self, value: i64) -> bool {
        if self.count == self.data.len() as i64 {
            return false;
        }
        let at = (self.head + self.count) % self.data.len() as i64;
        self.data[at as usize] = value;
        self.count += 1;
        true
    }

    fn de_queue(&mut self) -> bool {
        if self.count == 0 {
            return false;
        }
        self.head = (self.head + 1) % self.data.len() as i64;
        self.count -= 1;
        true
    }

    fn front(&self) -> i64 {
        if self.count == 0 { -1 } else { self.data[self.head as usize] }
    }

    fn rear(&self) -> i64 {
        if self.count == 0 {
            -1
        } else {
            self.data[((self.head + self.count - 1) % self.data.len() as i64) as usize]
        }
    }

    fn is_empty(&self) -> bool {
        self.count == 0
    }

    fn is_full(&self) -> bool {
        self.count == self.data.len() as i64
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn script(count: i64, seed: &mut i64) -> Vec<i64> {
    let mut ops = Vec::new();
    for _ in 0..count {
        let roll = next_random(seed) % 40;
        if roll < 16 {
            ops.push(next_random(seed) % 1001);
        } else if roll < 26 {
            ops.push(-1);
        } else if roll < 30 {
            ops.push(-2);
        } else if roll < 34 {
            ops.push(-3);
        } else if roll < 37 {
            ops.push(-4);
        } else {
            ops.push(-5);
        }
    }
    ops
}

fn main() {
    let rounds = 300;
    let mut seed: i64 = 622;
    let ops = script(100000, &mut seed);
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let mut q = MyCircularQueue::new(1 + (r * 37) % 1000);
        for &op in ops.iter() {
            let v = if op >= 0 {
                q.en_queue(op) as i64
            } else if op == -1 {
                q.de_queue() as i64
            } else if op == -2 {
                q.front()
            } else if op == -3 {
                q.rear()
            } else if op == -4 {
                q.is_empty() as i64
            } else {
                q.is_full() as i64
            };
            checksum = (checksum * 31 + v + 2) % 1000000007;
        }
    }
    println!("{} queues, {} operations each: checksum {}", rounds, ops.len(), checksum);
}
