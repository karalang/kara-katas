// LeetCode #708: Insert into a Sorted Circular Linked List -- an arena.
// Benchmark mirror of the Kara star arm: values and next links in two
// growable arrays; walk from the given node to the first gap that fits.

struct Ring {
    vals: Vec<i64>,
    next: Vec<usize>,
}

fn fits(a: i64, b: i64, x: i64) -> bool {
    if a <= b {
        a <= x && x <= b
    } else {
        x >= a || x <= b
    }
}

impl Ring {
    fn insert(&mut self, head: Option<usize>, insert_val: i64) -> usize {
        let id = self.vals.len();
        self.vals.push(insert_val);
        let head = match head {
            Some(h) => h,
            None => {
                self.next.push(id);
                return id;
            }
        };
        let mut prev = head;
        loop {
            let curr = self.next[prev];
            if fits(self.vals[prev], self.vals[curr], insert_val) {
                break;
            }
            prev = curr;
            if prev == head {
                break;
            }
        }
        let after = self.next[prev];
        self.next.push(after);
        self.next[prev] = id;
        head
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 708;
    let mut checksum: i64 = 0;
    let n = 20000usize;
    for _ in 0..5 {
        for _ in 0..10 {
            let mut sorted: Vec<i64> = Vec::with_capacity(n);
            for _ in 0..n {
                let hi = next_random(&mut seed);
                let lo = next_random(&mut seed);
                sorted.push((hi * 32768 + lo) % 2000001 - 1000000);
            }
            sorted.sort();
            let start = (next_random(&mut seed) % n as i64) as usize;
            let mut ring = Ring { vals: Vec::new(), next: Vec::new() };
            for i in 0..n {
                ring.vals.push(sorted[(start + i) % n]);
                ring.next.push((i + 1) % n);
            }
            let mut head = 0;
            for _ in 0..1000 {
                let hi = next_random(&mut seed);
                let lo = next_random(&mut seed);
                head = ring.insert(Some(head), (hi * 32768 + lo) % 2000001 - 1000000);
            }
            let mut at = head;
            loop {
                checksum = (checksum * 31 + ring.vals[at] + 1000001) % 1000000007;
                at = ring.next[at];
                if at == head {
                    break;
                }
            }
        }
    }
    println!("5 rounds of 10 rings of 20000 values, 1000 inserts each: checksum {}", checksum);
}
