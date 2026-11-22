// LeetCode #2848: Points That Intersect With Cars -- the bench,
// mirrored from points.kara: each car marks its points on a road of
// 100, and the marked ones are counted.

fn number_of_points(nums: &[Vec<i64>]) -> i64 {
    let mut covered = [false; 101];
    for car in nums.iter() {
        for x in car[0]..car[1] + 1 {
            covered[x as usize] = true;
        }
    }
    covered.iter().filter(|&&c| c).count() as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 10000;
    let rounds = 50;
    let mut seed = 2848;
    let mut parkings: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..count {
        let cars = next_random(&mut seed) % 100 + 1;
        let nums: Vec<Vec<i64>> = (0..cars)
            .map(|_| {
                let start = next_random(&mut seed) % 100 + 1;
                let a = next_random(&mut seed);
                let length = a % (next_random(&mut seed) % 100 + 1);
                vec![start, (start + length).min(100)]
            })
            .collect();
        parkings.push(nums);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in parkings.iter() {
            let points = number_of_points(nums);
            total += points;
            check = (check * 31 + points + r) % 1000000007;
        }
    }
    println!("{count} parkings, {rounds} rounds: {total} points, checksum {check}");
}
