// LeetCode #1460 bench in Rust: the ★ arm (both arrays sorted and
// compared) on the same 200 pairs of 1000 values and 50 passes.

fn can_be_equal(target: &[i32], arr: &[i32]) -> bool {
    let mut a = target.to_vec();
    let mut b = arr.to_vec();
    a.sort();
    b.sort();
    a == b
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1460i64;
    let mut targets: Vec<Vec<i32>> = Vec::new();
    let mut arrs: Vec<Vec<i32>> = Vec::new();
    for _ in 0..200 {
        let target: Vec<i32> = (0..1000).map(|_| (1 + next_random(&mut seed) % 1000) as i32).collect();
        let mut arr = target.clone();
        for i in (1..1000usize).rev() {
            let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
            arr.swap(i, j);
        }
        targets.push(target);
        arrs.push(arr);
    }
    let mut check: i64 = 0;
    for pass in 0..50 {
        for p in 0..200 {
            let k = (check % 1000) as usize;
            arrs[p][k] = targets[p][((check / 7) % 1000) as usize];
            let same = can_be_equal(&targets[p], &arrs[p]);
            check = (check * 31 + if same { 1 } else { 0 } + pass) % 1000000007;
        }
    }
    println!("50 passes over 200 pairs of 1000 values: checksum {check}");
}
