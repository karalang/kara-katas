// LeetCode #1053: Previous Permutation With One Swap -- Rust mirror of
// bench/prev_perm.kara.

fn prev_perm_opt1(arr: &[i64]) -> Vec<i64> {
    let mut out = arr.to_vec();
    let n = out.len() as i64;
    let mut i = n - 2;
    while i >= 0 && out[i as usize] <= out[i as usize + 1] {
        i -= 1;
    }
    if i < 0 {
        return out;
    }
    let i = i as usize;
    let mut j = n as usize - 1;
    while out[j] >= out[i] {
        j -= 1;
    }
    while out[j - 1] == out[j] {
        j -= 1;
    }
    out.swap(i, j);
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (count, n, rounds) = (200, 20000i64, 25);
    let mut seed = 1053;
    let mut all: Vec<(Vec<i64>, usize)> = Vec::new();
    for _ in 0..count {
        let run = next_random(&mut seed) % (n - 1) + 1;
        let mut arr = Vec::new();
        for _ in 0..n - run {
            arr.push(next_random(&mut seed) % 10000 + 1);
        }
        let mut v = next_random(&mut seed) % 1000 + 1;
        for _ in 0..run {
            arr.push(v);
            v += next_random(&mut seed) % 3;
        }
        all.push((arr, (n - run - 1) as usize));
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..rounds {
        for (arr, from) in &all {
            let answer = prev_perm_opt1(arr);
            let mut h = 0i64;
            for k in *from..n as usize {
                h = (h * 10007 + answer[k]) % 1000000007;
            }
            total += answer[*from];
            check = (check * 131 + h) % 1000000007;
        }
    }
    println!("{count} arrays of {n} values, {rounds} rounds: total {total}, checksum {check}");
}
