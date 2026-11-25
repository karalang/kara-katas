// LeetCode #1381 bench -- Rust: the ★ arm: an increment is owed to the
// element k places up; a pop pays the top element what it is owed and
// hands the debt down to the one below.

struct CustomStack {
    max_size: usize,
    stack: Vec<i32>,
    owed: Vec<i32>,
}

impl CustomStack {
    fn new(max_size: i32) -> Self {
        CustomStack { max_size: max_size as usize, stack: Vec::new(), owed: Vec::new() }
    }

    fn push(&mut self, x: i32) {
        if self.stack.len() < self.max_size {
            self.stack.push(x);
            self.owed.push(0);
        }
    }

    fn pop(&mut self) -> i32 {
        let Some(x) = self.stack.pop() else {
            return -1;
        };
        let debt = self.owed.pop().unwrap();
        if let Some(below) = self.owed.last_mut() {
            *below += debt;
        }
        x + debt
    }

    fn increment(&mut self, k: i32, val: i32) {
        let reach = self.stack.len().min(k as usize);
        if reach > 0 {
            self.owed[reach - 1] += val;
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1381;
    let mut check: i64 = 0;
    for _ in 0..2000 {
        seed = (seed + check) % 2147483648;
        let mut s = CustomStack::new(1000);
        for _ in 0..3000 {
            let r = next_random(&mut seed) % 10;
            if r < 4 {
                s.push((1 + next_random(&mut seed) % 1000) as i32);
            } else if r < 7 {
                let k = 1 + next_random(&mut seed) % 1000;
                let val = next_random(&mut seed) % 101;
                s.increment(k as i32, val as i32);
            } else {
                check = (check * 131 + s.pop() as i64 + 1) % 1000000007;
            }
        }
    }
    println!("2000 rounds of 3000 calls on a stack of 1000: checksum {}", check);
}
