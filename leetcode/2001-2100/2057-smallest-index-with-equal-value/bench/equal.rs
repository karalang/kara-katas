// LeetCode #2057: Smallest Index With Equal Value -- Rust mirror of the ★
// arm's benchmark (equal.kara): the same 1000000 arrays drawn into one
// buffer, each answered by walking its indices from the front.

fn smallest_equal(nums: &[i64]) -> i64 {
    for i in 0..nums.len() {
        if (i % 10) as i64 == nums[i] {
            return i as i64;
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 2057;
    let mut nums: Vec<i64> = Vec::new();
    let (mut found, mut total, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..1000000 {
        let n = next_random(&mut seed) % 100 + 1;
        let rare = next_random(&mut seed) % 20 + 1;
        nums.clear();
        for i in 0..n {
            let d = next_random(&mut seed) % 10;
            nums.push(if d == i % 10 && next_random(&mut seed) % rare != 0 { (d + 1) % 10 } else { d });
        }
        let at = smallest_equal(&nums);
        if at >= 0 {
            found += 1;
        }
        total += at;
        check = (check * 31 + at + 2) % 1000000007;
    }
    println!("1000000 arrays: {found} found, sum {total}, checksum {check}");
}
