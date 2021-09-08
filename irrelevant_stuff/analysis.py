import re
import sys
from statistics import mean, median


def main(file_name_r: str, file_name_w: str, name_data: str):
    read_file = open(file_name_r, "r")
    content = read_file.read()
    write_file = open(file_name_w, "a")

    numbers = []
    pattern = re.compile(r"time:  (\d+\.\d+)")
    for match in pattern.finditer(content):
        number = float(match.group(1))
        numbers.append(number)

    sets = []
    pattern = re.compile(r"set1= (.*)\n")
    for match in pattern.finditer(content):
        set1 = match.group(1)
        sets.append(set1)

    # ----------------------------------
    print(name_data)

    write_file.write(f"    {name_data}_ratio = [")
    for i in range(0, len(numbers), 2):
        if (name_data[-1] == '1') and (i % 10 == 8 or i % 10 == 9):  # ignore EF for smallest sets
            continue
        ratio = numbers[i] / numbers[i + 1]
        write_file.write(f"{ratio:13.8f},")
        print(f"{ratio:13.8f}", end=",")
    write_file.write("]\n")
    print()

    write_file.write(f"    {name_data}_non   = [")
    for idx, n in enumerate(numbers[0::2]):
        if (name_data[-1] == '1') and (idx % 10 == 8 or idx % 10 == 9):  # ignore EF for smallest sets
            continue
        write_file.write(f"{n:13.8f},")
        print(f"{n:13.8f}", end=",")
    write_file.write("]\n")
    print()

    write_file.write(f"    {name_data}_opt   = [")
    for idx, n in enumerate(numbers[1::2]):
        if (name_data[-1] == '1') and (idx % 10 == 8 or idx % 10 == 9):  # ignore EF for smallest sets
            continue
        write_file.write(f"{n:13.8f},")
        print(f"{n:13.8f}", end=",")
    write_file.write("]\n")
    write_file.write(f"    {name_data} = [{name_data}_ratio, {name_data}_non, {name_data}_opt]\n\n")
    print("\n")

# ----------------------

    """
    print(name_data)
    ratios = []
    for i in range(0, len(numbers), 2):
        ratio = numbers[i] / numbers[i + 1]
        ratios.append(ratio)

        write_file.write(f"{ratio:15.8f}        | non-opt: {numbers[i]:>13.8f}        | set: {sets[i]}\n")
        print(f"{ratio:15.8f}        | non-opt: {numbers[i]:>13.8f}        | set: {sets[i]}")

    print()
    write_file.write("\n")

    print(f"{mean(ratios):>15.8f}  -  mean of ratios")
    write_file.write(f"{mean(ratios):>15.8f}  -  mean of ratios\n")
    print(f"{median(ratios):>15.8f}  -  median of ratios")
    write_file.write(f"{median(ratios):>15.8f}  -  median of ratios\n")

    print(f"{sum(numbers[0::2]):>15.8f}  -  total time non-opt")
    write_file.write(f"{sum(numbers[0::2]):>15.8f}  -  total time non-opt\n")
    print(f"{sum(numbers[1::2]):>15.8f}  -  total time opt")
    write_file.write(f"{sum(numbers[1::2]):>15.8f}  -  total time opt\n")
    print()
    """

    read_file.close()
    write_file.close()


if __name__ == '__main__':
    # use the CLI argument if provided, or else use predefined file
    if len(sys.argv) > 1:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        names1 = ["binder1", "binder2", "binder3", "binder4", "binder7",
                  "jump1", "jump2", "jump3", "jump4", "jump7",
                  "exist1", "exist2", "exist3", "exist4", "exist7"]
        names2 = ["union_one1", "union_one2", "union_one3", "union_one4", "union_one7",
                  "union_both1", "union_both2", "union_both3", "union_both4", "union_both7"]
        names1_v2 = ["binder2_v2", "binder3_v2", "binder4_v2", "binder5_v2", "binder6_v2", "binder7_v2",
                     "jump2_v2", "jump3_v2", "jump4_v2", "jump5_v2", "jump6_v2", "jump7_v2",
                     "exist2_v2", "exist3_v2", "exist4_v2", "exist5_v2", "exist6_v2",  "exist7_v2"]

        for name in names1_v2:
            # main(f"results\\{name}.txt", f"analysed_results\\{name}_stats.txt")
            main(f"results\\{name}.txt", f"analysed_results\\all_stats1_v2.txt", name)
