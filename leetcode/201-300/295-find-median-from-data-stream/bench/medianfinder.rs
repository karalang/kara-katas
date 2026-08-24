// LeetCode 295 benchmark lane — Rust mirror of medianfinder.kara.
//
// Deliberately a HAND-ROLLED heap rather than std's `BinaryHeap`, for the same
// reason the C mirror hand-rolls one: the Kara version has no stdlib heap to
// call, so benchmarking Kara's hand-written sift loop against Rust's tuned
// library heap would measure library maturity rather than code generation.
// Same algorithm on both sides, same `max` flag instead of negation.

struct Heap { data: Vec<i64>, max: bool }

impl Heap {
    fn new(max: bool) -> Heap { Heap { data: Vec::with_capacity(1024), max } }

    #[inline]
    fn outranks(&self, a: i64, b: i64) -> bool {
        if self.max { a > b } else { a < b }
    }

    fn push(&mut self, v: i64) {
        self.data.push(v);
        let mut i = self.data.len() - 1;
        while i > 0 {
            let parent = (i - 1) / 2;
            if !self.outranks(self.data[i], self.data[parent]) { break; }
            self.data.swap(i, parent);
            i = parent;
        }
    }

    fn pop(&mut self) -> i64 {
        let top = self.data[0];
        let last = self.data.pop().unwrap();
        if !self.data.is_empty() {
            self.data[0] = last;
            let n = self.data.len();
            let mut i = 0usize;
            loop {
                let l = 2 * i + 1;
                let r = l + 1;
                let mut best = i;
                if l < n && self.outranks(self.data[l], self.data[best]) { best = l; }
                if r < n && self.outranks(self.data[r], self.data[best]) { best = r; }
                if best == i { break; }
                self.data.swap(i, best);
                i = best;
            }
        }
        top
    }
}

fn main() {
    let n: i64 = 2_000_000;
    let mut lo = Heap::new(true);
    let mut hi = Heap::new(false);

    let mut state: i64 = 12345;
    let mut checksum: i64 = 0;
    for _ in 0..n {
        state = (state.wrapping_mul(1103515245).wrapping_add(12345)) & 0x7fffffff;
        let v = state % 1000003 - 500000;

        lo.push(v);
        let moved = lo.pop();
        hi.push(moved);
        if hi.data.len() > lo.data.len() {
            let back = hi.pop();
            lo.push(back);
        }

        let twice = if lo.data.len() > hi.data.len() {
            2 * lo.data[0]
        } else {
            lo.data[0] + hi.data[0]
        };
        checksum = (checksum * 31 + twice) % 1000000007;
    }

    println!("adds {} checksum {}", n, checksum);
}
