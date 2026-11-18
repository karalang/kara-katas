// LeetCode #1200 bench: the ★ arm in Rust, over the same 20 arrays of 10^5
// values and 10 rounds as the Kāra bench; each call sorts its own copy with
// the standard `sort`.

fn minimum_abs_difference(mut arr: Vec<i64>) -> Vec<[i64; 2]> {
    arr.sort();
    let mut least = i64::MAX;
    for i in 1..arr.len() {
        least = least.min(arr[i] - arr[i - 1]);
    }
    let mut pairs = Vec::new();
    for i in 1..arr.len() {
        if arr[i] - arr[i - 1] == least {
            pairs.push([arr[i - 1], arr[i]]);
        }
    }
    pairs
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let spans = [1000000i64, 100000, 60000];
    let mut seed = 1200;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for k in 0..20 {
        let span = spans[k % 3];
        let mut taken = vec![false; (2 * span + 1) as usize];
        let mut arr = Vec::new();
        while arr.len() < 100000 {
            let a = next_random(&mut seed);
            let b = next_random(&mut seed);
            let v = (a * 32768 + b) % (2 * span + 1) - span;
            if !taken[(v + span) as usize] {
                taken[(v + span) as usize] = true;
                arr.push(v);
            }
        }
        arrays.push(arr);
    }
    let mut check: i64 = 0;
    for _ in 0..10 {
        for arr in &arrays {
            let pairs = minimum_abs_difference(arr.clone());
            check = (check * 131 + pairs.len() as i64) % 1000000007;
            for p in &pairs {
                check = (check * 131 + p[0] + p[1] + 2000000) % 1000000007;
            }
        }
    }
    println!("10 rounds of 20 arrays of 100000 values: checksum {}", check);
}
