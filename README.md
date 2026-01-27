# maqamat

A tool for generating musical scale data from maqamat (Arabic musical scales) defined in a YAML configuration file. Produces TSV interval tables, SVG bracelet diagrams, and Scala (.scl) tuning files.

## Prerequisites

- Python 3
- [Task](https://taskfile.dev/) (go-task runner)
- [yq](https://github.com/mikefarah/yq) (for listing maqamat)

## Setup

```bash
task install
```

## Usage

List all available maqamat:

```bash
task list:maqamat
```

Generate all output files for every maqam defined in `maqamat.yml`:

```bash
task generate:all
```

Generate output for a specific maqam:

```bash
task generate:maqam MAQAM=urmawi
```

Show all available tasks:

```bash
task
```

### Direct script usage

```bash
./maqamat.py --generate-scl --maqamat-file maqamat.yml
./maqamat.py --generate-scl --maqamat-file maqamat.yml --maqam 53-tet --verbose
```

Run without arguments to see all options:

```bash
./maqamat.py
```

## Output

Output is written to `results/<by>/<maqam>/` where `<by>` is the scale type (`tet` or `ratios`) and `<maqam>` is the maqam name from the YAML file. Each maqam produces:

- `<maqam>.tsv` -- interval table with cents, frequency ratios, derived ratios, and errors
- `<maqam>.svg` -- SVG bracelet diagram
- `<maqam>.scl` -- Scala tuning file (when `--generate-scl` is used)

## Defining maqamat

Scales are defined in `maqamat.yml`. Each entry specifies a `metadata.by` field (`tet` or `ratios`) and an `intervals` array:

```yaml
maqamat:
  12-tet:
    enabled: true
    metadata:
      by: "tet"
      comment: "N-tone equal temperament"
    name: tet
    number_of_intervals: 12
    intervals: []

  urmawi:
    metadata:
      by: "ratios"
      source: "mikosch2022"
      page: 31
      comment: "intervals of Safi al-Din al-Urmawi's enharmonic scale"
    name: urmawi
    intervals:
      [1, 256/243, 65536/59049, 9/8, 32/27, 8192/6561, 81/64, 4/3, 1024/729, 262144/177147, 3/2, 128/81, 32768/19683, 27/16, 16/9, 4096/2187, 1048576/531441, 2]
```

## References

- [53 equal temperament](https://en.wikipedia.org/wiki/53_equal_temperament)
- [Scala .scl file format](https://www.huygens-fokker.org/scala/scl_format.html)
- Mikosch, Thomas. *Oriental Jazz Improvisation - Microtonality and Harmony*. Tredition, 2022.
