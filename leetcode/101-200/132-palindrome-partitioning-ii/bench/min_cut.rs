// Benchmark harness for LeetCode #132 — Palindrome Partitioning II.
// Mirrors min_cut.kara algorithm-for-algorithm, including the nested
// Vec<Vec<bool>> palindrome table.

fn min_cut(s: &str) -> i64 {
    let bytes = s.as_bytes();
    let n = bytes.len() as i64;
    if n <= 1 {
        return 0;
    }

    let mut pal: Vec<Vec<bool>> = Vec::new();
    for i in 0..n {
        let mut row: Vec<bool> = Vec::new();
        for j in 0..n {
            row.push(i == j);
        }
        pal.push(row);
    }

    let mut length: i64 = 2;
    while length <= n {
        let mut lo: i64 = 0;
        while lo <= n - length {
            let hi = lo + length - 1;
            let ends_match = bytes[lo as usize] == bytes[hi as usize];
            let inner_ok = length == 2 || pal[(lo + 1) as usize][(hi - 1) as usize];
            if ends_match && inner_ok {
                pal[lo as usize][hi as usize] = true;
            }
            lo += 1;
        }
        length += 1;
    }

    let mut cut: Vec<i64> = vec![0; n as usize];
    for i in 0..n {
        if pal[0][i as usize] {
            cut[i as usize] = 0;
        } else {
            let mut best = i;
            let mut j: i64 = 1;
            while j <= i {
                if pal[j as usize][i as usize] && (cut[(j - 1) as usize] + 1) < best {
                    best = cut[(j - 1) as usize] + 1;
                }
                j += 1;
            }
            cut[i as usize] = best;
        }
    }
    cut[(n - 1) as usize]
}

fn lcg_str(seed: i64, n: i64, alpha: i64) -> String {
    let alphabet = "abcdefghijklmnopqrstuvwxyz";
    let mut out = String::new();
    let mut x = seed;
    for _ in 0..n {
        x = (x * 1103515245 + 12345) % 2147483648;
        let target = (x / 65536) % alpha;
        for (idx, ch) in alphabet.chars().enumerate() {
            if idx as i64 == target {
                out.push(ch);
            }
        }
    }
    out
}

fn main() {
    let n: i64 = 500;
    let iters: i64 = 400;

    let cases = [
        lcg_str(1, n, 2),
        lcg_str(2, n, 4),
        lcg_str(3, n, 26),
        lcg_str(4, n, 3),
    ];

    let np = cases.len() as i64;
    let mut sink: i64 = 0;
    for it in 0..iters {
        let idx = ((it * 3) % np) as usize;
        sink = (sink + min_cut(&cases[idx])) % 1000000007;
    }
    println!("{}", sink);
}
