// LeetCode #1122: Relative Sort Array -- the bench in Rust: the ★ arm over
// 4 problems of 1000 values, each round swapping two values of each `arr1`
// and two of each `arr2` and sorting it again.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn relative_sort_array(arr1: &[i32], arr2: &[i32]) -> Vec<i32> {
    let mut count = vec![0i64; 1001];
    for &x in arr1 {
        count[x as usize] += 1;
    }
    let mut out = Vec::with_capacity(arr1.len());
    for &x in arr2 {
        for _ in 0..count[x as usize] {
            out.push(x);
        }
        count[x as usize] = 0;
    }
    for v in 0..1001 {
        for _ in 0..count[v] {
            out.push(v as i32);
        }
    }
    out
}

fn main() {
    let tops = [1000i64, 500, 100, 10];
    let mut seed = 1122i64;
    let mut ones: Vec<Vec<i32>> = Vec::new();
    let mut twos: Vec<Vec<i32>> = Vec::new();
    for &top in tops.iter() {
        let arr1: Vec<i32> = (0..1000).map(|_| (next_random(&mut seed) % (top + 1)) as i32).collect();
        let mut distinct = arr1.clone();
        distinct.sort();
        distinct.dedup();
        for j in (1..distinct.len()).rev() {
            let k = (next_random(&mut seed) % (j as i64 + 1)) as usize;
            distinct.swap(j, k);
        }
        let half = (distinct.len() + 1) / 2;
        twos.push(distinct[0..half].to_vec());
        ones.push(arr1);
    }
    let mut check = 0i64;
    for round in 0..5000usize {
        for j in 0..4 {
            let m = twos[j].len();
            ones[j].swap(round * 7919 % 1000, round * 104729 % 1000);
            twos[j].swap(round * 31 % m, round * 17 % m);
            let r = relative_sort_array(&ones[j], &twos[j]);
            for &x in r.iter() {
                check = (check * 31 + x as i64) % 1000000007;
            }
        }
    }
    println!("5000 rounds over 4 problems of 1000 values: checksum {check}");
}
