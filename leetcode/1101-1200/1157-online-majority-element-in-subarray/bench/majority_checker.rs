// LeetCode #1157 bench: the ★ arm's vote tree and sorted places, the same
// workload as majority_checker.kara.

fn vote(a: (i64, i64), b: (i64, i64)) -> (i64, i64) {
    if a.0 == b.0 {
        (a.0, a.1 + b.1)
    } else if a.1 >= b.1 {
        (a.0, a.1 - b.1)
    } else {
        (b.0, b.1 - a.1)
    }
}

struct MajorityChecker {
    size: usize,
    tree: Vec<(i64, i64)>,
    places: Vec<Vec<i64>>,
}

impl MajorityChecker {
    fn new(arr: &[i32]) -> Self {
        let n = arr.len();
        let mut size = 1;
        while size < n {
            size *= 2;
        }
        let mut tree = vec![(0i64, 0i64); 2 * size];
        let mut places: Vec<Vec<i64>> = vec![Vec::new(); 20001];
        for (i, &x) in arr.iter().enumerate() {
            tree[size + i] = (x as i64, 1);
            places[x as usize].push(i as i64);
        }
        for i in (1..size).rev() {
            tree[i] = vote(tree[2 * i], tree[2 * i + 1]);
        }
        MajorityChecker { size, tree, places }
    }

    fn query(&self, left: i64, right: i64, threshold: i64) -> i64 {
        let mut lo = left as usize + self.size;
        let mut hi = right as usize + self.size + 1;
        let mut won = (0i64, 0i64);
        while lo < hi {
            if lo % 2 == 1 {
                won = vote(won, self.tree[lo]);
                lo += 1;
            }
            if hi % 2 == 1 {
                hi -= 1;
                won = vote(won, self.tree[hi]);
            }
            lo /= 2;
            hi /= 2;
        }
        let p = &self.places[won.0 as usize];
        let count = (p.partition_point(|&i| i <= right) - p.partition_point(|&i| i < left)) as i64;
        if count >= threshold { won.0 } else { -1 }
    }
}

fn main() {
    let passes = 100i64;
    let mut seed: i64 = 1157;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut checkers = Vec::new();
    let mut queries: Vec<Vec<(i64, i64, i64)>> = Vec::new();
    for kind in 0..4 {
        let v = 1 + next_random() % 20000;
        let arr: Vec<i32> = (0..20000)
            .map(|_| {
                let x = if kind == 0 {
                    1 + next_random() % 2
                } else if kind == 2 {
                    1 + next_random() % 20000
                } else if next_random() % 100 < (if kind == 1 { 67 } else { 50 }) {
                    v
                } else {
                    1 + next_random() % 20000
                };
                x as i32
            })
            .collect();
        checkers.push(MajorityChecker::new(&arr));
        let qs: Vec<(i64, i64, i64)> = (0..10000)
            .map(|_| {
                let a = next_random() % 20000;
                let b = next_random() % 20000;
                let (left, right) = (a.min(b), a.max(b));
                let least = (right - left + 1) / 2 + 1;
                (left, right, least + next_random() % (right - left + 2 - least))
            })
            .collect();
        queries.push(qs);
    }
    let mut check = 0i64;
    for p in 0..passes {
        for k in 0..4 {
            for &(left, right, threshold) in &queries[k] {
                check = (check * 31 + checkers[k].query(left, right, threshold) + p + 1) % 1000000007;
            }
        }
    }
    println!("{} passes over 4 arrays of 20000 values, 10000 queries each: checksum {}", passes, check);
}
