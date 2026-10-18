// LeetCode #699: Falling Squares -- bench program, Rust mirror of the segment-tree arm.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

struct Tree {
    best: Vec<i64>,
    pending: Vec<i64>,
}

impl Tree {
    fn push_down(&mut self, node: usize) {
        let p = self.pending[node];
        if p >= 0 {
            for child in [2 * node, 2 * node + 1] {
                self.best[child] = p;
                self.pending[child] = p;
            }
            self.pending[node] = -1;
        }
    }

    fn query(&mut self, node: usize, lo: usize, hi: usize, from: usize, to: usize) -> i64 {
        if to <= lo || hi <= from {
            return 0;
        }
        if from <= lo && hi <= to {
            return self.best[node];
        }
        self.push_down(node);
        let mid = (lo + hi) / 2;
        self.query(2 * node, lo, mid, from, to).max(self.query(2 * node + 1, mid, hi, from, to))
    }

    fn set(&mut self, node: usize, lo: usize, hi: usize, from: usize, to: usize, h: i64) {
        if to <= lo || hi <= from {
            return;
        }
        if from <= lo && hi <= to {
            self.best[node] = h;
            self.pending[node] = h;
            return;
        }
        self.push_down(node);
        let mid = (lo + hi) / 2;
        self.set(2 * node, lo, mid, from, to, h);
        self.set(2 * node + 1, mid, hi, from, to, h);
        self.best[node] = self.best[2 * node].max(self.best[2 * node + 1]);
    }
}

fn falling_squares(positions: &[(i64, i64)]) -> Vec<i64> {
    let mut edges: Vec<i64> = Vec::new();
    for &(left, side) in positions {
        edges.push(left);
        edges.push(left + side);
    }
    edges.sort();
    edges.dedup();
    let cells = edges.len();
    let mut tree = Tree { best: vec![0; 4 * cells], pending: vec![-1; 4 * cells] };
    let mut answer: Vec<i64> = Vec::new();
    for &(left, side) in positions {
        let from = edges.binary_search(&left).unwrap();
        let to = edges.binary_search(&(left + side)).unwrap();
        let top = tree.query(1, 0, cells, from, to) + side;
        tree.set(1, 0, cells, from, to, top);
        answer.push(tree.best[1]);
    }
    answer
}

fn main() {
    let mut seed = 699;
    let mut problems: Vec<Vec<(i64, i64)>> = Vec::new();
    for p in 0..100i64 {
        let width = 1000 + p * 999990;
        let biggest = 1 + next_random(&mut seed) % 1000000;
        let mut positions: Vec<(i64, i64)> = Vec::new();
        for _ in 0..1000 {
            let a = next_random(&mut seed);
            let b = next_random(&mut seed);
            let left = 1 + (a * 32768 + b) % width;
            let side = 1 + next_random(&mut seed) % biggest;
            positions.push((left, side));
        }
        problems.push(positions);
    }
    let rounds = 5;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        for positions in &problems {
            let heights = falling_squares(positions);
            let last = heights[heights.len() - 1];
            total += last;
            checksum = (checksum * 31 + last) % 1000000007;
        }
    }
    println!("{} rounds of 100 problems of 1000 squares: tallest stacks sum to {}, checksum {}", rounds, total, checksum);
}
