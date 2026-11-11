// LeetCode #2119: A Number After a Double Reversal -- the benchmark, the
// same algorithm as reversed.kara: each number's digits reversed by % 10
// and / 10, twice.

fn reverse(num: i64) -> i64 {
    let mut n = num;
    let mut out = 0i64;
    while n > 0 {
        out = out * 10 + n % 10;
        n /= 10;
    }
    out
}

fn is_same_after_reversals(num: i64) -> bool {
    reverse(reverse(num)) == num
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2119i64;
    let mut nums: Vec<i64> = Vec::new();
    for _ in 0..1000000 {
        let mut num = next_random(&mut seed) % 1000001;
        if next_random(&mut seed) % 3 == 0 {
            num = num / 1000 * 1000;
        }
        nums.push(num);
    }
    let mut same = 0i64;
    let mut check = 0i64;
    for round in 0..100usize {
        nums[round * 7919 % 1000000] += 1;
        for &num in nums.iter() {
            if is_same_after_reversals(num) {
                same += 1;
                check = (check * 31 + num % 1000) % 1000000007;
            }
        }
    }
    println!("100000000 checks: {} the same, checksum {}", same, check);
}
