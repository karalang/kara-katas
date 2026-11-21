// LeetCode #2424: Longest Uploaded Prefix -- the bench, the ★ arm: a flag
// for each video and the prefix so far, moved on by `longest` past every
// flag set beyond it.

struct LuPrefix {
    uploaded: Vec<bool>,
    prefix: usize,
}

impl LuPrefix {
    fn new(n: usize) -> LuPrefix {
        LuPrefix { uploaded: vec![false; n + 2], prefix: 0 }
    }

    fn upload(&mut self, video: usize) {
        self.uploaded[video] = true;
    }

    fn longest(&mut self) -> usize {
        while self.uploaded[self.prefix + 1] {
            self.prefix += 1;
        }
        self.prefix
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: usize = 100000;
    let mut seed = 2424;
    let mut scripts: Vec<Vec<usize>> = Vec::new();
    for s in 0..10 {
        let width = 1usize << (s + 3);
        let mut order: Vec<usize> = (1..n + 1).collect();
        let mut start = 0;
        while start < n {
            let end = (start + width).min(n);
            for i in (start + 1..end).rev() {
                let r = next_random(&mut seed) * 32768 + next_random(&mut seed);
                let j = start + (r % (i - start + 1) as i64) as usize;
                order.swap(i, j);
            }
            start = end;
        }
        scripts.push(order);
    }
    let mut check: i64 = 0;
    for p in 0..50 {
        for order in scripts.iter() {
            let mut server = LuPrefix::new(n);
            for &v in order.iter() {
                server.upload(v);
                check = (check * 31 + server.longest() as i64 + p) % 1000000007;
            }
        }
    }
    println!("50 passes over 10 scripts of 10^5 uploads: checksum {}", check);
}
