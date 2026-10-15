// Benchmark for #673: the length and count ending at each place, as the
// Kara ★ arm.

fn find_number_of_lis(nums: &[i64]) -> i64 {
    let n = nums.len();
    let mut length = vec![1i64; n];
    let mut count = vec![1i64; n];
    for i in 0..n {
        for j in 0..i {
            if nums[j] < nums[i] {
                if length[j] + 1 > length[i] {
                    length[i] = length[j] + 1;
                    count[i] = count[j];
                } else if length[j] + 1 == length[i] {
                    count[i] += count[j];
                }
            }
        }
    }
    let mut best = 0;
    for &v in &length {
        best = best.max(v);
    }
    let mut total = 0;
    for i in 0..n {
        if length[i] == best {
            total += count[i];
        }
    }
    total
}

fn main() {
    let rounds: i64 = 150;
    let size: i64 = 2000;
    let mut seed: i64 = 673;
    let mut sum: i64 = 0;
    for _ in 0..rounds {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..size {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            nums.push(seed / 65536);
        }
        sum = (sum * 31 + find_number_of_lis(&nums)) % 1000000007;
    }
    println!("{} arrays of {}: checksum {}", rounds, size, sum);
}
