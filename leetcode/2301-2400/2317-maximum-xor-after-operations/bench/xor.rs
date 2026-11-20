// LeetCode #2317: Maximum XOR After Operations -- the bench, the ★ arm in
// Rust. The operation can clear any of a number's bits and set none, so
// the most is the OR of all the numbers.

fn maximum_xor(nums: &[i64]) -> i64 {
    let mut all = 0i64;
    for &x in nums {
        all |= x;
    }
    all
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2317i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..20 {
        let mut mask = 0i64;
        for _ in 0..a + 4 {
            mask |= 1 << (next_random(&mut seed) % 27);
        }
        let mut nums = Vec::new();
        for _ in 0..100000 {
            let hi = next_random(&mut seed);
            nums.push((hi * 32768 + next_random(&mut seed)) % 100000001 & mask);
        }
        arrays.push(nums);
    }
    let mut check = 0i64;
    for p in 0..100 {
        for a in 0..20 {
            check = (check * 31 + maximum_xor(&arrays[(a + p) % 20])) % 1000000007;
        }
    }
    println!("100 passes over 20 arrays of 10^5 numbers: checksum {}", check);
}
