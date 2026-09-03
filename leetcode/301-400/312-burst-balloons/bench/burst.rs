// Benchmark workload for LeetCode #312 - Burst Balloons.
//
// Mirror of burst.kara: same interval DP, same flat table reused across
// passes, same serial dependency between passes, same masked sink. Kept
// algorithm-for-algorithm so the cross-language comparison is honest.

fn solve(a: &[i64], w: i64, dp: &mut [i64]) -> i64 {
    for len in 2..w {
        for i in 0..(w - len) {
            let j = i + len;
            let ai = a[i as usize];
            let aj = a[j as usize];
            let base = i * w;
            let mut best = 0i64;
            for k in (i + 1)..j {
                let coins = dp[(base + k) as usize] + dp[(k * w + j) as usize]
                    + ai * a[k as usize] * aj;
                if coins > best {
                    best = coins;
                }
            }
            dp[(base + j) as usize] = best;
        }
    }
    dp[(w - 1) as usize]
}

fn main() {
    let n: i64 = 300;
    let w: i64 = n + 2;
    let passes: i64 = 88;

    let mut a: Vec<i64> = Vec::with_capacity(w as usize);
    a.push(1);
    let mut state: i64 = 987654321;
    for _ in 0..n {
        state = (state * 1103515245 + 12345) % 2147483648;
        a.push(1 + state % 50);
    }
    a.push(1);

    let mut dp: Vec<i64> = vec![0; (w * w) as usize];

    let mut checksum: i64 = 0;
    for _ in 0..passes {
        let idx = (1 + checksum % n) as usize;
        a[idx] = 1 + (a[idx] + checksum) % 50;
        let total = solve(&a, w, &mut dp);
        checksum = (checksum + total) & 1073741823;
    }

    println!("checksum {}", checksum);
}
