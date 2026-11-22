// LeetCode #2897: Apply Operations on Array to Maximize Sum of Squares --
// the bench's Rust mirror (squares.kara).

fn max_sum(nums: &[i64], k: i64) -> i64 {
    let modulus = 1000000007i64;
    let mut holders = [0i64; 31];
    for &v in nums {
        for b in 0..31 {
            if (v >> b) & 1 == 1 {
                holders[b] += 1;
            }
        }
    }
    let mut sum = 0i64;
    for _ in 0..k {
        let mut value = 0i64;
        for b in 0..31 {
            if holders[b] > 0 {
                holders[b] -= 1;
                value |= 1 << b;
            }
        }
        sum = (sum + value * value) % modulus;
    }
    sum
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let (count, rounds, n) = (20i64, 20i64, 10000i64);
    let mut seed = 2897i64;
    let mut cases: Vec<(Vec<i64>, i64)> = Vec::new();
    for c in 0..count {
        let mut nums = Vec::new();
        for _ in 0..n {
            if c % 2 == 0 {
                nums.push(wide(&mut seed) % 1000000000 + 1);
            } else {
                let a = next_random(&mut seed) % 30;
                let b = next_random(&mut seed) % 30;
                nums.push((1i64 << a) | (1i64 << b));
            }
        }
        let k = wide(&mut seed) % n + 1;
        cases.push((nums, k));
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for (nums, k) in &cases {
            let s = max_sum(nums, *k);
            total += s;
            check = (check * 31 + s + r) % 1000000007;
        }
    }
    println!("{count} arrays of {n}, {rounds} rounds: sums total {total}, checksum {check}");
}
