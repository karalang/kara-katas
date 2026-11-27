// LeetCode #1822: Sign of the Product of an Array -- the bench in Rust: the
// ★ arm over 300000 calls on runs of 500 to 999 numbers cut from one list
// of 2000 numbers from -100 to 100 but zero, built once, each run's start
// and length drawn from the checksum so far.

fn array_sign(nums: Vec<i64>) -> i64 {
    let mut sign = 1;
    for &x in nums.iter() {
        if x == 0 {
            return 0;
        }
        if x < 0 {
            sign = -sign;
        }
    }
    sign
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1822;
    let mut base: Vec<i64> = Vec::new();
    for _ in 0..2000 {
        let x = next_random(&mut seed) % 200 - 100;
        base.push(if x >= 0 { x + 1 } else { x });
    }
    let mut check: i64 = 0;
    for call in 0..300000 {
        let start = ((check + call) % 1000) as usize;
        let n = (500 + (check * 7 + call) % 500) as usize;
        check = (check * 3 + array_sign(base[start..start + n].to_vec()) + 1) % 1000000007;
    }
    println!("300000 calls: checksum {}", check);
}
