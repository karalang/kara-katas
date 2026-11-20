// LeetCode #1253 bench, in Rust: the ★ arm (the 2s counted first, then
// each column of 1 giving its 1 to the upper row while it has room, and
// to the lower after) on 20 random cases of 100000 columns built once,
// each with its own share of 2s and half of them with no matrix; each
// asked 50 times, every answer folded into a checksum.

fn reconstruct_matrix(upper: i64, lower: i64, colsum: &[i64]) -> Vec<Vec<i64>> {
    let n = colsum.len();
    let twos = colsum.iter().filter(|&&v| v == 2).count() as i64;
    let ones = colsum.iter().filter(|&&v| v == 1).count() as i64;
    if upper < twos || lower < twos || upper + lower != 2 * twos + ones {
        return vec![];
    }
    let mut up = vec![0i64; n];
    let mut low = vec![0i64; n];
    let mut left = upper - twos;
    for i in 0..n {
        if colsum[i] == 2 {
            up[i] = 1;
            low[i] = 1;
        } else if colsum[i] == 1 {
            if left > 0 {
                up[i] = 1;
                left -= 1;
            } else {
                low[i] = 1;
            }
        }
    }
    vec![up, low]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1253;
    let mut cases: Vec<(i64, i64, Vec<i64>)> = Vec::new();
    for t in 0..20 {
        let twos = next_random(&mut seed) % 101;
        let mut colsum = Vec::new();
        let mut upper = 0;
        let mut lower = 0;
        for _ in 0..100000 {
            let v = if next_random(&mut seed) % 100 < twos { 2 } else { next_random(&mut seed) % 2 };
            colsum.push(v);
            if v == 2 {
                upper += 1;
                lower += 1;
            } else if v == 1 {
                if next_random(&mut seed) % 2 == 0 {
                    upper += 1;
                } else {
                    lower += 1;
                }
            }
        }
        if t % 2 == 1 {
            upper += 1;
        }
        cases.push((upper, lower, colsum));
    }
    let mut check: i64 = 0;
    for _ in 0..50 {
        for (upper, lower, colsum) in &cases {
            let ans = reconstruct_matrix(*upper, *lower, colsum);
            let mut even = 0;
            if !ans.is_empty() {
                let mut i = 0;
                while i < colsum.len() {
                    even += ans[0][i];
                    i += 2;
                }
            }
            check = (check * 131 + ans.len() as i64 + even) % 1000000007;
        }
    }
    println!("50 rounds of 20 cases of 100000 columns: checksum {check}");
}
