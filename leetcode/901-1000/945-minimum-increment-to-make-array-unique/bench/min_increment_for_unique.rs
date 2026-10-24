// Benchmark: LeetCode #945 Minimum Increment to Make Array Unique -- the
// ★ arm, sorted and raised, on arrays of 100000 values, LeetCode's
// longest. Mirrors min_increment_for_unique.kara, .c, .py and go-seq/.

fn min_increment_for_unique(nums: &[i64]) -> i64 {
    let mut a = nums.to_vec();
    a.sort();
    let mut moves = 0;
    let mut floor = -1;
    for &v in &a {
        let end = v.max(floor + 1);
        moves += end - v;
        floor = end;
    }
    moves
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (rounds, count, n) = (5, 20, 100000);
    let mut seed = 945;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let range = 70001 + next_random(&mut seed) * 4 % 30001;
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..n {
            let wide = next_random(&mut seed) * 32768 + next_random(&mut seed);
            nums.push(wide % range);
        }
        arrays.push(nums);
    }
    let mut total = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let m = min_increment_for_unique(&arrays[(r + i) % count]);
            total += m;
            check = (check * 1000003 + m) % 1000000007;
        }
    }
    println!("{rounds} rounds over {count} arrays of {n} values: {total} moves, checksum {check}");
}
