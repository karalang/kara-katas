// benchmark's Rust mirror of collisions.kara (LeetCode #2211, the ★ arm):
// skip the leading 'L's and the trailing 'R's and count the cars between
// that are not 'S'.

fn count_collisions(directions: &str) -> i64 {
    let cars: Vec<char> = directions.chars().collect();
    let mut lo = 0;
    while lo < cars.len() && cars[lo] == 'L' {
        lo += 1;
    }
    let mut hi = cars.len();
    while hi > lo && cars[hi - 1] == 'R' {
        hi -= 1;
    }
    let mut count = 0;
    for &car in &cars[lo..hi] {
        if car != 'S' {
            count += 1;
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2211;
    let mut roads: Vec<String> = Vec::new();
    for r in 0..20 {
        // a run of left-movers at the front and right-movers at the back,
        // each r thousand cars long, around random cars
        let mut road = String::new();
        for i in 0..100000 {
            road.push(if i < r * 1000 {
                'L'
            } else if i >= 100000 - r * 1000 {
                'R'
            } else {
                ['L', 'R', 'S'][(next_random(&mut seed) % 3) as usize]
            });
        }
        roads.push(road);
    }
    let mut check: i64 = 0;
    for p in 0..10 {
        for road in &roads {
            check = (check * 31 + count_collisions(road) + p) % 1000000007;
        }
    }
    println!("10 passes over 20 roads: checksum {check}");
}
