# Gene Order SVG Drawer

A simple Python script for visualizing mitochondrial gene order from a tab-delimited gene order file and exporting editable SVG figures.

## Usage

```bash
python draw_gene_order.py -i example_gene_order.txt -o gene_order.svg

## Preparation of input files

The `gene_order` input file can be generated using PhyloSuite. Briefly, all sequences should be imported into PhyloSuite, followed by clicking `Extract`. The resulting `linear_order.txt` file located in the extracted `files` directory can then be directly used as the input file for this script.
