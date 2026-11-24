// LeetCode #1300 bench: the ★ arm (the numbers sorted and walked from the
// smallest; the best cap is the target's share of what is left, rounded down
// or up) over 50 arrays of 10^4 numbers, up to 20, 100, 1000, 10^4 or 10^5 in
// turn, built once; then 200 passes, each setting one number of every array
// and its target from the checksum so far, answering it, and folding the
// answer into the checksum.

fn find_best_value(arr: &[i64], target: i64) -> i64 {
    let mut sorted = arr.to_vec();
    sorted.sort();
    let n = sorted.len() as i64;
    let mut before = 0;
    for i in 0..n {
        let left = n - i;
        let v = sorted[i as usize];
        if before + v * left >= target {
            let x = (target - before) / left;
            let low = (before + x * left - target).abs();
            let high = (before + (x + 1) * left - target).abs();
            return if low <= high { x } else { x + 1 };
        }
        before += v;
    }
    sorted[(n - 1) as usize]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let tops = [20i64, 100, 1000, 10000, 100000];
    let mut seed = 1300;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for t in 0..50 {
        let mut arr: Vec<i64> = Vec::new();
        for _ in 0..10000 {
            let hi = next_random(&mut seed);
            arr.push(1 + (hi * 32768 + next_random(&mut seed)) % tops[t % 5]);
        }
        arrays.push(arr);
    }
    let mut check: i64 = 0;
    for p in 0..200 {
        for (t, arr) in arrays.iter_mut().enumerate() {
            arr[(check % 10000) as usize] = 1 + check % tops[t % 5];
            let target = 1 + (check * 7919) % 100000;
            check = (check * 31 + find_best_value(arr, target) + p) % 1000000007;
        }
    }
    println!("200 passes over 50 arrays of 10^4: checksum {}", check);
}
