// LeetCode #1399 bench -- Rust: each number's digit sum by peeling off its
// last digit, the groups' sizes in an array indexed by the sum, and the
// groups of the largest size counted.

fn digit_sum(x: i32) -> i64 {
    let mut rest = x;
    let mut sum = 0i64;
    while rest > 0 {
        sum += (rest % 10) as i64;
        rest /= 10;
    }
    sum
}

fn count_largest_group(n: i32) -> i32 {
    let mut size = vec![0i32; 37];
    for x in 1..=n {
        size[digit_sum(x) as usize] += 1;
    }
    let largest = *size.iter().max().unwrap();
    size.iter().filter(|&&s| s == largest).count() as i32
}

fn main() {
    let mut check: i64 = 0;
    for r in 0..6000i64 {
        let n = 1 + (check + r * 7919) % 10000;
        check = (check * 131 + count_largest_group(n as i32) as i64) % 1000000007;
    }
    println!("6000 rounds of n up to 10^4: checksum {}", check);
}
