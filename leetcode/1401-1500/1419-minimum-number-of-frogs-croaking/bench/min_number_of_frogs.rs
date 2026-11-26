fn min_number_of_frogs(croak_of_frogs: &str) -> i32 {
    let mut heard = [0i32; 5];
    let mut most: i32 = 0;
    for c in croak_of_frogs.chars() {
        let i = match c {
            'c' => 0,
            'r' => 1,
            'o' => 2,
            'a' => 3,
            'k' => 4,
            _ => return -1,
        };
        heard[i] += 1;
        if i > 0 && heard[i] > heard[i - 1] {
            return -1;
        }
        most = most.max(heard[0] - heard[4]);
    }
    if heard[0] == heard[4] { most } else { -1 }
}

fn main() {
    let mut seed: i64 = 1419;
    let word: Vec<char> = "croak".chars().collect();
    let mut pool = String::new();
    for _ in 0..1000 {
        let mut croaking: Vec<usize> = Vec::new();
        let mut started = 0;
        while started < 100 || !croaking.is_empty() {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let r = seed / 65536;
            if started < 100 && (croaking.is_empty() || r % 3 == 0) {
                pool.push('c');
                croaking.push(1);
                started += 1;
            } else {
                let i = (r / 3) as usize % croaking.len();
                pool.push(word[croaking[i]]);
                croaking[i] += 1;
                if croaking[i] == 5 {
                    croaking.swap_remove(i);
                }
            }
        }
    }
    let mut check: i64 = 0;
    for _ in 0..500 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let start = (500 * (seed / 65536 % 801)) as usize;
        check = (check * 131 + min_number_of_frogs(&pool[start..start + 100000]) as i64 + 1) % 1000000007;
    }
    println!("500 windows of 10^5 letters: checksum {}", check);
}
