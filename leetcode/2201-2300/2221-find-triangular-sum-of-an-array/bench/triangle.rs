// LeetCode #2221: Find Triangular Sum of an Array -- bench mirror of
// triangle.kara: the rounds done in place, each writing
// (nums[i] + nums[i + 1]) % 10 over nums[i].

fn triangular_sum(nums: &[i64]) -> i64 {
    let mut row = nums.to_vec();
    let n = row.len();
    for live in (1..n).rev() {
        for i in 0..live {
            row[i] = (row[i] + row[i + 1]) % 10;
        }
    }
    row[0]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2221;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..8 {
        // 1000 digits, the constraints' largest
        arrays.push((0..1000).map(|_| next_random(&mut seed) % 10).collect());
    }
    let mut check: i64 = 0;
    for a in 0..8 {
        for r in 0..8 {
            // punch: one digit is drawn again before each answer
            arrays[a][r * 113] = next_random(&mut seed) % 10;
            check = (check * 31 + triangular_sum(&arrays[a])) % 1000000007;
        }
    }
    println!("8 arrays of 1000 digits, 8 punches: checksum {check}");
}
