#!/usr/bin/env python3
"""Regenerates the synthetic .passthm fixtures used by test_backend_passthm.py.

These stand in for two real themes the test suite was originally written
against (MinePass_Nightly.passthm and тцк.passthm, both only ever present on
the original author's own Mac under ~/Downloads, never in this repo). Each
fixture is a minimal 10-entry zip (digits 0-9, a 1x1 PNG payload) built to
reproduce the one naming quirk that made each original archive notable:

- MinePass_Nightly.passthm: every source file is "ru-" prefixed instead of
  "en-" (see docs/superpowers/specs/2026-09-17-passcode-theme-creator-design.md).
  Digit 2 uses the exact filename from that bug report.
- тцк.passthm: source files carry no language prefix at all, just the digit.

parse_passthm_archive() fans out to every locale (en/other/ru/uk + Cyrillic
subtexts) from the digit alone, regardless of the source file's own naming,
so this synthetic content exercises the same code paths the real archives did
for every assertion in test_backend_passthm.py.

Run from anywhere; writes next to this script.
"""
import base64
import zipfile
from pathlib import Path

PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


def main() -> None:
    here = Path(__file__).resolve().parent

    minepass = here / "MinePass_Nightly.passthm"
    with zipfile.ZipFile(minepass, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("ru-2-A B C--white.png", PNG_1X1)
        for d in range(10):
            if d == 2:
                continue
            z.writestr(f"ru-{d}---white.png", PNG_1X1)

    tck = here / "тцк.passthm"
    with zipfile.ZipFile(tck, "w", zipfile.ZIP_DEFLATED) as z:
        for d in range(10):
            z.writestr(f"{d}--white.png", PNG_1X1)

    print(f"wrote {minepass}")
    print(f"wrote {tck}")


if __name__ == "__main__":
    main()
