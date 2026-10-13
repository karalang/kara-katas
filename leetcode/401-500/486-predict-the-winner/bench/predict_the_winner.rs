// Benchmark for #486: Rust mirror of the ★ arm (one row of leads); see
// predict_the_winner.kara.

fn predict_the_winner(nums: &[i64]) -> bool {
    let n = nums.len() as i64;
    let mut d = nums.to_vec();
    let mut i = n - 2;
    while i >= 0 {
        for j in (i + 1) as usize..n as usize {
            d[j] = (nums[i as usize] - d[j]).max(nums[j] - d[j - 1]);
        }
        i -= 1;
    }
    d[(n - 1) as usize] >= 0
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    let mut seed: i64 = 486;
    for a in 0..200 {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..1000 + a % 2 {
            nums.push(next_random(&mut seed) * 32768 % 10000001);
        }
        arrays.push(nums);
    }
    let mut wins: i64 = 0;
    let mut checksum: i64 = 0;
    for nums in &arrays {
        let win = if predict_the_winner(nums) { 1 } else { 0 };
        wins += win;
        checksum = (checksum * 31 + win * 7 + nums.len() as i64) % 1000000007;
    }
    println!("200 arrays of 1000 or 1001 numbers: player 1 wins {wins}, checksum {checksum}");
}
