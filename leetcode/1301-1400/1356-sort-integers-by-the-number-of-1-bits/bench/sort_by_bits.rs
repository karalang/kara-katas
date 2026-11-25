// LeetCode #1356 bench -- Rust: one sort keyed by the pair (the number of
// 1 bits, the value).
fn sort_by_bits(arr: &[i32]) -> Vec<i32> {
    let mut sorted = arr.to_vec();
    sorted.sort_by_key(|&x| (x.count_ones(), x));
    sorted
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 20 arrays of 500 values from 0 to 10^4, the constraints' most, built
    // once; then 2 * 10^4 rounds, each setting one place of one array to a
    // value, all drawn from the checksum so far, sorting it, and folding
    // three values of the answer into the checksum
    let mut seed = 1356;
    let mut arrays: Vec<Vec<i32>> = Vec::new();
    for _ in 0..20 {
        let arr: Vec<i32> = (0..500).map(|_| (next_random(&mut seed) % 10001) as i32).collect();
        arrays.push(arr);
    }
    let mut check: i64 = 0;
    for r in 0..20000 {
        let k = (check % 20) as usize;
        arrays[k][((check / 20) % 500) as usize] = ((check / 10000) % 10001) as i32;
        let got = sort_by_bits(&arrays[k]);
        check = (check * 31
            + got[0] as i64
            + got[(check % 500) as usize] as i64 * 7
            + got[499] as i64 * 13
            + r)
            % 1000000007;
    }
    println!("20000 rounds over 20 arrays of 500 values: checksum {}", check);
}
