// LeetCode #2502: Design Memory Allocator -- Rust mirror of the benchmark
// (alloc.kara): the same sessions, calls and checksum; every unit's owner
// in a `Vec`.

struct Allocator {
    memory: Vec<i64>,
}

impl Allocator {
    fn new(n: usize) -> Allocator {
        Allocator { memory: vec![0; n] }
    }

    fn allocate(&mut self, size: i64, m_id: i64) -> i64 {
        let mut run = 0;
        for i in 0..self.memory.len() {
            if self.memory[i] == 0 {
                run += 1;
                if run == size {
                    let start = i + 1 - size as usize;
                    for j in start..i + 1 {
                        self.memory[j] = m_id;
                    }
                    return start as i64;
                }
            } else {
                run = 0;
            }
        }
        -1
    }

    fn free_memory(&mut self, m_id: i64) -> i64 {
        let mut freed = 0;
        for i in 0..self.memory.len() {
            if self.memory[i] == m_id {
                self.memory[i] = 0;
                freed += 1;
            }
        }
        freed
    }
}

struct Rng(i64);

impl Rng {
    fn next(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn main() {
    let sessions = 400;
    let mut rng = Rng(2502);
    let mut check: i64 = 0;
    for s in 0..sessions {
        let mut allocator = Allocator::new(1000);
        for _ in 0..1000 {
            let r = if (rng.next() + check) % 3 < 2 {
                let size = rng.next() % 20 + 1;
                allocator.allocate(size, rng.next() % 50 + 1)
            } else {
                allocator.free_memory(rng.next() % 50 + 1)
            };
            check = (check * 31 + r + 1 + s) % 1000000007;
        }
    }
    println!("{} sessions of 1000 calls on 1000 units: checksum {}", sessions, check);
}
