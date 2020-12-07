#[macro_use] extern crate lazy_static;
use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead};
use std::vec::Vec;
use regex::Regex;

fn is_valid(entry: &HashMap<String, String>) -> bool
{
    let required_fields = vec!["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"];
    let mut entry_valid = true;
    for field in required_fields.iter() {
        let value = match entry.get(*field) {
            Some(value) => { value },
            None => {
                entry_valid = false;
                break;
            }
        };
        let value_valid = match *field {
            "byr" => {
                lazy_static! {
                    static ref BYR_RE: Regex = Regex::new(r"^(\d{4})$").unwrap();                
                }
                let rval = match BYR_RE.captures(value) {
                    Some(cap) => {
                        let v = cap[1].parse::<i32>().unwrap();
                        cap.len() == 2 && v >= 1902 && v <= 2002
                    },
                    None => { false }
                };
                rval
            },
            "iyr" => {
                lazy_static! {
                    static ref IYR_RE: Regex = Regex::new(r"^(\d{4})$").unwrap();                
                }
                let rval = match IYR_RE.captures(value) {
                    Some(cap) => {
                        let v = cap[1].parse::<i32>().unwrap();
                        cap.len() == 2 && v >= 2010 && v <= 2020
                    },
                    None => { false }
                };
                rval
            },
            "eyr" => {
                lazy_static! {
                    static ref EYR_RE: Regex = Regex::new(r"^(\d{4})$").unwrap();
                }
                let rval = match EYR_RE.captures(value) {
                    Some(cap) => {
                        let v = cap[1].parse::<i32>().unwrap();
                        cap.len() == 2 && v >= 2020 && v <= 2030
                    },
                    None => { false }
                };
                rval
            },
            "hgt" => {
                lazy_static! {
                    static ref HGT_RE: Regex = Regex::new(r"^(\d+)(cm|in)$").unwrap();
                }
                let rval = match HGT_RE.captures(value) {
                    Some(cap) => {
                        let v = cap[1].parse::<i32>().unwrap();
                        let scale = &cap[2];
                        if scale == "cm" {
                            cap.len() == 3 && v >= 150 && v <= 193
                        } else if scale == "in" {
                            cap.len() == 3 && v >= 59 && v <= 76
                        } else {
                            false
                        }
                    },
                    None => { false }
                };
                rval
            },
            "hcl" => {
                lazy_static! {
                    static ref HCL_RE: Regex = Regex::new(r"^(\#[0-9a-f]{6})$").unwrap();
                }
                let rval = match HCL_RE.captures(value) {
                    Some(cap) => {
                        cap.len() == 2
                    },
                    None => { false }
                };
                rval
            },
            "ecl" => {
                let valid_values = vec!["amb", "blu", "brn", "gry", "grn", "hzl", "oth"];
                let mut rval : bool = false;
                for vv in valid_values.iter() {
                    if vv == value {
                        rval = true;
                        break
                    }
                }
                rval
            },
            "pid" => {
                lazy_static! {
                    static ref PID_RE: Regex = Regex::new(r"^([0-9]{9})$").unwrap();
                }
                let rval = match PID_RE.captures(value) {
                    Some(cap) => {
                        cap.len() == 2
                    },
                    None => { false }
                };
                rval
            },
            "cid" => {
                panic!("{}", field);
            }
            _ => {
                panic!("{}", field);
            }
        };
        if !value_valid {
            println!("invalid {:?}", entry);
            println!("invalid {:?}: {:?}", *field, value);
        }
        entry_valid &= value_valid;
    }
    entry_valid
}

fn main() {

    let file = match File::open("input.txt") {
        Ok(file) => file,
        Err(error) => panic!("{}", error)
    };

    let mut count_valid = 0;
    let mut entry = HashMap::new();
    for line in io::BufReader::new(file).lines() {
        if let Ok(line) = line {
            if line.len() > 0 {
                let tuples: Vec<&str> = line.split_ascii_whitespace().collect();
                for t in tuples {
                    let kv: Vec<&str> = t.split(':').collect();
                    entry.insert(String::from(kv[0]), String::from(kv[1]));
                }
            } else {
                if is_valid(&entry) {
                    count_valid += 1;
                }
                entry.clear();
            }
        }
    }
    if !entry.is_empty() {
        if is_valid(&entry) {
            count_valid += 1;
        }
    }
    println!("count_valid={}", count_valid);
}
