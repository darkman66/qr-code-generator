# QR Badge

Generate a PNG badge with a QR code and a customizable call-to-action label.

## Requirements

- Python 3.15 or later
- [uv](https://docs.astral.sh/uv/)

## Install

Clone the repository, move into the project directory, and install its dependencies:

```sh
uv sync
```

## Usage

Run the command with the URL to encode:

```sh
uv run qr-badge https://example.com
```

This writes `qr_badge.png` in the current directory. Pass a label and output path to customize it:

```sh
uv run qr-badge https://example.com "VISIT OUR SITE" --output event-badge.png
```

The label is optional and defaults to `SCAN ME`. The output path can be provided with `-o` or `--output` and defaults to `qr_badge.png`.

To see all command-line options:

```sh
uv run qr-badge --help
```