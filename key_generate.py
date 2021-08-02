import random
import datetime as dt
import calendar
import base64


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return dt.datetime(year, month, day)


SCORE = 1523
CHECK_DIGIT_POINTS = 4
CHUNKS_LEN = 4


class License:
    def __init__(self, key=''):
        if key == '':
            license, due_day = self.generate()
            self.key = {"license": license,
                        "license_due_day": due_day.strftime("%Y/%m/%d %H:%M:%S")}
        else:
            self.key = key.lower()

    def verify_license(self, license):
        score = 0
        check_digit = license[0]
        check_digit_count = 0
        chunks = license.split('-')
        for chunk in chunks:
            if len(chunk) != CHUNKS_LEN:
                return False
            for char in chunk:
                if char == check_digit:
                    check_digit_count += 1
                score += ord(char)
        # print("score", score, "check_digit_count", check_digit_count)
        if score == SCORE and check_digit_count == CHECK_DIGIT_POINTS:
            # print("::: License code (%s) is Valid" % license)
            return True
        return False

    def verify_due_day(self, due_day):
        try:
            if due_day < dt.datetime.now():
                return False
            else:
                # print("::: Due day: %s" % due_day)
                return True
        except:
            return False

    def generate(self):
        due_day = add_months(dt.datetime.today(), 6)
        license = ''
        chunk = ''
        alphabet = 'abcdefghijklmnopqrstuvwxyz1234567890'
        while True:
            while len(license) < CHUNKS_LEN*(CHECK_DIGIT_POINTS+1):
                char = random.choice(alphabet)
                license += char
                chunk += char
                if len(chunk) == CHUNKS_LEN:
                    license += '-'
                    chunk = ''
            license = license[:-1]
            if self.verify_license(license) and self.verify_due_day(due_day):
                return license, due_day
            else:
                license = ''

    def encode(self):
        duecode = base64.b64encode(
            self.key["license_due_day"].encode("utf-8"))
        # durecode: b'MjAyMi8wMi8wMiAwMDowMDowMA==' -> MjAyMi8wMi8wMiAwMDowMDowMA==
        return "%s##%s" % (self.key["license"], str(duecode)[2:-1])

    def output(self):
        print("::: License code: %s, \n::: Due Day: %s" %
              (self.key["license"], self.key["license_due_day"]))
        print("::: License for SAE PlotTool ----> \n")
        print("\t%s" % self.encode())
        print("\n------------------------------------------------------")


def main():
    run = True
    while run:
        print("Generate a new license for SAE PlotTool? (y/n)")
        ans = input()
        if ans in ['y', 'Y', 'yes']:
            license = License()
            license.output()
        else:
            run = False


if __name__ == '__main__':
    main()
