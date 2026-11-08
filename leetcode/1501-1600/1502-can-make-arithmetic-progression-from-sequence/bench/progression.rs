// LeetCode #1502: Can Make Arithmetic Progression From Sequence -- the
// benchmark, the same algorithm as progression.kara: sorted, every gap
// equal to the first.

fn can_make(arr: Vec<i64>) -> bool {
    let mut a = arr;
    a.sort();
    let d = a[1] - a[0];
    for i in 1..a.len() - 1 {
        if a[i + 1] - a[i] != d {
            return false;
        }
    }
    true
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn random_array(most: i64, seed: &mut i64) -> Vec<i64> {
    let n = next_random(seed) % (most - 1) + 2;
    let kind = next_random(seed) % 3;
    let mut arr = Vec::new();
    if kind == 2 {
        let spread = next_random(seed) % 50 + 1;
        for _ in 0..n {
            arr.push(next_random(seed) % spread - spread / 2);
        }
    } else {
        let start = next_random(seed) % 2001 - 1000;
        let d = next_random(seed) % 21 - 10;
        for i in 0..n {
            arr.push(start + i * d);
        }
        if kind == 1 {
            let at = (next_random(seed) % n) as usize;
            arr[at] += if next_random(seed) % 2 == 0 { 1 } else { -1 };
        }
    }
    for i in (1..n).rev() {
        let j = next_random(seed) % (i + 1);
        arr.swap(i as usize, j as usize);
    }
    arr
}

fn main() {
    let mut seed = 1502;
    let arrays: Vec<Vec<i64>> = (0..3000).map(|_| random_array(1000, &mut seed)).collect();
    let (mut can, mut check) = (0, 0);
    for _ in 0..10 {
        for arr in &arrays {
            let answer = if can_make(arr.clone()) { 1 } else { 0 };
            can += answer;
            check = mix(check, answer);
        }
    }
    println!("30000 answers over 3000 arrays of 2 to 1000 numbers: {can} can, checksum {check}");
}
