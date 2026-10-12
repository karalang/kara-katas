// Benchmark for #457: mirror of circular_loop.kara (the ★ arm, slow and
// fast pointers) on the same workload.

fn next_index(a: &[i64], i: i64) -> i64 {
    let n = a.len() as i64;
    ((i + a[i as usize]) % n + n) % n
}

fn circular_array_loop(nums: &[i64]) -> bool {
    let mut a = nums.to_vec();
    let n = a.len() as i64;
    for start in 0..n {
        if a[start as usize] == 0 {
            continue;
        }
        let forward = a[start as usize] > 0;
        let mut slow = start;
        let mut fast = start;
        loop {
            let s = next_index(&a, slow);
            let f1 = next_index(&a, fast);
            if a[f1 as usize] == 0 || (a[f1 as usize] > 0) != forward {
                break;
            }
            let f2 = next_index(&a, f1);
            if a[f2 as usize] == 0 || (a[f2 as usize] > 0) != forward {
                break;
            }
            slow = s;
            fast = f2;
            if slow == fast {
                if next_index(&a, slow) != slow {
                    return true;
                }
                break;
            }
        }
        // Nothing on this path reaches a valid cycle: clear it.
        let mut i = start;
        while a[i as usize] != 0 && (a[i as usize] > 0) == forward {
            let next = next_index(&a, i);
            a[i as usize] = 0;
            i = next;
        }
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
    let mut seed: i64 = 457;
    let mut all: Vec<Vec<i64>> = Vec::new();
    for _ in 0..arrays {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..n {
            let step = 1 + next_random(&mut seed) % 1000;
            if next_random(&mut seed) % 2 == 0 {
                nums.push(step);
            } else {
                nums.push(-step);
            }
        }
        all.push(nums);
    }
    let mut found = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        for a in 0..arrays {
            let hi = next_random(&mut seed);
            let lo = next_random(&mut seed);
            let k = ((hi * 65536 + lo) % (n - 1)) as usize;
            let (one, two) = (all[a][k], all[a][k + 1]);
            if next_random(&mut seed) % 2 == 0 {
                all[a][k] = 1;
                all[a][k + 1] = n - 1;
            }
            let has = circular_array_loop(&all[a]);
            all[a][k] = one;
            all[a][k + 1] = two;
            if has {
                found += 1;
            }
            checksum = (checksum * 31 + if has { k as i64 + 1 } else { 0 }) % 1000000007;
        }
    }
    println!("{rounds} rounds on {arrays} arrays of {n}: {found} with a loop, checksum {checksum}");
}
