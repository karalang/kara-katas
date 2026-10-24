// Benchmark: LeetCode #949 Largest Time for Given Digits -- the ★ arm,
// every arrangement, on all 10000 arrays of four digits. Mirrors
// largest_time_from_digits.kara, .c, .py and go-seq/.

fn largest_time_from_digits(arr: &[i64]) -> String {
    let mut best: i64 = -1;
    for i in 0..4 {
        for j in 0..4 {
            if j == i {
                continue;
            }
            for k in 0..4 {
                if k == i || k == j {
                    continue;
                }
                let l = 6 - i - j - k;
                let hours = arr[i] * 10 + arr[j];
                let minutes = arr[k] * 10 + arr[l];
                if hours < 24 && minutes < 60 {
                    best = best.max(hours * 60 + minutes);
                }
            }
        }
    }
    if best < 0 {
        return String::new();
    }
    format!("{}{}:{}{}", best / 600, best / 60 % 10, best % 60 / 10, best % 10)
}

fn main() {
    let (rounds, count): (i64, i64) = (500, 10000);
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..count {
        arrays.push(vec![a / 1000, a / 100 % 10, a / 10 % 10, a % 10]);
    }
    let mut times = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let s = largest_time_from_digits(&arrays[((r * 37 + i) % count) as usize]);
            let mut v: i64 = 0;
            for c in s.bytes() {
                v = v * 131 + c as i64;
            }
            if !s.is_empty() {
                times += 1;
            }
            check = (check * 1000003 + v) % 1000000007;
        }
    }
    println!("{rounds} rounds over all {count} arrays of four digits: {times} times, checksum {check}");
}
