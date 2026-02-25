#!/usr/bin/env python
from argparse import ArgumentParser, SUPPRESS
from pathlib import Path
import core.watermarker_image as wm_img

parser = ArgumentParser(
    prog="Watermarker",
    description="Pass an image file or a folder of images, adding a watermark to them"
)
parser.add_argument(
    "path",
    help="Input path, may be a file or a folder",
    type=Path
)
parser.add_argument(
    "--mode", "-m",
    default="Image",
    help=SUPPRESS
)

if __name__ == '__main__':
    args = parser.parse_args()
    path: Path = args.path
    mode: str = args.mode

    if not path.exists():
        exit(1)

    if path.is_dir():
        files = [p for p in path.rglob('*') if p.is_file()]
    elif path.is_file():
        files = [path]
    
    match mode.lower():
        case "image":
            marker_function = wm_img.add_watermark
        case _:
            exit(1)
    
    for f in files:
        outpath = f.parent / Path(f.stem + ".marked" + f.suffix)
        marker_function(
            f,
            outpath
        )
