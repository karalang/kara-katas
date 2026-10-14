// LeetCode 633 -- Sum of Square Numbers, bench mirror in Rust.
//
// The ★ arm of judge_square_sum.kara: two pointers from 0 and from the
// integer square root of `c`, found by binary search. Same values, same
// output line.

fn root(n: i64) -> i64 {
    let mut lo = 0;
    let mut hi = n.min(3037000499) + 1;
    while hi - lo > 1 {
        let mid = (lo + hi) / 2;
        if mid * mid <= n {
            lo = mid;
        } else {
            hi = mid;
        }
    }
    lo
}

fn judge_square_sum(c: i64) -> bool {
    let mut a = 0;
    let mut b = root(c);
    while a <= b {
        let sum = a * a + b * b;
        if sum == c {
            return true;
        }
        if sum < c {
            a += 1;
        } else {
            b -= 1;
        }
    }
    false
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 633;
    let mut values: Vec<i64> = Vec::new();
    for _ in 0..10000 {
        let wide = next_random(&mut seed) * 32768 + next_random(&mut seed);
        values.push(wide * 2 + next_random(&mut seed) % 2);
    }
    let mut yes = 0;
    let mut checksum: i64 = 0;
    for &c in values.iter() {
        if judge_square_sum(c) {
            yes += 1;
            checksum = (checksum * 31 + c) % 1000000007;
        }
    }
    println!("{} values: {} sums of two squares, checksum {}", values.len(), yes, checksum);
}
