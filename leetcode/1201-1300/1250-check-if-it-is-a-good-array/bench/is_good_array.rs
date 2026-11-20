// LeetCode #1250 bench, in Rust: the ★ arm (Euclid's algorithm folded
// over the array, stopping once the divisor reaches 1) on 50 random
// arrays of 100000 values built once, every value sharing a factor from
// 2 to 1000 and, in half of them, one value of no shared factor put in
// at a random place; each asked 20 times, every answer folded into a
// checksum.

fn gcd(a: i64, b: i64) -> i64 {
    let mut a = a;
    let mut b = b;
    while b != 0 {
        let r = a % b;
        a = b;
        b = r;
    }
    a
}

fn is_good_array(nums: &[i64]) -> bool {
    let mut g = 0;
    for &x in nums {
        g = gcd(g, x);
        if g == 1 {
            return true;
        }
    }
    g == 1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn big_random(seed: &mut i64) -> i64 {
    let hi = next_random(seed) * 32768;
    hi + next_random(seed)
}

fn main() {
    let mut seed = 1250;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for t in 0..50 {
        let factor = next_random(&mut seed) % 999 + 2;
        let mut nums = Vec::with_capacity(100000);
        for _ in 0..100000 {
            nums.push(factor * (big_random(&mut seed) % (1000000000 / factor) + 1));
        }
        if t % 2 == 0 {
            let at = (big_random(&mut seed) % 100000) as usize;
            nums[at] = 999999937;
        }
        arrays.push(nums);
    }
    let mut check: i64 = 0;
    for _ in 0..20 {
        for (t, nums) in arrays.iter().enumerate() {
            let yes = is_good_array(nums);
            check = (check * 131 + if yes { t as i64 + 1 } else { 0 }) % 1000000007;
        }
    }
    println!("20 rounds of 50 arrays of 100000 values: checksum {check}");
}
