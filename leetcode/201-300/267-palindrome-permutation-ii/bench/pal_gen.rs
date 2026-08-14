// Benchmark workload for LeetCode #267 — Palindrome Permutation II (Rust mirror).
// Mirrors pal_gen.kara algorithm-for-algorithm, including the hoisted output
// buffer (see that file for why no mirror builds a string per leaf).

fn build(counts: &mut [i64], half: &mut Vec<i64>, half_len: usize, middle: i64,
         buf: &mut [i64], acc: &mut i64) {
    if half.len() == half_len {
        let mut n = 0usize;
        for i in 0..half_len {
            buf[n] = half[i];
            n += 1;
        }
        if middle >= 0 {
            buf[n] = middle;
            n += 1;
        }
        for j in (0..half_len).rev() {
            buf[n] = half[j];
            n += 1;
        }
        for k in 0..n {
            *acc = (*acc * 31 + buf[k]) % 1000000007;
        }
        return;
    }
    for c in 0..128usize {
        if counts[c] > 0 {
            counts[c] -= 1;
            half.push(c as i64);
            build(counts, half, half_len, middle, buf, acc);
            half.pop();
            counts[c] += 1;
        }
    }
}

fn main() {
    let pairs: i64 = 8;
    let rounds: i64 = 44;

    let mut buf = vec![0i64; 64];

    let mut sink: i64 = 0;
    for r in 0..rounds {
        let mut counts = vec![0i64; 128];
        for p in 0..pairs {
            counts[(97 + p) as usize] = 2;
        }
        counts[(97 + r % pairs) as usize] += 1;

        let mut middle: i64 = -1;
        let mut half_len: i64 = 0;
        for c in 0..128usize {
            if counts[c] % 2 == 1 {
                middle = c as i64;
            }
            counts[c] /= 2;
            half_len += counts[c];
        }

        let mut acc: i64 = 0;
        let mut half: Vec<i64> = Vec::new();
        build(&mut counts, &mut half, half_len as usize, middle, &mut buf, &mut acc);
        sink = (sink * 131 + acc) % 1000000007;
    }

    println!("{}", sink);
}
