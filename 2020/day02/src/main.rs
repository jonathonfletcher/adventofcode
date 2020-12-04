use std::fs::File;
use std::io::{self, BufRead};
use regex::Regex;

fn main() {
    let re = Regex::new(r"^(\d+)\-(\d+)\s+(\w+):\s*(\w+)$").unwrap();

    let file = match File::open("input.txt") {
        Ok(file) => file,
        Err(error) => panic!("{}", error)
    };

    let mut n_valid_p1 = 0;    
    let mut n_valid_p2 = 0;    
    for line in io::BufReader::new(file).lines() {
        if let Ok(line) = line {
            for cap in re.captures_iter(&line) {
                let c_min = cap[1].parse::<i32>().unwrap();
                let c_max = cap[2].parse::<i32>().unwrap();
                let c_char = &cap[3].chars().next().unwrap();
                let c_passwd = &cap[4];

                // Part 01 - use the c_min / c_max 
                let mut c_cnt = 0;
                for c in c_passwd.chars() {
                    if c == *c_char {
                        c_cnt += 1;
                    }
                }
                if c_cnt >= c_min && c_cnt <= c_max {
                    n_valid_p1 += 1;
                }

                // Part 02 - use c_min / c_max as indexes
                let mut c_cnt = 0;
                let c_passwd_len = &c_passwd.len();
                let v = vec![c_min as usize, c_max as usize];
                for idx in v.iter() {
                    if idx <= c_passwd_len {
                        let c = c_passwd.chars().nth(idx-1).unwrap();
                        if c == *c_char {
                            c_cnt += 1;
                        }
                    }
                }
                if c_cnt == 1 {
                    n_valid_p2 += 1;
                }

            }
        }
    }
    println!("n_valid_p1={:?}", n_valid_p1);
    println!("n_valid_p2={:?}", n_valid_p2);
}
