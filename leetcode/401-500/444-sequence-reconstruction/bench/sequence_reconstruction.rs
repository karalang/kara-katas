// Benchmark for #444: mirror of sequence_reconstruction.kara (positions
// and neighbouring pairs) on 50 random cases of n = 5,000, built once
// and answered 30 times over.

fn sequence_reconstruction(nums: &[i64], sequences: &[Vec<i64>]) -> bool {
    let n = nums.len();
    let mut position = vec![0usize; n + 1];
    for i in 0..n {
        position[nums[i] as usize] = i;
    }
    let mut covered = vec![false; n];
    for s in sequences {
        for j in 1..s.len() {
            let a = position[s[j - 1] as usize];
            let b = position[s[j] as usize];
            if a >= b {
                return false;
            }
            if b == a + 1 {
                covered[a] = true;
            }
        }
    }
    for i in 0..n.saturating_sub(1) {
        if !covered[i] {
            return false;
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 50;
    let n: i64 = 5000;
    let rounds = 30;
    let mut seed: i64 = 444;
    let mut cases_nums: Vec<Vec<i64>> = Vec::new();
    let mut cases_sequences: Vec<Vec<Vec<i64>>> = Vec::new();
    let mut values = 0;
    for c in 0..count {
        let mut nums: Vec<i64> = (1..n + 1).collect();
        let mut i = n - 1;
        while i > 0 {
            let j = next_random(&mut seed) % (i + 1);
            nums.swap(i as usize, j as usize);
            i -= 1;
        }
        let mut sequences: Vec<Vec<i64>> = Vec::new();
        let windows = 1 + next_random(&mut seed) % (n * 2 + 2);
        for _ in 0..windows {
            let start = next_random(&mut seed) % n;
            let length = 1 + next_random(&mut seed) % 12;
            let mut s: Vec<i64> = Vec::new();
            for k in start..(start + length).min(n) {
                if s.is_empty() || next_random(&mut seed) % 10 != 0 {
                    s.push(nums[k as usize]);
                }
            }
            values += s.len();
            sequences.push(s);
        }
        if c % 2 == 0 {
            values += n as usize;
            sequences.push(nums.clone());
        }
        cases_nums.push(nums);
        cases_sequences.push(sequences);
    }
    let mut true_count = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for c in 0..count {
            let answer = sequence_reconstruction(&cases_nums[c], &cases_sequences[c]);
            if answer {
                true_count += 1;
            }
            checksum =
                (checksum * 31 + c as i64 * 2 + if answer { 1 } else { 0 } + round) % 1000000007;
        }
    }
    println!("{rounds} rounds on {count} cases of n = {n} ({values} values in sequences): {true_count} true, checksum {checksum}");
}
