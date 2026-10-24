// Benchmark: LeetCode #978 Longest Turbulent Subarray -- the ★ arm, two
// running lengths, on 20 arrays of 40000 values. Mirrors
// max_turbulence_size.kara, .c, .py and go-seq/.

fn max_turbulence_size(arr: &[i64]) -> i64 {
    let mut best = 1;
    let mut up = 1;
    let mut down = 1;
    for i in 1..arr.len() {
        if arr[i - 1] < arr[i] {
            up = down + 1;
            down = 1;
        } else if arr[i - 1] > arr[i] {
            down = up + 1;
            up = 1;
        } else {
            up = 1;
            down = 1;
        }
        best = best.max(up.max(down));
    }
    best
}

struct Rng(i64);

impl Rng {
    fn next(&mut self) -> i64 {
        self.0 = (self.0 * 1103515245 + 12345) % 2147483648;
        self.0 / 65536
    }
}

fn main() {
    let rounds = 150;
    let count = 20;
    let mut rng = Rng(978);
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let arr: Vec<i64> = (0..40000).map(|_| rng.next() % 100).collect();
        arrays.push(arr);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let k = max_turbulence_size(&arrays[(r + i) % count]);
            total += k;
            check = (check * 31 + k) % 1000000007;
        }
    }
    println!("{rounds} rounds over {count} arrays of 40000 values: lengths total {total}, checksum {check}");
}
