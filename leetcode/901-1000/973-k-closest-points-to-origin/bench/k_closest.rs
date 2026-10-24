// Benchmark: LeetCode #973 K Closest Points to Origin -- the ★ arm, sort
// by squared distance, on 100 sets of 1000 random points. Mirrors
// k_closest.kara, .c, .py and go-seq/.

fn k_closest(points: &[(i64, i64)], k: usize) -> Vec<(i64, i64)> {
    let mut sorted = points.to_vec();
    sorted.sort_by_key(|p| p.0 * p.0 + p.1 * p.1);
    sorted.truncate(k);
    sorted
}

struct Rng(i64);

impl Rng {
    fn next(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn random_case(n: usize, rng: &mut Rng) -> (Vec<(i64, i64)>, usize) {
    let mut points = Vec::with_capacity(n);
    for _ in 0..n {
        let x = rng.next() % 20001 - 10000;
        let y = rng.next() % 20001 - 10000;
        points.push((x, y));
    }
    let mut ds: Vec<i64> = points.iter().map(|p| p.0 * p.0 + p.1 * p.1).collect();
    ds.sort();
    let mut k = 1 + (rng.next() % n as i64) as usize;
    while k < n && ds[k - 1] == ds[k] {
        k += 1;
    }
    (points, k)
}

fn main() {
    let rounds = 100;
    let count = 100;
    let mut rng = Rng(973);
    let cases: Vec<(Vec<(i64, i64)>, usize)> = (0..count).map(|_| random_case(1000, &mut rng)).collect();
    let mut kept = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let c = (r + i) % count;
            let answer = k_closest(&cases[c].0, cases[c].1);
            kept += answer.len();
            for (x, y) in answer {
                let v = ((x + 10001) * 20003 + y + 10001) % 1000000007;
                check = (check + v * v) % 1000000007;
            }
        }
    }
    println!("{rounds} rounds over {count} sets of 1000 points: {kept} points kept, checksum {check}");
}
