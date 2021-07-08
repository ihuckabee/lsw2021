# Test reading in line lists, EQW and SPEC files to match line pairs
import re
from dataclasses import dataclass
import shlex
from typing import Dict, List
import fortranformat as ff
from itertools import permutations
from copy import copy
import pandas as pd


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

  # Info for/from header
  header: str

  def __str__(self) -> str:
    # Line -> string as expected in a TS line list
    # Fixed width fortran format
    # TODO: Fix output format to be proper fixed-width!
    output_format = r"(F10.3,2(F7.3),F9.3,1X,F6.1,1X,1PE9.2,2(1X,A3),2(0PF6.1,1X),A)"
    output_str = fortran_format_str(output_format,
                                    [float(self.wavelength),
                                     float(self.excitation_energy),
                                     float(self.oscillator_strength),
                                     float(self.F_dampening),
                                     float(self.R_jupper),
                                     float(self.gamma_radiation),
                                     f"'{self.lower_level}'",
                                     f"'{self.upper_level}'",
                                     float(self.placeholder_ew),
                                     float(self.place_holder_abu),
                                     f"'{self.transition}'"])
    return output_str


@dataclass
class LineCollection:
  # A collection of Line objects of the same element/ionisation
  # TS linelists are written in these blocks containing headers defining the
  # properties of the element/ionisation and the number of spectral lines that
  # follow the headers
  # TODO: Fix Fortran formatting of strings to correctly read in mass, etc
  # with apostrophes
  # mass: float
  # ionisation: int
  # element_ion: str
  # num_lines: int
  header_1: str  # mass, ionisation, num_lines header
  header_2: str  # element ionisation header
  lines: List[Line]

  def __str__(self) -> str:
    # Create the two headers and write out each Line in the list of lines
    # header_1_format = r"(''F8.3'',12X,3X,I1,6X,I2)"
    # header_1 = fortran_format_str(header_1_format,
    #                               [self.mass, self.ionisation, self.num_lines])
    # header_2_format = r"(A8,2X)"
    # header_2 = fortran_format_str(header_2_format, [self.element_ion])

    # print("header 1")
    # print(header_1)
    # print("header 2")
    # print(header_2)
    # output_str = f"{header_1}\n{header_2}\n"
    # for line in self.lines:
    #   output_str += f"{str(line)}\n"

    # return output_str
    output_str = f"{self.header_1}\n{self.header_2}\n"
    for line in self.lines:
      output_str += f"{str(line)}\n"

    return output_str


def parse_line(line: str, header: str):
  # Given a line in the TS line list format, parse it and return a Line object
  args = shlex.split(line)
  return Line(*args, header)


def fortran_format_str(fortran_format: str, values: List) -> str:
  # Given a format and a list of ordered values, return a fortran formatted str
  writer = ff.FortranRecordWriter(fortran_format)
  return writer.write(values)


def read_eqw_file(eqw_file: str) -> pd.DataFrame:
  # Read in equivalent-width measurement file as a DataFrame
  eqw_df = pd.read_fwf(eqw_file)
  # for data with comments
  eqw_df = eqw_df.drop(eqw_df.columns[[13, 14, 15]], axis=1)
  eqw_df = eqw_df.drop(eqw_df.columns[[6, 7, 8, 9, 10, 11, 12]], axis=1)
  eqw_df.columns = ['element', 'ion', 'wl', 'exc', 'loggf', 'eqw']

  return eqw_df
  # nonzero_eqw = ew_df[ew_df.ew > 1]


def substitute_num_lines_in_header(header: str, new_num: int) -> str:
  # Replace the numebr of lines in the header with the 'new_num' specified
  pattern = re.compile(r"\d+(\D*)$")
  return pattern.sub(str(new_num), header)


