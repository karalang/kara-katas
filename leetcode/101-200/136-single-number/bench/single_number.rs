fn single_number(nums: &[i64]) -> i64 {
    let mut acc = 0i64;
    for &x in nums {
        acc ^= x;
    }
    acc
}

fn main() {
    let pairs: i64 = 140000;
    let passes: i64 = 3400;
    let n = 2 * pairs + 1;

    let mut nums: Vec<i64> = Vec::new();
    let mut state: i64 = 12345;
    for _ in 0..pairs {
        state = (state * 1103515245 + 12345) & 2147483647;
        let v = state >> 16;
        nums.push(v);
        nums.push(v);
    }
    state = (state * 1103515245 + 12345) & 2147483647;
    nums.push(state >> 16);

    let mut sink: i64 = 0;
    for p in 0..passes {
        let idx = ((p * 97 + 13) % n) as usize;
        nums[idx] ^= 1i64 << (p % 14);
        sink += single_number(&nums);
    }
    println!("{}", sink);
}
