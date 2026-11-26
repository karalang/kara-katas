// LeetCode #1494: Parallel Courses II -- the bench in Rust, mirroring
// min_number_of_semesters.kara: a DP over the sets of courses taken.

fn min_number_of_semesters(n: i32, relations: &[Vec<i32>], k: i32) -> i32 {
    let n = n as usize;
    let mut pre = vec![0i64; n];
    for r in relations {
        pre[(r[1] - 1) as usize] |= 1 << (r[0] - 1);
    }
    let full = (1i64 << n) - 1;
    let mut semesters = vec![i32::MAX; (full + 1) as usize];
    semesters[0] = 0;
    for taken in 0..full {
        let t = taken as usize;
        if semesters[t] == i32::MAX {
            continue;
        }
        let mut open = 0i64;
        for i in 0..n {
            if taken & (1 << i) == 0 && pre[i] & taken == pre[i] {
                open |= 1 << i;
            }
        }
        let next = semesters[t] + 1;
        if open.count_ones() as i32 <= k {
            let to = (taken | open) as usize;
            semesters[to] = semesters[to].min(next);
            continue;
        }
        let mut pick = open;
        while pick > 0 {
            if pick.count_ones() as i32 == k {
                let to = (taken | pick) as usize;
                semesters[to] = semesters[to].min(next);
            }
            pick = (pick - 1) & open;
        }
    }
    semesters[full as usize]
}

fn main() {
    let mut check: i64 = 0;
    for call in 0..300i64 {
        let mut seed = check + call;
        let mut next = || {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            seed / 65536
        };
        let dense = next() % 8;
        let k = 2 + next() % 4;
        let mut relations: Vec<Vec<i32>> = Vec::new();
        for a in 1..=15 {
            for b in a + 1..=15 {
                if next() % 100 < dense {
                    relations.push(vec![a, b]);
                }
            }
        }
        check = (check * 31 + min_number_of_semesters(15, &relations, k as i32) as i64) % 1000000007;
    }
    println!("300 calls on 15 courses: checksum {}", check);
}
