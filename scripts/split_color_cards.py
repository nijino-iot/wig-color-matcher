#!/usr/bin/env python3
"""Split 千型 color card sheets into individual swatches."""

from pathlib import Path
from PIL import Image

# Source files and their number ranges
SOURCE_FILES = [
    ("千型1-24.jpg", 1),
    ("千型25-48.jpg", 25),
    ("千型49-72.jpg", 49),
    ("千型73-96.jpg", 73),
    ("千型97-120.jpg", 97),
    ("千型121-144.jpg", 121),
]

# Grid configuration: 4 rows × 6 columns
ROWS = 4
COLS = 6

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent / "public" / "wig_cards"


def get_grid_params(img: Image.Image, filename: str) -> dict:
    """
    Get grid parameters based on image size.
    Returns dict with left, right, row_tops (list of y positions), row_height.
    """
    w, h = img.size
    
    if w == 1500 and h == 1691:
        # 千型1-24.jpg - has header text
        # Grid is on the right side, 6 columns from x=710 to x=1460
        return {
            'left': 710,
            'right': 1460,
            'row_tops': [240, 530, 820, 1110],
            'row_height': 200,
        }
    elif w == 1440 and h == 1440:
        # 千型97-120, 121-144 - square format
        # Rows have large gaps between them
        return {
            'left': 678,
            'right': 1408,
            'row_tops': [50, 330, 630, 900],
            'row_height': 170,
        }
    elif w == 800 and h == 800:
        # 千型25-48, 49-72, 73-96 - smaller square
        # Rows have gaps between them
        return {
            'left': 368,
            'right': 785,
            'row_tops': [25, 200, 350, 500],
            'row_height': 120,
        }
    else:
        # Fallback
        row_h = int(h * 0.15)
        return {
            'left': int(w * 0.45),
            'right': int(w * 0.98),
            'row_tops': [int(h * 0.04 + i * h * 0.16) for i in range(4)],
            'row_height': row_h,
        }


def split_image(src_path: Path, start_num: int, output_dir: Path) -> list[Path]:
    """Split a color card sheet into individual swatches."""
    img = Image.open(src_path)
    params = get_grid_params(img, src_path.name)
    
    left = params['left']
    right = params['right']
    row_tops = params['row_tops']
    row_height = params['row_height']
    
    grid_width = right - left
    cell_width = grid_width // COLS
    
    print(f"Processing {src_path.name}")
    print(f"  Image size: {img.size}")
    print(f"  Grid: left={left}, right={right}, cell_w={cell_width}")
    print(f"  Row tops: {row_tops}, row_h={row_height}")
    
    output_files = []
    num = start_num
    
    for row in range(ROWS):
        row_top = row_tops[row]
        
        for col in range(COLS):
            # Calculate cell bounds
            x1 = left + col * cell_width
            y1 = row_top
            x2 = x1 + cell_width
            y2 = min(y1 + row_height, img.size[1])  # Don't exceed image bounds
            
            # Crop with padding to remove number labels and white borders
            label_height = max(8, min(35, int(row_height * 0.18)))
            margin_x = 12  # Horizontal margin to exclude white borders
            margin_y = 8   # Vertical margin
            
            crop_box = (
                x1 + margin_x,
                y1 + label_height,
                x2 - margin_x,
                y2 - margin_y
            )
            
            cell = img.crop(crop_box)
            
            # Output filename
            out_path = output_dir / f"千型{num}.png"
            cell.save(out_path, "PNG")
            output_files.append(out_path)
            
            num += 1
    
    print(f"  Saved: 千型{start_num}.png ~ 千型{num-1}.png")
    return output_files


def main():
    home = Path.home()
    output_dir = OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Output directory: {output_dir}")
    print()
    
    all_outputs = []
    for filename, start_num in SOURCE_FILES:
        src_path = home / filename
        if src_path.exists():
            outputs = split_image(src_path, start_num, output_dir)
            all_outputs.extend(outputs)
        else:
            print(f"WARNING: {src_path} not found, skipping")
    
    print()
    print(f"Total files created: {len(all_outputs)}")


if __name__ == "__main__":
    main()
