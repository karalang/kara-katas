// Benchmark: LeetCode #1093 Statistics from a Large Sample -- the ★ arm, two
// walks over the counts. Mirrors sample_stats.kara.

fn sample_stats(count: &[i64]) -> Vec<f64> {
    let mut low: i64 = -1;
    let mut high: i64 = 0;
    let mut sum: i64 = 0;
    let mut total: i64 = 0;
    let mut mode: usize = 0;
    for k in 0..count.len() {
        let c = count[k];
        if c == 0 {
            continue;
        }
        if low < 0 {
            low = k as i64;
        }
        high = k as i64;
        sum += k as i64 * c;
        total += c;
        if c > count[mode] {
            mode = k;
        }
    }
    let (left, right) = ((total - 1) / 2, total / 2);
    let mut seen = 0;
    let mut median_low: i64 = -1;
    let mut median_high: i64 = -1;
    for k in 0..count.len() {
        seen += count[k];
        if median_low < 0 && seen > left {
            median_low = k as i64;
        }
        if seen > right {
            median_high = k as i64;
            break;
        }
    }
    vec![low as f64, high as f64, sum as f64 / total as f64, (median_low + median_high) as f64 / 2.0, mode as f64]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1093;
    let mut samples: Vec<Vec<i64>> = Vec::new();
    for k in 0..64 {
        let mut c = vec![0i64; 256];
        for _ in 0..4 + k * 4 {
            let p = (next_random(&mut seed) % 256) as usize;
            c[p] = next_random(&mut seed) * 91 % 3000000 + 1;
        }
        samples.push(c);
    }
    let mut modes: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..10000usize {
        for j in 0..samples.len() {
            samples[j][(round * 7 + j * 13) % 256] += 1;
            let s = sample_stats(&samples[j]);
            modes += s[4] as i64;
            for x in s.iter() {
                check = (check * 31 + (x * 1000000.0) as i64) % 1000000007;
            }
        }
    }
    println!("10000 rounds over 64 samples: modes sum to {}, checksum {}", modes, check);
}
