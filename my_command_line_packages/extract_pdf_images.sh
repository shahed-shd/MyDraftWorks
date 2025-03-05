#!/bin/bash

# Description:
# Extract images from pdf files in a directory
# Example:
#   bash extract_pdf_images.sh <intput-dir> <output-dir>
# Here, input-dir and output-dir are optional

# Set the input directory (default to current directory if not provided)
INPUT_DIR="${1:-.}"

# Set output directory
OUTPUT_DIR="${2:-./extracted_images}"
mkdir -p "$OUTPUT_DIR"

# Loop through all PDF files in the input directory
for pdf_file in "$INPUT_DIR"/*.pdf; do
    # Skip if no PDF files are found
    [ -e "$pdf_file" ] || continue

    # Get the base filename (without extension)
    base_name=$(basename "$pdf_file" .pdf)

    echo "Extracting images from: $pdf_file"

    # Extract images using pdfimages
    pdfimages -all "$pdf_file" "$OUTPUT_DIR/$base_name"

    echo "Images saved in: $OUTPUT_DIR"
done

echo "Image extraction completed!"