def read_line_file(line_file: str, eqw_filter_file=None, eqw_filter=1):
  # Open a valid Turbospectrum line list, read it line-by-line and return a
  # collection of all the line data
  # If 'eqw_filter_file' is provided, use the eqw_filter to remove lines that
  # have an equivalent width less than filter
  line_list = {}  # key is element/ionisation, value is list of lines
  if eqw_filter_file:
    eqw_df = read_eqw_file(eqw_filter_file)
    eqw_df.set_index('wl', inplace=True)

  # Perhaps create a LineList class to hold the data?
  # Read line-by-line
  # There are 2 lines of headers before each collection of lines, each starts
  # with an apostrophe '
  # The first starts with '\t[0-9] and contains info about the mass of the
  # element, the ionisation level, and the number of lines to expect
  # The second starts with '[aA-zZ] and contains the string identifier of the
  # element & ionisation stage
  mass_info_header_pattern = re.compile(r"^'\s+[0-9]")
  element_info_header_pattern = re.compile("^'[A-Z]")
  with open(line_file, 'r', encoding='utf-8') as infile:
    num_lines = 0  # number of lines to read under current header
    header = ""
    key = ""  # key built from headers
    count = 0
    # Read file line-by-line
    while True:
      count += 1
      # if count > 13:
      #   break
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
        output_num_lines = num_lines

        # print(key, num_lines)
        lines = []
        lines.append(header)
        lines.append(parse_line(text, header))
        for i in range(num_lines - 1):  # first line was already read
          # Check if line passes EQW filter test
          line = parse_line(infile.readline().rstrip(), header)
          if eqw_filter_file:
            if eqw_df[line.wavelength] >= eqw_filter:
              lines.append(line)
            else:
              output_num_lines -= 1
          else:
            lines.append(line)

        # Create LineCollection
        # line_collection = LineCollection(float(mass), ion, element_ion,
        #                                  num_lines, lines[1:])
        # TODO: Edit header 1 to use output_num_lines not the num_lines we
        # started with
        header_1, header_2, _ = header.split('\n')
        header_1 = substitute_num_lines_in_header(header_1, output_num_lines)

        line_collection = LineCollection(header_1, header_2, lines[1:])

        # Add to line list dictionary
        line_list[key] = line_collection

        # Reset key and num lines
        key = ""
        num_lines = 0
        continue

  return line_list


def write_line_file(line_list: Dict, output_path: str):
  # Write a dict containing the list of LineCollection objects
  with open(output_path, 'w', encoding='utf-8') as outfile:
    for line_collection in line_list.values():
      outfile.write(str(line_collection))


def write_pairs_line_list(line_list: Dict, output_path: str):
  # From a specified line list (conventionally parsed from 'read_line_file()'),
  # pair every line and create a new line list with the pairs
  # TODO: Add wavelength ranges and change the pair wavelengths
  # Generate permutations of headers + list indices (unique IDs)
  line_collection_dict = line_list.values()
  # Figure out mapping from line -> header...
  lines = [line for i, value in enumerate(line_collection_dict)
           for line in value.lines]
  pairs = permutations(lines, 2)
  # print(len(lines))
  # print(len(list(pairs)))

  # Edit wavelengths
  start_wavelength = 3000  # angstroms
  max_wavelength = 10000  # angstroms
  wavelength_step = 5  # between each line
  current_wavelength = start_wavelength

  output_lines = []
  for pair in pairs:
    for line in pair:
      new_line = copy(line)
      new_line.wavelength = current_wavelength

      output_lines.append(new_line)
      current_wavelength += wavelength_step
    if current_wavelength > max_wavelength:
      break

  print("Done changing wavelengths")
  # Create line collections
  # If lines have the same header, they are part of the same collection
  line_collection_dict = {}  # key: header, value: list of valid lines
  for line in output_lines:
    key = line.header
    if not key in line_collection_dict:
      line_collection_dict[key] = [line]
    else:
      line_collection_dict[key].append(line)

  print("Done creating line collection dictionary")

  line_collections = []
  # Create LineCollection for each key
  for key, lines in line_collection_dict.items():
    # Change num lines in header_1
    header_1, header_2, _ = key.split('\n')
    header_1 = substitute_num_lines_in_header(header_1, len(lines))

    line_collection = LineCollection(header_1, header_2, lines)
    line_collections.append(line_collection)

  print("Done creating line collections list")

  with open(output_path, 'w', encoding='utf-8') as outfile:
    for line_collection in line_collections:
      outfile.write(f"{str(line_collection)}")

  print("Done writing file")
  exit()


if __name__ == "__main__":
  res_dir = "../res"
  out_dir = "../out"
  identifier = "vald-6700-6720"
  line_file = f"{res_dir}/{identifier}.list"
  spec_file = f"{res_dir}/{identifier}.spec"
  eqw_file = f"{res_dir}/{identifier}.eqw"

  line_list = read_line_file(line_file)
  # for key, value in line_list.items():
  # print(key)
  # print(value)
  # print('\n'.join([f"\t{v}\n" for v in value]))

  output_file = f"{out_dir}/test.list"
  write_pairs_line_list(line_list, output_file)

  write_line_file(line_list, output_file)
