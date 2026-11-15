// benchmark's Rust mirror of replace.kara (LeetCode #2197, the ★ arm): a
// stack merged at its top.

fn gcd(a: i64, b: i64) -> i64 {
    let (mut x, mut y) = (a, b);
    while y != 0 {
        let r = x % y;
        x = y;
        y = r;
    }
    x
}

fn replace_non_coprimes(nums: &[i64]) -> Vec<i64> {
    let mut stack: Vec<i64> = Vec::new();
    for &x in nums {
        let mut cur = x;
        while let Some(&top) = stack.last() {
            let g = gcd(top, cur);
            if g == 1 {
                break;
            }
            cur = top / g * cur;
            stack.pop();
        }
        stack.push(cur);
    }
    stack
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn divisors(m: i64) -> Vec<i64> {
    (1..100001).filter(|d| m % d == 0).collect()
}

fn main() {
    let pools = [divisors(10810800), divisors(1674432), vec![1, 99991, 99989, 99971, 99961, 99929, 99923]];
    let mut seed = 2197;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..12 {
        let pool = &pools[a % 3];
        let nums: Vec<i64> = (0..100000).map(|_| pool[(wide_random(&mut seed) % pool.len() as i64) as usize]).collect();
        arrays.push(nums);
    }
    let mut check: i64 = 0;
    for _ in 0..100 {
        for nums in &arrays {
            let out = replace_non_coprimes(nums);
            check = (check * 31 + out.len() as i64) % 1000000007;
            check = (check * 31 + out[out.len() / 2]) % 1000000007;
        }
    }
    println!("100 passes over 12 arrays: checksum {}", check);
}
