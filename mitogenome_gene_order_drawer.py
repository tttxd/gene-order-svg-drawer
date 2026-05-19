import re
import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Draw mitochondrial gene order diagram and export editable SVG."
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Input gene order file in txt format."
    )
    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output SVG file."
    )
    return parser.parse_args()


def gene_color(gene):
    gene = gene.lower()
    if gene.startswith("cox"):
        return "#8CB3E6"
    if gene.startswith("nad"):
        return "#95C98B"
    if gene.startswith("atp"):
        return "#E8B06A"
    if gene.startswith("cob"):
        return "#B79AD8"
    return "#CCCCCC"


def arrow_points(x, y, w, h, direction):
    head = 16
    top = y - h / 2
    bottom = y + h / 2

    if direction == "+":
        pts = [
            (x, top), (x + w - head, top),
            (x + w, y),
            (x + w - head, bottom), (x, bottom)
        ]
    else:
        pts = [
            (x + w, top), (x + head, top),
            (x, y),
            (x + head, bottom), (x + w, bottom)
        ]

    return " ".join(f"{px},{py}" for px, py in pts)


def read_gene_order(input_file):
    records = {}
    name = None

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            if line.startswith(">"):
                name = line[1:]
                records[name] = []
            else:
                for raw in line.split("\t"):
                    direction = "-" if raw.startswith("-") else "+"
                    gene = raw[1:] if direction == "-" else raw
                    base_gene = re.sub(r"_copy\d+$", "", gene)

                    records[name].append({
                        "raw": raw,
                        "gene": gene,
                        "base": base_gene,
                        "direction": direction
                    })

    return records


def draw_svg(records, output_svg):
    left_margin = 320
    top_margin = 120
    row_gap = 50
    arrow_w = 85
    arrow_h = 24

    max_genes = max(len(v) for v in records.values())
    width = left_margin + max_genes * arrow_w + 100
    height = top_margin + len(records) * row_gap + 80

    svg = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
    )

    svg.append("""
<style>
.title { font: bold 24px Arial; fill: #222; }
.species { font: italic 14px Arial; fill: #222; }
.gene { font: 10px Arial; fill: #111; }
.legend { font: 13px Arial; fill: #222; }
</style>
""")

    svg.append(
        '<text x="40" y="45" class="title">'
        'Comparative mitochondrial gene order'
        '</text>'
    )
    svg.append(
        '<text x="40" y="72" class="legend">'
        'Arrow direction indicates gene orientation.'
        '</text>'
    )

    legend_items = [
        ("cox genes", "#8CB3E6"),
        ("nad genes", "#95C98B"),
        ("atp genes", "#E8B06A"),
        ("cob gene", "#B79AD8")
    ]

    for i, (label, color) in enumerate(legend_items):
        x = 40 + i * 160
        y = 95
        svg.append(
            f'<rect x="{x}" y="{y}" width="20" height="12" '
            f'fill="{color}" stroke="#444"/>'
        )
        svg.append(
            f'<text x="{x + 28}" y="{y + 11}" class="legend">{label}</text>'
        )

    for idx, (species, genes) in enumerate(records.items()):
        y = top_margin + idx * row_gap
        display_name = species.replace("_", " ")

        svg.append(
            f'<text x="40" y="{y + 5}" class="species">{display_name}</text>'
        )

        for j, g in enumerate(genes):
            x = left_margin + j * arrow_w
            color = gene_color(g["base"])
            pts = arrow_points(x, y, arrow_w - 8, arrow_h, g["direction"])

            svg.append(
                f'<polygon points="{pts}" fill="{color}" '
                f'stroke="#333" stroke-width="0.8"/>'
            )
            svg.append(
                f'<text x="{x + (arrow_w - 8) / 2}" y="{y + 4}" '
                f'class="gene" text-anchor="middle">{g["gene"]}</text>'
            )

    svg.append("</svg>")

    Path(output_svg).write_text("\n".join(svg), encoding="utf-8")


def main():
    args = parse_args()
    records = read_gene_order(args.input)
    draw_svg(records, args.output)
    print(f"SVG saved to: {args.output}")


if __name__ == "__main__":
    main()
