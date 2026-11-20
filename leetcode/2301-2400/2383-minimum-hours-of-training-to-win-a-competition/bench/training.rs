// LeetCode #2383: Minimum Hours of Training to Win a Competition -- the
// bench, the ★ arm in Rust: the energy trained to one above the
// opponents' sum, the experience walked through the opponents.

fn min_number_of_hours(initial_energy: i64, initial_experience: i64, energy: &[i64], experience: &[i64]) -> i64 {
    let needed = energy.iter().sum::<i64>() + 1;
    let mut hours = 0i64;
    if initial_energy < needed {
        hours = needed - initial_energy;
    }
    let mut have = initial_experience;
    for &e in experience {
        if have <= e {
            hours += e + 1 - have;
            have = e + 1;
        }
        have += e;
    }
    hours
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 1000 contests of 100 opponents, contest c's from 1 to 1 + c % 100;
    // pass p starts contest c with (p + c) % 50 more energy and
    // (3 p + c) % 50 more experience than its own start
    let mut seed = 2383i64;
    let mut energies: Vec<Vec<i64>> = Vec::new();
    let mut experiences: Vec<Vec<i64>> = Vec::new();
    let mut starts: Vec<(i64, i64)> = Vec::new();
    for c in 0..1000i64 {
        let top = 1 + c % 100;
        let ie = 1 + next_random(&mut seed) % 100;
        let ix = 1 + next_random(&mut seed) % 100;
        starts.push((ie, ix));
        energies.push((0..100).map(|_| 1 + next_random(&mut seed) % top).collect());
        experiences.push((0..100).map(|_| 1 + next_random(&mut seed) % top).collect());
    }
    let mut check = 0i64;
    for p in 0..5000i64 {
        for c in 0..1000i64 {
            let (ie, ix) = starts[c as usize];
            let hours = min_number_of_hours(
                ie + (p + c) % 50,
                ix + (3 * p + c) % 50,
                &energies[c as usize],
                &experiences[c as usize],
            );
            check = (check * 31 + hours + p) % 1000000007;
        }
    }
    println!("5000 passes over 1000 contests of 100 opponents: checksum {}", check);
}
