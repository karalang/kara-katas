// LeetCode #2079: Watering Plants -- Rust mirror of the ★ arm's benchmark
// (water.kara): 2000 gardens of 1000 plants built first, then every
// garden answered for 500 cans, from 1000 up by 97 a can.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn watering_plants(plants: &[i64], capacity: i64) -> i64 {
    let mut steps = 0;
    let mut can = capacity;
    for (i, &need) in plants.iter().enumerate() {
        if can < need {
            steps += 2 * i as i64;
            can = capacity;
        }
        steps += 1;
        can -= need;
    }
    steps
}

fn main() {
    let mut seed = 2079;
    let mut gardens: Vec<Vec<i64>> = Vec::new();
    for _ in 0..2000 {
        let plants: Vec<i64> = (0..1000).map(|_| next_random(&mut seed) % 1000 + 1).collect();
        gardens.push(plants);
    }
    let (mut total, mut check) = (0i64, 0i64);
    for plants in &gardens {
        for k in 0..500 {
            let a = watering_plants(plants, 1000 + 97 * k);
            total += a;
            check = (check * 31 + a) % 1000000007;
        }
    }
    println!("1000000 answers: sum {}, checksum {}", total, check);
}
