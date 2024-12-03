import re


class MemoryUncorruptor:
    def __init__(self, file_path, consider_dos=False):
        self.data = self._read_file(file_path)
        self.operations = []
        self.consider_dos = consider_dos
        self.enabled = True

    @staticmethod
    def _read_file(file_path):
        with open(file_path, 'r') as f:
            return f.readlines()

    def _locate_valid_operations(self):
        for line in self.data:
            self.operations.extend(re.findall(r'((?:(mul)\((\d{1,3}),(\d{1,3})\))|(do\(\))|(don\'t\(\)))', line))

    def execute_operations(self):
        operation_sum = 0
        self._locate_valid_operations()
        for operation in self.operations:

            if not operation[0]:  # Skip empty matches
                continue
            if operation[0] == 'do()':
                self.enabled = True
            elif operation[0] == "don't()":
                if self.consider_dos:
                    self.enabled = False
            elif self.enabled:
                x = int(operation[2])
                y = int(operation[3])
                operation_sum += x * y

        return operation_sum


if __name__ == '__main__':
    mu = MemoryUncorruptor('input_d03.txt', consider_dos=False)
    result = mu.execute_operations()
    print(f"Operation sum: {result}")
