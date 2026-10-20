"""Regenerate README.md's tool catalogue from the live server's own `tools/list`.

Everything written between the TOOLS markers, and the tool count between the COUNT markers, is
read from https://jeanslabs.vercel.app/mcp at run time, so the README can never list a tool the
server does not have. Run by .github/workflows/registry.yml daily; run by hand with
`python scripts/tools_readme.py`.
"""

import json
import re
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

ENDPOINT = "https://jeanslabs.vercel.app/mcp"
README = Path(__file__).resolve().parent.parent / "README.md"

# Shown in this order. A tool lands in the first section whose rule matches; anything unmatched
# falls into its server-declared capability, so a new tool is never dropped from the list.
SECTIONS = [
    ("cloning", "🧬 Cloning & assembly", "Digests, ligations, Gibson, Golden Gate, Gateway-style recombination, part grammars and assembly planning."),
    ("amplify", "🔥 PCR, primers & thermocycling", "Primer design for every kind of PCR, melting temperatures and reaction simulation."),
    ("crispr", "✂️ CRISPR & genome editing", "Guide design and scoring, off-targets, screens, and editing outcomes measured from traces."),
    ("sequencing", "📈 Sanger, sequencing & verification", "Trace reading, base calling, construct verification, read QC and alignment to a reference."),
    ("qpcr", "🧪 qPCR & digital PCR", "Amplification and melt curves, RDML runs, droplet gating, uncertainty and relative quantification."),
    ("design", "🎛️ Design & expression", "Codon optimisation, RBS and operons, probes, barcodes, genetic circuits and annotation."),
    ("phylo", "🌳 Alignment & phylogenetics", "Pairwise and multiple alignment, dot plots, model selection, trees and tree comparison."),
    ("variants", "🧫 Genomics, variants & copy number", "Variant calls, copy-number segmentation, LOH and mosaicism, genome regions."),
    ("protein", "🧩 Proteins, domains & proteomics", "Domains and motifs, residue sites, protein properties and peptide evidence."),
    ("chem", "⚗️ Cheminformatics", "Molecules, conformers, scaffolds, reactions, chemical space and library screening."),
    ("discovery", "🔬 Expression & hypothesis testing", "Differential expression, gene-set enrichment and falsification-tested discovery programmes."),
    ("data", "🗄️ Public databases & records", "Search and fetch from NCBI, EMBL-EBI, UCSC, UniProt and more, then hand the record to any tool."),
    ("analyze", "📊 Sequence analysis", "Everything else a bench scientist asks of a sequence."),
    ("pipelines", "🔗 Pipelines & lab records", "Chain tools into reproducible workflows, export records, keep lab notes."),
]

RULES = [
    ("cloning", r"gel|digest|ligat|gibson|golden_gate|assembl|domesticat|overhang"),
    ("design", r"codon|back_translate|rbs|operon|probe|circuit|barcode|index_oligo|annotat"),
    ("protein", r"antibody|antigen"),
    ("crispr", r"crispr|guide|sgrna|off_?target|base_edit|indel|tide|screen_"),
    ("qpcr", r"qpcr|cq|melt|rdml|droplet|dpcr|taqman|uncertainty|amplification"),
    ("phylo", r"tree|phylo|align|dot_plot|substitution|msa"),
    ("variants", r"variant|copy_number|region|cnv|loh|mosaic|population"),
    ("chem", r"molecul|compound|tautomer|conformer|scaffold|reaction|protonation|r_groups|activity_cliff|chemical|structure_library"),
    ("protein", r"protein|domain|motif|residue|peptide|blast_cdd|smart|proteom"),
    ("discovery", r"discover|differential|gene_set|enrichment|hypothes|gene_trait|falsif"),
    ("data", r"search_|fetch_|lookup_|query_database|list_databases|literature|accession|find_assemblies|list_samples|ontology|omics"),
    ("pipelines", r"workflow|experiment|export|deposit|construction|preference|collection|report"),
]

SKIP_CAPABILITIES = {"workspace"}  # editor-state tools: meaningful inside the workbench only


def fetch_tools():
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}).encode()
    req = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={"content-type": "application/json", "accept": "application/json, text/event-stream"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        text = r.read().decode()
    line = next(l for l in text.splitlines() if l.startswith("data: "))
    return json.loads(line[6:])["result"]["tools"]


def one_line(tool):
    contract = tool.get("_meta", {}).get("bio.jane/contract", {})
    text = contract.get("question") or tool.get("description", "")
    text = re.sub(r"`([^`]*)`", r"\1", text).replace("\n", " ").strip()
    # Workbench phrasing: over MCP the caller passes the data; there is no open project.
    text = re.sub(r"THIS PROJECT'S OWN records", "your own records", text)
    text = re.sub(r"\s+(in|into|from) this project\b", "", text)
    text = text.replace("the open record", "the record").replace("on the trace that is open", "on the trace")
    if not contract.get("question"):
        text = re.split(r"(?<=[.!?])\s|\s—\s", text, maxsplit=1)[0]
    return text if len(text) <= 220 else text[:217].rstrip() + "…"


def section_of(tool):
    name = tool["name"]
    for key, pattern in RULES:
        if re.search(pattern, name, re.I):
            return key
    cap = tool.get("_meta", {}).get("bio.jane/capability")
    if cap == "record":
        return "data"
    if cap in {s[0] for s in SECTIONS}:
        return cap
    return "pipelines" if cap is None else "analyze"


def render(tools):
    groups = defaultdict(list)
    for t in tools:
        if t.get("_meta", {}).get("bio.jane/capability") in SKIP_CAPABILITIES:
            continue
        groups[section_of(t)].append(t)
    shown = sum(len(v) for v in groups.values())
    out = []
    for key, heading, blurb in SECTIONS:
        items = sorted(groups.get(key, []), key=lambda t: t["annotations"].get("title", t["name"]).lower())
        if not items:
            continue
        out.append(f"<details>\n<summary><b>{heading}</b> · {len(items)} tools</summary>\n\n_{blurb}_\n")
        out.append("| Tool | What it answers |\n|---|---|")
        for t in items:
            title = t["annotations"].get("title", t["name"]).replace("|", "\\|")
            answer = one_line(t).replace("|", "\\|")
            out.append(f"| **{title}** <br><sub>`{t['name']}`</sub> | {answer} |")
        out.append("\n</details>\n")
    return shown, "\n".join(out)


def replace_between(text, tag, body):
    pattern = re.compile(rf"(<!-- {tag}:START -->)(.*?)(<!-- {tag}:END -->)", re.S)
    if not pattern.search(text):
        sys.exit(f"README.md has no {tag} markers")
    return pattern.sub(lambda m: f"{m.group(1)}{body}{m.group(3)}", text)


def main():
    tools = fetch_tools()
    shown, table = render(tools)
    text = README.read_text(encoding="utf-8")
    text = replace_between(text, "COUNT", str(shown))
    text = replace_between(text, "TOOLS", "\n" + table + "\n")
    README.write_text(text, encoding="utf-8", newline="\n")
    print(f"{shown} tools written")


if __name__ == "__main__":
    main()
