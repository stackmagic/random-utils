import shutil
import sys

def parse_log_summary(lines):
    data = {}
    for line in lines:
        try:
            count, angle = line.strip().split()
            count = int(count)
            angle = float(angle.strip('°+'))
            data[angle] = count
        except ValueError:
            continue
    return data

def fill_missing_temps(data):
    if not data:
        return []
    # Find min and max temperatures
    min_temp = min(data.keys())
    max_temp = max(data.keys())
    # Create continuous data from min to max with 1.0° steps
    continuous_data = []
    temp = min_temp
    while temp <= max_temp:
        count = data.get(temp, 0)
        continuous_data.append((temp, count))
        temp = round(temp + 1.0, 1)  # Increment by 1.0°
    return continuous_data

def draw_histogram(data):
    # Get terminal width
    terminal_width = shutil.get_terminal_size().columns
    # Reserve space for labels and padding
    max_label_width = 10  # For "XXX.XX°: " and counts
    max_count_width = max(len(str(count)) for _, count in data) + 2 if data else 2
    chart_width = terminal_width - max_label_width - max_count_width - 2

    if chart_width < 10:
        print("Terminal too narrow to display chart")
        return

    # Find max count for scaling
    max_count = max(count for _, count in data) if data else 0
    if max_count == 0:
        print("No data to display")
        return

    # Draw histogram
    for angle, count in data:
        # Scale bar length
        bar_length = int((count / max_count) * chart_width) if max_count > 0 else 0
        bar = '█' * bar_length
        # Format label
        label = f"{angle:>5.1f}°"
        # Format count
        count_str = f"({count})"
        # Print row
        print(f"{label}: {count_str:>{max_count_width}} {bar:<{chart_width}}")

def main():
    # Read input from stdin or file
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            lines = f.readlines()
    else:
        lines = sys.stdin.readlines()

    data = parse_log_summary(lines)
    continuous_data = fill_missing_temps(data)
    if continuous_data:
        draw_histogram(continuous_data)
    else:
        print("No valid data found")

if __name__ == "__main__":
    main()

