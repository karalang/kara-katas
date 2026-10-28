// Benchmark: LeetCode #1007 Minimum Domino Rotations For Equal Row -- the
// ★ arm, two candidates, on rows of 20000 dominoes, LeetCode's longest.
// Mirrors min_rotations.kara, .c, .py and go-seq/.

fn rotations(tops: &[i64], bottoms: &[i64], v: i64) -> i64 {
    let mut to_top = 0;
    let mut to_bottom = 0;
    for i in 0..tops.len() {
        if tops[i] != v && bottoms[i] != v {
            return -1;
        }
        if tops[i] != v {
            to_top += 1;
        } else if bottoms[i] != v {
            to_bottom += 1;
        }
    }
    to_top.min(to_bottom)
}

fn min_domino_rotations(tops: &[i64], bottoms: &[i64]) -> i64 {
    let a = rotations(tops, bottoms, tops[0]);
    let b = rotations(tops, bottoms, bottoms[0]);
    if a == -1 {
        b
    } else if b == -1 {
        a
    } else {
        a.min(b)
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds: i64 = 400;
    let n: i64 = 20000;
    let mut seed: i64 = 1007;
    let mut all_tops: Vec<Vec<i64>> = Vec::new();
    let mut all_bottoms: Vec<Vec<i64>> = Vec::new();
    for t in 0..20i64 {
        let target = t % 6 + 1;
        let mut tops = Vec::new();
        let mut bottoms = Vec::new();
        for _ in 0..n {
            let mut top = 1 + next_random(&mut seed) % 6;
            let mut bottom = 1 + next_random(&mut seed) % 6;
            if t % 2 == 0 || next_random(&mut seed) % 2000 != 0 {
                if next_random(&mut seed) % 2 == 0 {
                    top = target;
                } else {
                    bottom = target;
                }
            }
            tops.push(top);
            bottoms.push(bottom);
        }
        all_tops.push(tops);
        all_bottoms.push(bottoms);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..20i64 {
            let t = ((r + i) % 20) as usize;
            let got = min_domino_rotations(&all_tops[t], &all_bottoms[t]);
            total += got;
            check = (check * 31 + got + 2) % 1000000007;
        }
    }
    println!("{rounds} rounds over 20 rows of {n} dominoes: answers sum to {total}, checksum {check}");
}
