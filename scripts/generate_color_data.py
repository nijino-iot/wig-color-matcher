#!/usr/bin/env python3
"""
Generate color data for 千型 color cards.
This script analyzes the color cards and extracts RGB values.
"""

import json
import os
from pathlib import Path
from PIL import Image
import numpy as np

def analyze_image_colors(image_path):
    """Analyze an image and extract dominant color."""
    try:
        img = Image.open(image_path)
        # Convert to RGB if necessary
        img = img.convert('RGB')
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # Calculate average color (excluding potential borders/edges)
        # Take center portion to avoid edge artifacts
        h, w = img_array.shape[:2]
        center_h_start = h // 4
        center_h_end = 3 * h // 4
        center_w_start = w // 4
        center_w_end = 3 * w // 4
        
        center_region = img_array[center_h_start:center_h_end, center_w_start:center_w_end]
        
        # Calculate average RGB
        avg_rgb = np.mean(center_region, axis=(0, 1)).astype(int)
        
        return avg_rgb.tolist()
    except Exception as e:
        print(f"Error analyzing {image_path}: {e}")
        return [128, 128, 128]  # Default gray


def main():
    # Define paths
    cards_dir = Path.home() / "dev" / "wig-matcher" / "public" / "wig_cards"
    output_file = Path.home() / "dev" / "wig-matcher" / "src" / "assets" / "color_cards.json"
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Find all 千型 color cards
    color_cards = []
    
    for i in range(1, 145):  # 1 to 144
        filename = f"千型{i}.png"
        image_path = cards_dir / filename
        
        if image_path.exists():
            rgb = analyze_image_colors(image_path)
            
            card_info = {
                "code": str(i),
                "filename": filename,
                "rgb": rgb
            }
            
            color_cards.append(card_info)
            print(f"Processed 千型{i}: RGB{rgb}")
        else:
            print(f"Warning: {filename} not found")
    
    # Write to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(color_cards, f, ensure_ascii=False, indent=2)
    
    print(f"\nGenerated {output_file}")
    print(f"Total color cards processed: {len(color_cards)}")


if __name__ == "__main__":
    main()