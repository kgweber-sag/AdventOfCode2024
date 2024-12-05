from collections import defaultdict

class PrinterSorter:
    def __init__(self, file_path: str):
        """Initialize PrinterSorter with input file path."""
        self.rules = dict()
        self.updates = []
        self.correct_middle_sum = 0
        self.incorrect_middle_sum = 0
        self._read_data(file_path)
        self.dependency_graph = self.build_dependency_graph()

    def _read_data(self, file_path: str) -> None:
        """Read and parse input file into list of tuples."""
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()

        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: {file_path}")

        except Exception as e:
            raise RuntimeError(f"Error reading input file: {str(e)}")

        for line in lines:
            if '|' in line:
                before_page, after_page = map(int, line.strip().split('|'))
                # add a new dictionary entry [before_page] = [after_page] if necessary, otherwise add after_page to the existing list
                self.rules[before_page] = self.rules.get(before_page, []) + [after_page]
            if ',' in line:
                self.updates.append([int(x) for x in line.strip().split(',')])

    def build_dependency_graph(self):
        graph = defaultdict(list)
        for before_page, after_page in self.rules.items():
            for page in after_page:
                graph[before_page].append(page)
        return graph

    def check_update(self, update):
        for index, page in enumerate(update):
             before = set(update[:index])
             if before.intersection(self.rules.get(page, [])):
                 return False
        return True

    @staticmethod
    def get_middle_item(update):
        return update[len(update) // 2]

    def visit(self, node, path=None):
        if path is None:
            path = set()

        if node in path:
            return  # Skip if cyclic

        if node in self.checked:
            return

        path.add(node)
        self.checked.add(node)

        # Must process nodes that should come *after* the current node
        for required_after in self.rules.get(node, []):
            if required_after in self.update_set:
                self.visit(required_after, path)

        path.remove(node)
        self.order.append(node)

    def correct_update(self, update):
        self.checked = set()
        self.order = []
        self.update_set = set(update)

        for page in update:
            if page not in self.checked:
                self.visit(page)

        return [x for x in self.order if x in update][::-1]

    def check_all_updates(self):

        for update in self.updates:
            if not self.check_update(update):
                corrected_update = self.correct_update(update)
                self.incorrect_middle_sum += self.get_middle_item(corrected_update)
                if not self.check_update(corrected_update):
                    print("Failed to correct update:", update)
                    print("Corrected update:", corrected_update)
            else:
                self.correct_middle_sum += self.get_middle_item(update)



if __name__ == '__main__':
    ps = PrinterSorter('input_d05.txt')
    ps.check_all_updates()
    print("Correct middle sum:", ps.correct_middle_sum)
    print("Corrected middle sum:", ps.incorrect_middle_sum)