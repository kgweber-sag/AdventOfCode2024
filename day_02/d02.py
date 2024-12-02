class SafeCheck():
    def __init__(self, file_path):
        self.read_file(file_path)
        self.safe_report_count = 0
        self.dampened_report_count = 0

    def read_file(self, file_path):
        with open(file_path, 'r') as f:
            self.data = [[int(x) for x in line.strip().split(' ')] for line in f]

    def safety_check(self, report):
        ascending = report[0] < report[1]
        for i in range(len(report) - 1):
            if abs(report[i] - report[i + 1]) > 3 or report[i] == report[i + 1]:
                return False
            if (report[i] > report[i + 1] and ascending) or (report[i] < report[i + 1] and not ascending):
                return False
        return True

    def score_safety_check(self):
        for line in self.data:
            if self.safety_check(line):
                self.safe_report_count += 1
        return self.safe_report_count

    def problem_dampened_safety_check(self):
        for index, line in enumerate(self.data):
            if self.safety_check(line):
                self.dampened_report_count += 1
                continue
            for i in range(len(line)):
                test_line = line[:i] + line[i+1:]
                if self.safety_check(test_line):
                    self.dampened_report_count += 1
                    break

        return self.dampened_report_count

if __name__ == '__main__':
    sc = SafeCheck('input_d02.txt')
    print(sc.score_safety_check())
    print(sc.problem_dampened_safety_check())