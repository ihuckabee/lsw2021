# Test reading in line lists, EQW and SPEC files to match line pairs
import re


def read_line_file(line_file: str):
  # Open a valid Turbospectrum line list, read it line-by-line and return a
  # collection of all the line data
  line_list = {}  # key is element/ionisation, value is list of lines

  # Perhaps create a LineList class to hold the data?
  # Read line-by-line
  # There are 2 lines of headers before each collection of lines, each starts
  # with an apostrophe '
  # The first starts with '\t[0-9] and contains info about the mass of the
  # element, the ionisation level, and the number of lines to expect
  # The second starts with '[aA-zZ] and contains the string identifier of the
  # element & ionisation stage
  mass_info_header_pattern = re.compile("^'   [0-9]")
  element_info_header_pattern = re.compile("^'[A-Z]")
  with open(line_file, 'r', encoding='utf-8') as infile:
    num_lines = 0  # number of lines to read under current header
    key = ""  # key built from headers
    count = 0
    # Read file line-by-line
    while True:
      count += 1
      if count > 13:
        break
      text = infile.readline()
      if not text:
        break
      if mass_info_header_pattern.match(text):
        # Mass info header
        pattern_match = re.findall(r"([\d.]+)\s+(\S+)", text)
        mass, ion, num_lines = pattern_match[0][0], \
            int(pattern_match[1][0]), int(pattern_match[1][1])

        key = f"({mass})"
        continue
      elif element_info_header_pattern.match(text):
        # Element info header
        element_ion = text.replace("'", "").strip()
        key = f"{element_ion} {key}"
        continue
      else:
        # Read 'num_lines' lines
        # print(key, num_lines)
        lines = []
        lines.append(text)
        for i in range(num_lines - 1):  # first line was already read
          lines.append(infile.readline().rstrip())

        # Add to line list dictionary
        line_list[key] = lines

        # Reset key and num lines
        key = ""
        num_lines = 0
        continue

  return line_list


if __name__ == "__main__":
  res_dir = "../res"
  identifier = "vald-6700-6720"
  line_file = f"{res_dir}/{identifier}.list"
  spec_file = f"{res_dir}/{identifier}.spec"
  eqw_file = f"{res_dir}/{identifier}.eqw"

  line_list = read_line_file(line_file)
  for key, value in line_list.items():
    print(f"{key}: {len(value)} lines")
    print('\n'.join([f"\t{v}\n" for v in value]))
