// Benchmark for #359 -- mirror of logger.kara.
use std::collections::HashMap;

struct Logger {
    next_ok: HashMap<String, i64>,
}

impl Logger {
    fn should_print_message(&mut self, timestamp: i64, message: String) -> bool {
        if let Some(&t) = self.next_ok.get(&message) {
            if timestamp < t {
                return false;
            }
        }
        self.next_ok.insert(message, timestamp + 10);
        true
    }
}

fn main() {
    let mut seed: i64 = 359;
    let mut logger = Logger { next_ok: HashMap::new() };
    let mut t: i64 = 0;
    let mut printed = 0;
    let mut checksum: i64 = 0;
    for _ in 0..1000000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        t += if (seed / 65536) % 8 == 0 { 1 } else { 0 };
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let id = (seed / 65536) % 100;
        let ok = logger.should_print_message(t, format!("msg{}", id));
        if ok {
            printed += 1;
        }
        checksum = (checksum * 3 + if ok { 1 } else { 2 }) % 1000000007;
    }
    println!("{} of 1000000 calls printed, checksum {}", printed, checksum);
}
