// LeetCode #2216: Minimum Deletions to Make Array Beautiful -- bench
// mirror of beautiful.kara: a number that would start a pair is deleted
// when the number after it is the same; an odd length left costs one more.

fn min_deletion(nums: &[i64]) -> i64 {
    let n = nums.len() as i64;
    let mut deleted: i64 = 0;
    for i in 0..n - 1 {
        if (i - deleted) % 2 == 0 && nums[i as usize] == nums[i as usize + 1] {
            deleted += 1;
        }
    }
    if (n - deleted) % 2 == 1 {
        deleted += 1;
    }
    deleted
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

// a draw of 30 bits, since one draw stops at 32767
fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2216;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..60 {
        // 10^5 numbers up to 1, 3 and 10^5 in turn
        let top = [1, 3, 100000][a % 3];
        arrays.push((0..100000).map(|_| wide_random(&mut seed) % (top + 1)).collect());
    }
    let mut check: i64 = 0;
    for a in 0..60 {
        for r in 0..20 {
            // punch: one number takes its neighbour's value before each answer
            arrays[a][r * 4999 + 1] = arrays[a][r * 4999];
            check = (check * 31 + min_deletion(&arrays[a])) % 1000000007;
        }
    }
    println!("60 arrays of 10^5, 20 punches: checksum {check}");
}
