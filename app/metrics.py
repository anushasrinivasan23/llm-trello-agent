def calculate_accuracy(total_lines, valid_tasks):
    if total_lines == 0:
        return 0.0
    return round((valid_tasks / total_lines) * 100, 2)

