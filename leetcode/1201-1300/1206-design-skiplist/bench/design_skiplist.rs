// LeetCode #1206 bench, in Rust: the ★ arm (a skiplist whose nodes live in
// a `Vec`, each node's forward links one per level it stands on, heights
// by coin flips from the list's own generator, erased slots reused) on
// 50000 calls drawn once, a third each of search, add and erase, on values
// up to 20000; then 10 rounds, each on a new list, every answer folded
// into a checksum.

const LEVELS: usize = 16;

struct Skiplist {
    values: Vec<i64>,
    next: Vec<Vec<i64>>,
    free: Vec<usize>,
    seed: i64,
}

impl Skiplist {
    fn new() -> Self {
        Skiplist { values: vec![0], next: vec![vec![-1; LEVELS]], free: Vec::new(), seed: 1206 }
    }

    fn height(&mut self) -> usize {
        let mut h = 1;
        while h < LEVELS {
            self.seed = (self.seed * 1103515245 + 12345) % 2147483648;
            if (self.seed / 65536) % 2 == 1 {
                break;
            }
            h += 1;
        }
        h
    }

    fn path(&self, target: i64) -> [usize; LEVELS] {
        let mut path = [0usize; LEVELS];
        let mut x = 0usize;
        for level in (0..LEVELS).rev() {
            while self.next[x][level] >= 0 && self.values[self.next[x][level] as usize] < target {
                x = self.next[x][level] as usize;
            }
            path[level] = x;
        }
        path
    }

    fn search(&self, target: i64) -> bool {
        let at = self.next[self.path(target)[0]][0];
        at >= 0 && self.values[at as usize] == target
    }

    fn add(&mut self, num: i64) {
        let path = self.path(num);
        let h = self.height();
        let links: Vec<i64> = (0..h).map(|level| self.next[path[level]][level]).collect();
        let node = match self.free.pop() {
            Some(slot) => {
                self.values[slot] = num;
                self.next[slot] = links;
                slot
            }
            None => {
                self.values.push(num);
                self.next.push(links);
                self.values.len() - 1
            }
        };
        for level in 0..h {
            self.next[path[level]][level] = node as i64;
        }
    }

    fn erase(&mut self, num: i64) -> bool {
        let path = self.path(num);
        let at = self.next[path[0]][0];
        if at < 0 || self.values[at as usize] != num {
            return false;
        }
        let at = at as usize;
        for level in 0..self.next[at].len() {
            if self.next[path[level]][level] == at as i64 {
                self.next[path[level]][level] = self.next[at][level];
            }
        }
        self.free.push(at);
        true
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1206i64;
    let mut calls: Vec<(i64, i64)> = Vec::new();
    for _ in 0..50000 {
        let op = next_random(&mut seed) % 3;
        let hi = next_random(&mut seed);
        calls.push((op, (hi * 32768 + next_random(&mut seed)) % 20001));
    }
    let mut check: i64 = 0;
    for _ in 0..10 {
        let mut list = Skiplist::new();
        for &(op, v) in &calls {
            let answer = if op == 0 {
                list.search(v)
            } else if op == 1 {
                list.add(v);
                true
            } else {
                list.erase(v)
            };
            check = (check * 131 + op * 2 + answer as i64) % 1000000007;
        }
    }
    println!("10 rounds of 50000 calls: checksum {check}");
}
