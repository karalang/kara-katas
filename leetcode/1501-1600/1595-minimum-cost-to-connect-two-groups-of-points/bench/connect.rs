// LeetCode #1595: Minimum Cost to Connect Two Groups of Points
// -- the bench in Rust, mirroring connect.kara: one edge per first point
// over a mask of the second group's points joined, then each point still
// alone takes its cheapest edge; 200 problems of 12 by 12, costs from 0
// to 100, all drawn first.

fn connect_two_groups(cost: &[Vec<i32>]) -> i32 {
    let first = cost.len();
    let second = cost[0].len();
    let full = 1usize << second;
    let cheapest: Vec<i32> = (0..second).map(|j| (0..first).map(|i| cost[i][j]).min().unwrap()).collect();
    let mut best = vec![i32::MAX; full];
    best[0] = 0;
    for i in 0..first {
        let mut next = vec![i32::MAX; full];
        for mask in 0..full {
            if best[mask] == i32::MAX {
                continue;
            }
            for j in 0..second {
                let joined = mask | 1 << j;
                next[joined] = next[joined].min(best[mask] + cost[i][j]);
            }
        }
        best = next;
    }
    let mut answer = i32::MAX;
    for mask in 0..full {
        if best[mask] == i32::MAX {
            continue;
        }
        let mut total = best[mask];
        for j in 0..second {
            if mask >> j & 1 == 0 {
                total += cheapest[j];
            }
        }
        answer = answer.min(total);
    }
    answer
}

fn main() {
    let mut seed: i64 = 1595;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let problems: Vec<Vec<Vec<i32>>> = (0..200)
        .map(|_| (0..12).map(|_| (0..12).map(|_| (next_random() % 101) as i32).collect()).collect())
        .collect();
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for cost in &problems {
        let answer = connect_two_groups(cost);
        total += answer as i64;
        check = (check * 31 + answer as i64 + 1) % 1000000007;
    }
    println!("200 problems of 12 by 12: total {}, checksum {}", total, check);
}
