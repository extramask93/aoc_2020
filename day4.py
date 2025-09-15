from pathlib import Path
from typing import Dict
import re
#128<answer<138
def load_input(path: Path):
    with open(path,"r") as file:
        passport_string = []
        for line in file:
            passport_string.append(line)
            if line.isspace():
                yield "".join(passport_string)
                passport_string.clear()
        yield "".join(passport_string)
def fail_printer_decorator(func):
    return func
@fail_printer_decorator
def hgt_validator(s: str):
    match = re.fullmatch(r"(\d+)(cm|in)",s)
    if not match:
        return False
    value, unit = match.groups()
    return 150<=int(value)<=193 if unit == "cm" else  59<=int(value)<=76
@fail_printer_decorator
def byr_validator(s: str):
    return 1920<=int(s)<=2002
@fail_printer_decorator
def iyr_validator(s: str):
    return  2010<=int(s)<=2020
@fail_printer_decorator
def eyr_validator(s: str):
    return  2020<=int(s)<=2030
@fail_printer_decorator
def hcl_validator(s: str):
    return re.fullmatch(r"#[0-9a-f]{6}",s)
@fail_printer_decorator
def ecl_validator(s: str):
    return  re.fullmatch(r"amb|blu|brn|gry|grn|hzl|oth",s)
@fail_printer_decorator
def pid_validator(s: str):
    return  re.fullmatch(r"\d{9}",s)
class Passport:
    def __init__(self):
        self.fields: Dict[str,str] = {} 
        self.fields_and_validators = {
            "byr": byr_validator,
            "iyr": iyr_validator,
            "eyr": eyr_validator,
            "hgt": hgt_validator,
            "hcl": hcl_validator,
            "ecl": ecl_validator,
            "pid": pid_validator
            }
    @classmethod
    def from_string(cls, s: str) -> "Passport":
        result = cls()
        fields = re.split(r"\s+", s.strip()) 
        fields = [field.split(":") for field in fields]
        result.fields = dict(fields)
        return result
    def is_valid_first_part(self):
        return all(field in self.fields for field in self.fields_and_validators)
    def is_valid_second_part(self):
        return all( (field in self.fields and
                     validator(self.fields[field]))
                     for field,validator in self.fields_and_validators.items())

if __name__ == "__main__":
    passports = [Passport.from_string(s) for s in load_input(Path("inputs/day4.txt"))]
    nr_of_valid_passports = sum([passport.is_valid_first_part() for passport in passports])
    print(f"Answer to the first part: {nr_of_valid_passports}")
    nr_of_valid_passports = sum([passport.is_valid_second_part() for passport in passports])
    print(f"Answer to the second part: {nr_of_valid_passports}")


        
