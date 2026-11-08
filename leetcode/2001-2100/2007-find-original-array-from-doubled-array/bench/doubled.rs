// LeetCode #2007: Find Original Array From Doubled Array -- the ★ arm's
// benchmark, a mirror of doubled.kara.

fn find_original_array(changed: &[i64]) -> Vec<i64> {
    if changed.len() % 2 == 1 {
        return Vec::new();
    }
    let top = *changed.iter().max().unwrap();
    let mut count = vec![0i64; (top + 1) as usize];
    for &x in changed {
        count[x as usize] += 1;
    }
    if count[0] % 2 == 1 {
        return Vec::new();
    }
    let mut original: Vec<i64> = Vec::new();
    for _ in 0..count[0] / 2 {
        original.push(0);
    }
    for v in 1..=top {
        let c = count[v as usize];
        if c == 0 {
            continue;
        }
        if 2 * v > top || count[(2 * v) as usize] < c {
            return Vec::new();
        }
        count[(2 * v) as usize] -= c;
        for _ in 0..c {
            original.push(v);
        }
    }
    original
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2007i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..2000 {
        let mut changed: Vec<i64> = Vec::new();
        for _ in 0..500 {
            let x = next_random(&mut seed) % 5001;
            changed.push(x);
            changed.push(2 * x);
        }
        for i in (1..changed.len()).rev() {
            let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
            changed.swap(i, j);
        }
        if next_random(&mut seed) % 3 == 0 {
            let i = (next_random(&mut seed) % changed.len() as i64) as usize;
            changed[i] += 1;
        }
        arrays.push(changed);
    }
    let (mut calls, mut sum, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..25 {
        for changed in &arrays {
            let original = find_original_array(changed);
            let mut total = original.len() as i64;
            for v in original {
                total += v;
            }
            calls += 1;
            sum += total;
            check = (check * 31 + total) % 1000000007;
        }
    }
    println!("{calls} calls: sum {sum}, checksum {check}");
}
