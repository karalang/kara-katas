// Benchmark for #528: Rust mirror of the ★ arm (prefix sums and a binary
// search); see random_pick_with_weight.kara. The same seeded generator,
// so the same picks.

struct Draw {
    seed: i64,
}

impl Draw {
    fn step(&mut self) -> i64 {
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648;
        self.seed / 65536
    }

    fn below(&mut self, n: i64) -> i64 {
        let limit = 1073741824 / n * n;
        loop {
            let high = self.step();
            let low = self.step();
            let r = high * 32768 + low;
            if r < limit {
                return r % n;
            }
        }
    }
}

struct Solution {
    ends: Vec<i64>,
    draw: Draw,
}

impl Solution {
    fn new(w: &[i64], seed: i64) -> Solution {
        let mut ends = Vec::new();
        let mut total = 0;
        for x in w {
            total += x;
            ends.push(total);
        }
        Solution { ends, draw: Draw { seed } }
    }

    fn pick_index(&mut self) -> i64 {
        let r = self.draw.below(self.ends[self.ends.len() - 1]);
        let mut low = 0;
        let mut high = self.ends.len() - 1;
        while low < high {
            let mid = (low + high) / 2;
            if self.ends[mid] > r {
                high = mid;
            } else {
                low = mid + 1;
            }
        }
        low as i64
    }
}

fn main() {
    let mut seed: i64 = 528;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let mut w = Vec::new();
        for _ in 0..10000 {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let high = seed / 65536;
            seed = (seed * 1103515245 + 12345) % 2147483648;
            w.push(1 + (high * 32768 + seed / 65536) % 100000);
        }
        lists.push(w);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..50 {
        for l in 0..lists.len() {
            let mut solution = Solution::new(&lists[l], round * 20 + l as i64);
            for _ in 0..10000 {
                let i = solution.pick_index();
                total += i;
                checksum = (checksum * 31 + i) % 1000000007;
            }
        }
    }
    println!("20 lists of 10000, 50 rounds of 10000 picks: total {}, checksum {}", total, checksum);
}
