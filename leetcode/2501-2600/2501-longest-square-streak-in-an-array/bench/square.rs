// LeetCode #2501: Longest Square Streak in an Array -- Rust mirror of the
// benchmark (square.kara): the same arrays, passes and checksum; the
// values in a std `HashSet` on every ask.
use std::collections::HashSet;

fn longest_square_streak(nums: &[i64]) -> i64 {
    let present: HashSet<i64> = nums.iter().cloned().collect();
    let mut best = 0;
    for &v in present.iter() {
        let r = v.isqrt();
        if r * r == v && present.contains(&r) {
            continue;
        }
        let mut length = 0;
        let mut x = v;
        while present.contains(&x) {
            length += 1;
            x = x * x;
        }
        best = best.max(length);
    }
    if best >= 2 { best } else { -1 }
}

struct Rng(i64);

impl Rng {
    fn next(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
    fn below(&mut self, top: i64) -> i64 {
        let hi = self.next();
        (hi * 32768 + self.next()) % top
    }
}

fn chained(n: i64, rng: &mut Rng) -> Vec<i64> {
    let mut out = Vec::new();
    for _ in 0..n {
        if rng.next() % 4 == 0 {
            out.push(rng.below(99999) + 2);
        } else {
            let mut v = rng.next() % 19 + 2;
            for _ in 0..rng.next() % 4 {
                if v * v <= 100000 {
                    v = v * v;
                }
            }
            out.push(v);
        }
    }
    out
}

fn main() {
    let passes = 32;
    let n = 100000;
    let mut rng = Rng(2501);
    let mut arrays: Vec<Vec<i64>> = (0..20).map(|_| chained(n, &mut rng)).collect();
    let mut check: i64 = 0;
    for p in 0..passes {
        for q in 0..20 {
            let at = (check % n) as usize;
            let was = arrays[q][at];
            arrays[q][at] = (check + p) % 99999 + 2;
            check = (check * 31 + longest_square_streak(&arrays[q]) + 1 + p) % 1000000007;
            arrays[q][at] = was;
        }
    }
    println!("{} passes over 20 arrays of 10^5: checksum {}", passes, check);
}
