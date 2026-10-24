// Benchmark: LeetCode #961 N-Repeated Element in Size 2N Array -- the ★
// arm, near neighbours, on 10000 numbers, LeetCode's largest, with the
// repeated value at every other place. Each call swaps two of the other
// values first. Mirrors repeated_n_times.kara, .c, .py and go-seq/.

fn repeated_n_times(nums: &[i64]) -> i64 {
    let len = nums.len();
    for k in 1..4 {
        for i in 0..len - k {
            if nums[i] == nums[i + k] {
                return nums[i];
            }
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn alternating(seed: &mut i64, n: usize, first: bool) -> Vec<i64> {
    let mut used = vec![false; 10001];
    let r = next_random(seed) % 10001;
    used[r as usize] = true;
    let mut out = Vec::new();
    while out.len() < 2 * n {
        let v = next_random(seed) % 10001;
        if !used[v as usize] {
            used[v as usize] = true;
            if first {
                out.push(r);
                out.push(v);
            } else {
                out.push(v);
                out.push(r);
            }
        }
    }
    out
}

fn main() {
    let rounds = 1000;
    let mut seed = 961;
    let mut cases: Vec<Vec<i64>> = (0..50)
        .map(|i| alternating(&mut seed, 5000, i % 2 == 0))
        .collect();
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..50 {
            let c = (r + i) % 50;
            let p = (2 * (next_random(&mut seed) % 4999) + 1 - (c % 2) as i64) as usize;
            cases[c].swap(p, p + 2);
            let a = repeated_n_times(&cases[c]);
            total += a;
            check = (check * 31 + a + i as i64) % 1000000007;
        }
    }
    println!("{rounds} rounds over 50 cases of 10000 numbers: the repeated ones sum to {total}, checksum {check}");
}
