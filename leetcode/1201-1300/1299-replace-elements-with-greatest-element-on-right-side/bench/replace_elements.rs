// LeetCode #1299 bench: the ★ arm (one walk from the right end, each place
// given the greatest seen so far) over 50 arrays of 10^4 numbers up to 10^5,
// built once; then 1000 passes, each setting one number of every array from the
// checksum so far, answering it, and folding two of its answers, chosen by the
// checksum, into the checksum.

fn replace_elements(arr: &[i64]) -> Vec<i64> {
    let n = arr.len();
    let mut out = vec![-1i64; n];
    let mut greatest = -1;
    for i in (0..n).rev() {
        out[i] = greatest;
        if arr[i] > greatest {
            greatest = arr[i];
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1299;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..50 {
        let mut arr: Vec<i64> = Vec::new();
        for _ in 0..10000 {
            let hi = next_random(&mut seed);
            arr.push(1 + (hi * 32768 + next_random(&mut seed)) % 100000);
        }
        arrays.push(arr);
    }
    let mut check: i64 = 0;
    for p in 0..1000 {
        for arr in arrays.iter_mut() {
            arr[(check % 10000) as usize] = 1 + check * 7919 % 100000;
            let out = replace_elements(arr);
            check = (check * 31 + out[(check % 10000) as usize] + out[((check / 7) % 10000) as usize] + p) % 1000000007;
        }
    }
    println!("1000 passes over 50 arrays of 10^4: checksum {}", check);
}
