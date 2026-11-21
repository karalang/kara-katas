// LeetCode #2498: Frog Jump II -- Rust mirror of the benchmark (frog.kara):
// the same rows, passes and checksum.

fn max_jump(stones: &[i64]) -> i64 {
    let mut cost = stones[1] - stones[0];
    for i in 2..stones.len() {
        cost = cost.max(stones[i] - stones[i - 2]);
    }
    cost
}

fn main() {
    let n: i64 = 100000;
    let passes: i64 = 55;
    let mut seed: i64 = 2498;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut rows: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let mut stones: Vec<i64> = vec![0];
        for _ in 1..n {
            let last = stones[stones.len() - 1];
            stones.push(last + next_random() % 10000 + 1);
        }
        rows.push(stones);
    }
    let mut check: i64 = 0;
    for p in 0..passes {
        for r in 0..20 {
            let at = (check % (n - 2) + 1) as usize;
            let was = rows[r][at];
            let room = rows[r][at + 1] - rows[r][at - 1] - 1;
            if room > 0 {
                rows[r][at] = rows[r][at - 1] + 1 + (check + p) % room;
            }
            check = (check * 31 + max_jump(&rows[r]) + p) % 1000000007;
            rows[r][at] = was;
        }
    }
    println!("{passes} passes over 20 rows of 10^5: checksum {check}");
}
