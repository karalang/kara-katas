// Benchmark for #641: mirror of circular_deque.kara (the ★ arm: a ring
// with a start and a count) on the same workload.

struct MyCircularDeque {
    data: Vec<i64>,
    head: i64,
    count: i64,
}

impl MyCircularDeque {
    fn new(k: i64) -> MyCircularDeque {
        MyCircularDeque { data: vec![0; k as usize], head: 0, count: 0 }
    }

    fn len(&self) -> i64 {
        self.data.len() as i64
    }

    fn insert_front(&mut self, value: i64) -> bool {
        if self.count == self.len() {
            return false;
        }
        self.head = (self.head + self.len() - 1) % self.len();
        let at = self.head as usize;
        self.data[at] = value;
        self.count += 1;
        true
    }

    fn insert_last(&mut self, value: i64) -> bool {
        if self.count == self.len() {
            return false;
        }
        let at = ((self.head + self.count) % self.len()) as usize;
        self.data[at] = value;
        self.count += 1;
        true
    }

    fn delete_front(&mut self) -> bool {
        if self.count == 0 {
            return false;
        }
        self.head = (self.head + 1) % self.len();
        self.count -= 1;
        true
    }

    fn delete_last(&mut self) -> bool {
        if self.count == 0 {
            return false;
        }
        self.count -= 1;
        true
    }

    fn get_front(&self) -> i64 {
        if self.count == 0 { -1 } else { self.data[self.head as usize] }
    }

    fn get_rear(&self) -> i64 {
        if self.count == 0 {
            -1
        } else {
            self.data[((self.head + self.count - 1) % self.len()) as usize]
        }
    }

    fn is_empty(&self) -> bool {
        self.count == 0
    }

    fn is_full(&self) -> bool {
        self.count == self.len()
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
        if roll < 8 {
            ops.push(next_random(seed) % 1001);
        } else if roll < 16 {
            ops.push(1001 + next_random(seed) % 1001);
        } else if roll < 21 {
            ops.push(-1);
        } else if roll < 26 {
            ops.push(-2);
        } else if roll < 30 {
            ops.push(-3);
        } else if roll < 34 {
            ops.push(-4);
        } else if roll < 37 {
            ops.push(-5);
        } else {
            ops.push(-6);
        }
    }
    ops
}

fn flag(b: bool) -> i64 {
    if b { 1 } else { 0 }
}

fn main() {
    let rounds: i64 = 300;
    let mut seed: i64 = 641;
    let ops = script(100000, &mut seed);
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let mut q = MyCircularDeque::new(1 + (r * 37) % 1000);
        for &op in ops.iter() {
            let v = if op >= 1001 {
                flag(q.insert_last(op - 1001))
            } else if op >= 0 {
                flag(q.insert_front(op))
            } else if op == -1 {
                flag(q.delete_front())
            } else if op == -2 {
                flag(q.delete_last())
            } else if op == -3 {
                q.get_front()
            } else if op == -4 {
                q.get_rear()
            } else if op == -5 {
                flag(q.is_empty())
            } else {
                flag(q.is_full())
            };
            checksum = (checksum * 31 + v + 2) % 1000000007;
        }
    }
    println!("{} deques, {} operations each: checksum {}", rounds, ops.len(), checksum);
}
