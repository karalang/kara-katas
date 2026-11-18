// LeetCode #1603: Design Parking System -- the bench in Rust, mirroring
// parking.kara: the spaces left of each size in a `Vec`.

struct ParkingSystem {
    left: Vec<i32>,
}

impl ParkingSystem {
    fn new(big: i32, medium: i32, small: i32) -> Self {
        ParkingSystem { left: vec![big, medium, small] }
    }

    fn add_car(&mut self, car_type: i32) -> bool {
        let slot = (car_type - 1) as usize;
        if self.left[slot] == 0 {
            return false;
        }
        self.left[slot] -= 1;
        true
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1603;
    let mut lots = Vec::new();
    for _ in 0..1000 {
        let big = (next_random(&mut seed) % 3001) as i32;
        let medium = (next_random(&mut seed) % 3001) as i32;
        let small = (next_random(&mut seed) % 3001) as i32;
        lots.push((big, medium, small));
    }
    let cars: Vec<i32> = (0..10000000).map(|_| (next_random(&mut seed) % 3 + 1) as i32).collect();
    let mut check = 0;
    let mut parked = 0;
    for round in 0..20 {
        for (k, &(big, medium, small)) in lots.iter().enumerate() {
            let mut lot = ParkingSystem::new(big, medium, small);
            let mut count = 0;
            for c in cars[k * 10000..(k + 1) * 10000].iter() {
                if lot.add_car(*c) {
                    count += 1;
                }
            }
            parked += count;
            check = mix(check, count + round);
        }
    }
    println!("20 rounds of 1000 lots of up to 3000 spaces a size, 10000 cars each: {} parked, checksum {}", parked, check);
}
