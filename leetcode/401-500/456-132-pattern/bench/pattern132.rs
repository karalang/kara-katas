// Benchmark for #456: mirror of pattern132.kara (the ★ arm, one stack
// from the right) on the same workload.

fn find132pattern(nums: &[i64]) -> bool {
    let mut stack: Vec<i64> = Vec::new();
    let mut third = i64::MIN;
    for &x in nums.iter().rev() {
        if x < third {
            return true;
        }
        while let Some(&top) = stack.last() {
            if top >= x {
                break;
            }
            third = top;
            stack.pop();
        }
        stack.push(x);
    }
    false
}

// ---- benchmark --------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let arrays = 10;
    let n: i64 = 1000000;
    let rounds = 5;
    let mut seed: i64 = 456;
    let mut all: Vec<Vec<i64>> = Vec::new();
    for _ in 0..arrays {
        let mut nums: Vec<i64> = Vec::new();
        let mut top: i64 = 1000000000;
        while (nums.len() as i64) < n {
            let run = (1 + next_random(&mut seed) % 1000).min(n - nums.len() as i64);
            let low = top - run * 10 - 1 - next_random(&mut seed) % 100;
            for t in 0..run {
                nums.push(low + t * 10 + next_random(&mut seed) % 10);
            }
            top = low;
        }
        all.push(nums);
    }
    let mut found = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        for a in 0..arrays {
            let hi = next_random(&mut seed);
            let lo = next_random(&mut seed);
            let at = (hi * 65536 + lo) % n;
            let old = all[a][at as usize];
            let hi = next_random(&mut seed);
            let lo = next_random(&mut seed);
            let value = (hi * 65536 + lo) % 2000000001 - 1000000000;
            if next_random(&mut seed) % 2 == 0 {
                all[a][at as usize] = value;
            }
            let has = find132pattern(&all[a]);
            all[a][at as usize] = old;
            if has {
                found += 1;
            }
            checksum = (checksum * 31 + if has { at + 1 } else { 0 }) % 1000000007;
        }
    }
    println!(
        "{rounds} rounds on {arrays} arrays of {n}: {found} with the pattern, checksum {checksum}"
    );
}
