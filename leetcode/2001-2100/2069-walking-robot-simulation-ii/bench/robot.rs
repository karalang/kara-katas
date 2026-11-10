// LeetCode #2069: Walking Robot Simulation II -- Rust mirror of the ★
// arm's benchmark (robot.kara): 200 robots of 2 to 100 by 2 to 100, 50000
// calls each, half of them steps of up to 100000 cells.

struct Robot {
    width: i64,
    height: i64,
    at: i64,
    moved: bool,
}

impl Robot {
    fn new(width: i64, height: i64) -> Robot {
        Robot { width, height, at: 0, moved: false }
    }

    fn step(&mut self, num: i64) {
        self.moved = true;
        self.at = (self.at + num) % (2 * (self.width + self.height) - 4);
    }

    fn get_pos(&self) -> Vec<i64> {
        let (w, h, at) = (self.width - 1, self.height - 1, self.at);
        if at <= w {
            vec![at, 0]
        } else if at <= w + h {
            vec![w, at - w]
        } else if at <= 2 * w + h {
            vec![2 * w + h - at, h]
        } else {
            vec![0, 2 * w + 2 * h - at]
        }
    }

    fn get_dir(&self) -> String {
        let (w, h, at) = (self.width - 1, self.height - 1, self.at);
        let dir = if at == 0 {
            if self.moved { "South" } else { "East" }
        } else if at <= w {
            "East"
        } else if at <= w + h {
            "North"
        } else if at <= 2 * w + h {
            "West"
        } else {
            "South"
        };
        dir.to_string()
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2069;
    let mut check: i64 = 0;
    for t in 0..200 {
        let mut robot = Robot::new(2 + t % 99, 2 + t * 7 % 99);
        for _ in 0..50000 {
            let kind = next_random(&mut seed) % 4;
            if kind < 2 {
                let a = next_random(&mut seed);
                let b = next_random(&mut seed);
                robot.step((a * 32768 + b) % 100000 + 1);
            } else if kind == 2 {
                let p = robot.get_pos();
                check = (check * 31 + p[0] * 1000 + p[1]) % 1000000007;
            } else {
                check = (check * 31 + robot.get_dir().len() as i64) % 1000000007;
            }
        }
    }
    println!("200 robots, 10000000 calls: checksum {}", check);
}
