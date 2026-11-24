// LeetCode #1313 bench, Rust: the ★ arm (the list read two numbers at a
// time, each pair's value pushed as many times as its count) on the same
// 100 lists and 2000 passes.

fn decompress_rl_elist(nums: &[i64]) -> Vec<i64> {
    let mut out = Vec::new();
    for pair in nums.chunks(2) {
        for _ in 0..pair[0] {
            out.push(pair[1]);
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1313;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..100 {
        let mut nums = Vec::new();
        for _ in 0..100 {
            nums.push(1 + next_random(&mut seed) % 100);
        }
        lists.push(nums);
    }
    let mut check: i64 = 0;
    for pass in 0..2000 {
        for l in 0..100 {
            lists[l][(2 * (check % 50)) as usize] = 1 + (check / 7) % 100;
            lists[l][(2 * ((check / 11) % 50) + 1) as usize] = 1 + (check / 13) % 100;
            let got = decompress_rl_elist(&lists[l]);
            let n = got.len() as i64;
            check = (check * 31 + n) % 1000000007;
            check = (check * 31 + got[(check % n) as usize]) % 1000000007;
            check = (check * 31 + got[((check / 3) % n) as usize] + pass) % 1000000007;
        }
    }
    println!("2000 passes over 100 lists of 50 pairs: checksum {}", check);
}
