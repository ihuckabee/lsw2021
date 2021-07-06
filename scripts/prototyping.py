# Test reading in line lists, EQW and SPEC files to match line pairs
import re
from dataclasses import dataclass
import shlex
import fortranformat as ff
import numpy as np


@dataclass
class Line:
  # A spectral line object
  # Note that all attribute are strings because of formatted output and to
  # prevent rounding errors (i.e. preserve I/O decimal places)
  # TODO: Use correct types for each input and rely on fortranformat to perform
  # formatted I/O
  wavelength: str
  excitation_energy: str
  oscillator_strength: str
  F_dampening: str
  R_jupper: str  # 2R_jupper + 1
  gamma_radiation: str
  lower_level: str
  upper_level: str

  # TODO: Add better placeholder treatment!
  placeholder_ew: str
  place_holder_abu: str

  transition: str

  def __str__(self) -> str:
    # Line -> string as expected in a TS line list
    # Fixed width fortran format
    # TODO: Fix output format to be proper fixed-width!
    output_format = r"(F10.3,1X,2(F6.3,1X),F8.3,1X,F6.1,1X,1PE8.2,2(1X,A3),1X,2(0PF6.1,1X),A)"
    record_writer = ff.FortranRecordWriter(output_format)
    output_str = record_writer.write(
        [float(self.wavelength), float(self.excitation_energy),
         float(self.oscillator_strength),
         float(self.F_dampening), float(self.R_jupper),
         float(self.gamma_radiation),
         f"'{self.lower_level}'",
         f"'{self.upper_level}'",
         float(self.placeholder_ew),
         float(self.place_holder_abu), f"'{self.transition}'"]
    )

    return output_str


def parse_line(line: str):
  # Given a line in the TS line list format, parse it and return a Line object
  args = shlex.split(line)
  return Line(*args)


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
    header = ""
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
        header = text
        key = f"({mass})"
        continue
      elif element_info_header_pattern.match(text):
        # Element info header
        element_ion = text.replace("'", "").strip()
        header += text
        key = f"{element_ion} {key}"
        continue
      else:
        # Read 'num_lines' lines
        # print(key, num_lines)
        lines = []
        lines.append(header)
        lines.append(parse_line(text))
        for i in range(num_lines - 1):  # first line was already read
          line = parse_line(infile.readline().rstrip())
          lines.append(line)

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
    print(value[1])
    # print('\n'.join([f"\t{v}\n" for v in value]))
