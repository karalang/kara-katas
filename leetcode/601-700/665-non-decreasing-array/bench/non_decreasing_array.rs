// Benchmark for #665: fix each drop as it comes, as the Kara ★ arm.

fn check_possibility(nums: &[i64]) -> bool {
    let mut a = nums.to_vec();
    let mut fixes = 0;
    for i in 1..a.len() {
        if a[i] < a[i - 1] {
            fixes += 1;
            if fixes > 1 {
                return false;
            }
            if i < 2 || a[i - 2] <= a[i] {
                a[i - 1] = a[i];
            } else {
                a[i] = a[i - 1];
            }
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 665;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for t in 0..16 {
        let mut v: Vec<i64> = Vec::new();
        let mut x = -100000i64;
        for _ in 0..10000 {
            v.push(x);
            x += next_random(&mut seed) % 21;
        }
        for _ in 0..t % 3 {
            let at = (next_random(&mut seed) % 10000) as usize;
            v[at] = next_random(&mut seed) % 200001 - 100000;
        }
        arrays.push(v);
    }
    let rounds = 40000i64;
    let mut yes = 0;
    let mut sum = 0i64;
    for r in 0..rounds {
        let ok = check_possibility(&arrays[(r % 16) as usize]);
        if ok {
            yes += 1;
        }
        sum = (sum * 31 + r * 2 + if ok { 1 } else { 0 }) % 1000000007;
    }
    println!("16 arrays of 10000, {} rounds: {} can be sorted, checksum {}", rounds, yes, sum);
}
