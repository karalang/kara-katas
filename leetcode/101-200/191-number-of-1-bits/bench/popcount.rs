// LeetCode 191 popcount benchmark kernel (Rust mirror, rustc -O).
fn hamming_weight(n: i64) -> i64 {
    let mut count = 0i64;
    let mut x = n;
    while x != 0 {
        x &= x - 1;
        count += 1;
    }
    count
}

fn main() {
    let n: i64 = 2_000_000;
    let k: i64 = 10;
    let mut nums = vec![0i64; n as usize];
    let mut state: i64 = 12345;
    for slot in nums.iter_mut() {
        state = (state * 1103515245 + 12345) % 2147483648;
        *slot = state;
    }
    let mut sink: i64 = 0;
    for round in 0..k {
        for &v in &nums {
            sink += hamming_weight(v ^ round);
        }
    }
    println!("{}", sink);
}
