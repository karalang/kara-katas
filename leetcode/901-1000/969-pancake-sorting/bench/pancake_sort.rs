// Benchmark: LeetCode #969 Pancake Sorting -- the ★ arm, the largest
// pancake to the bottom one at a time, on 200 random stacks of 100
// pancakes. Mirrors pancake_sort.kara, .c, .py and go-seq/.

fn flip(a: &mut [i64], k: usize) {
    let mut i = 0;
    let mut j = k - 1;
    while i < j {
        a.swap(i, j);
        i += 1;
        j -= 1;
    }
}

fn pancake_sort(arr: &[i64]) -> Vec<i64> {
    let mut a = arr.to_vec();
    let mut flips = Vec::new();
    let mut size = a.len();
    while size > 1 {
        let mut i = 0;
        while a[i] != size as i64 {
            i += 1;
        }
        if i != size - 1 {
            if i != 0 {
                flip(&mut a, i + 1);
                flips.push((i + 1) as i64);
            }
            flip(&mut a, size);
            flips.push(size as i64);
        }
        size -= 1;
    }
    flips
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_permutation(n: i64, seed: &mut i64) -> Vec<i64> {
    let mut a: Vec<i64> = (1..=n).collect();
    let mut i = n - 1;
    while i > 0 {
        let j = next_random(seed) % (i + 1);
        a.swap(i as usize, j as usize);
        i -= 1;
    }
    a
}

fn main() {
    let rounds = 100;
    let count = 200;
    let mut seed = 969;
    let stacks: Vec<Vec<i64>> = (0..count).map(|_| random_permutation(100, &mut seed)).collect();
    let mut flips: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for s in 0..count {
            for k in pancake_sort(&stacks[(r + s) % count]) {
                flips += 1;
                check = (check * 131 + k) % 1000000007;
            }
        }
    }
    println!("{rounds} rounds over {count} stacks of 100 pancakes: {flips} flips, checksum {check}");
}
