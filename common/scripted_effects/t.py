import argparse
import re

def transform_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    output_lines = []
    i = 0
    texture_index = 0

    while i < len(lines):
        line = lines[i]

        # Match start of a texture block
        if re.match(r'^\s*texture\s*=\s*{', line):
            indent = re.match(r'^(\s*)', line).group(1)
            block_type = 'if' if texture_index == 0 else 'else_if'
            output_lines.append(f'{indent}{block_type} = {{\n')
            texture_index += 1
            i += 1

            # Collect block lines and brace count
            block_lines = []
            ref_path = None
            brace_depth = 1

            while i < len(lines) and brace_depth > 0:
                block_line = lines[i]
                brace_depth += block_line.count('{')
                brace_depth -= block_line.count('}')
                block_lines.append(block_line)
                i += 1

            # Extract reference path (from any line in block)
            for bl in block_lines:
                match = re.search(r'reference\s*=\s*"([^"]+)"', bl)
                if match:
                    ref_path = match.group(1)
                    break

            # Transform block
            new_block = []
            j = 0
            while j < len(block_lines):
                bl = block_lines[j]

                if re.match(r'^\s*trigger\s*=\s*{', bl):
                    limit_indent = re.match(r'^(\s*)', bl).group(1)
                    new_block.append(f'{limit_indent}limit = {{\n')
                    j += 1
                    inner_brace_depth = 1

                    while j < len(block_lines) and inner_brace_depth > 0:
                        inner_line = block_lines[j]
                        inner_brace_depth += inner_line.count('{')
                        inner_brace_depth -= inner_line.count('}')
                        new_block.append(inner_line)
                        j += 1

                    # Now insert debug_log after closing limit
                    if ref_path:
                        new_block.append(f'{limit_indent}debug_log = "VOTC:IN/;/background/;/{ref_path}/;/"\n')

                elif 'reference' in bl:
                    # Skip the original reference line
                    j += 1
                else:
                    new_block.append(bl)
                    j += 1

            output_lines.extend(new_block)

        else:
            output_lines.append(line)
            i += 1

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)

def main():
    parser = argparse.ArgumentParser(description="Transform Paradox texture blocks to if/else_if structure with debug_log.")
    parser.add_argument("input", help="Path to input file")
    parser.add_argument("output", help="Path to output file")
    args = parser.parse_args()
    transform_file(args.input, args.output)
    print(f"[✓] File transformed and saved to: {args.output}")

if __name__ == "__main__":
    main()
