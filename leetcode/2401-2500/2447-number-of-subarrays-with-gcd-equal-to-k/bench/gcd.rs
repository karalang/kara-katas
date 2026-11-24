// LeetCode #2447: Number of Subarrays With GCD Equal to K -- the bench,
// the ★ arm: from each start the running GCD, the walk stopped once it
// is no multiple of `k`.

fn gcd(a: i64, b: i64) -> i64 {
    let mut x = a;
    let mut y = b;
    while y != 0 {
        let r = x % y;
        x = y;
        y = r;
    }
    x
}

fn subarray_gcd(nums: &[i64], k: i64) -> i64 {
    let mut count = 0;
    for i in 0..nums.len() {
        let mut g = 0;
        for j in i..nums.len() {
            g = gcd(g, nums[j]);
            if g % k != 0 {
                break;
            }
            if g == k {
                count += 1;
            }
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn draw(seed: &mut i64) -> i64 {
    let v = 6 * (1 + next_random(seed) % 1000);
    if next_random(seed) % 40 == 0 { v + 1 } else { v }
}

fn main() {
    let mut seed = 2447;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..1000 {
            nums.push(draw(&mut seed));
        }
        arrays.push(nums);
    }
    let mut check: i64 = 0;
    for p in 0..90usize {
        for c in 0..arrays.len() {
            arrays[c][(37 * p + c) % 1000] = draw(&mut seed);
            check = (check * 31 + subarray_gcd(&arrays[c], 6) + p as i64) % 1000000007;
        }
    }
    println!("90 passes over 20 arrays of 1000 values: checksum {}", check);
}
