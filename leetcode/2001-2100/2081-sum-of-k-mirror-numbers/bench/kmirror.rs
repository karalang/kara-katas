// LeetCode #2081: Sum of k-Mirror Numbers -- Rust mirror of the ★ arm's
// benchmark (kmirror.kara): every base from 2 to 9 asked for every `n`
// from 1 to 32, each search started afresh: 256 searches.

fn is_mirror(x: i64, k: i64) -> bool {
    let mut digits: Vec<i64> = Vec::new();
    let mut y = x;
    while y > 0 {
        digits.push(y % k);
        y /= k;
    }
    let m = digits.len();
    for i in 0..m / 2 {
        if digits[i] != digits[m - 1 - i] {
            return false;
        }
    }
    true
}

fn k_mirror(k: i64, n: i64) -> i64 {
    let mut sum = 0;
    let mut found = 0;
    let mut length: i64 = 1;
    loop {
        let half = (length + 1) / 2;
        let start = 10i64.pow((half - 1) as u32);
        for h in start..start * 10 {
            let mut p = h;
            let mut rest = if length % 2 == 1 { h / 10 } else { h };
            while rest > 0 {
                p = p * 10 + rest % 10;
                rest /= 10;
            }
            if is_mirror(p, k) {
                sum += p;
                found += 1;
                if found == n {
                    return sum;
                }
            }
        }
        length += 1;
    }
}

fn main() {
    let (mut total, mut check) = (0i64, 0i64);
    for k in 2..10 {
        for n in 1..33 {
            let a = k_mirror(k, n);
            total += a;
            check = (check * 31 + a) % 1000000007;
        }
    }
    println!("256 answers: sum {}, checksum {}", total, check);
}
