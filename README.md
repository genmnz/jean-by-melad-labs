<div align="center">

<img src="assets/logo.png" alt="Jean" width="96" height="96" />

# Jean by Melad Labs

**A molecular biology bench your AI assistant can actually calculate on.**

Cloning · PCR & primer design · CRISPR · Sanger verification · alignment · qPCR · phylogenetics

[![MCP Registry](https://img.shields.io/badge/MCP%20Registry-io.github.genmnz%2Fjean-0b7285)](https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.genmnz/jean)
![Transport](https://img.shields.io/badge/transport-Streamable%20HTTP-2b8a3e)
![Auth](https://img.shields.io/badge/auth-none-495057)
[![Docs](https://img.shields.io/badge/docs-jeanslabs.vercel.app-1971c2)](https://jeanslabs.vercel.app/docs/api/mcp)

</div>

---

Ask a general-purpose model for a melting temperature, a restriction map or a Gibson overlap and it
will give you a confident number from memory. Sometimes that number is right.

**Jean replaces "sometimes" with a calculation.** It is a remote [Model Context Protocol](https://modelcontextprotocol.io)
server that hands your assistant a full molecular biology toolkit. The model does the reasoning;
Jean does the science, and every answer comes back with the method, the parameters and the inputs
that produced it, so you can check a result instead of trusting it.

## Connect in thirty seconds

| | |
|---|---|
| **Server URL** | `https://jeanslabs.vercel.app/mcp` |
| **Transport** | Streamable HTTP |
| **Authentication** | None. No key, no account, no sign-up |
| **Cost** | Free |

**Claude** (claude.ai, Desktop, Code): [**add Jean as a connector**](https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=Jean&connectorUrl=https%3A%2F%2Fjeanslabs.vercel.app%2Fmcp); the dialog opens prefilled.

**Cursor**, `~/.cursor/mcp.json`:

```json
{ "mcpServers": { "jean": { "url": "https://jeanslabs.vercel.app/mcp" } } }
```

**VS Code**, `.vscode/mcp.json`:

```json
{ "servers": { "jean": { "type": "http", "url": "https://jeanslabs.vercel.app/mcp" } } }
```

**Anything else that speaks MCP:** add a remote server with the URL above. Field-by-field help for
every connector dialog: [jeanslabs.vercel.app/docs/api/mcp](https://jeanslabs.vercel.app/docs/api/mcp).

## What your assistant can do with it

| At the bench | Jean can |
|---|---|
| **Cloning** | Find restriction sites on linear and circular DNA, simulate digests and ligations, plan Gibson, Golden Gate and recombination assemblies, model site-directed mutagenesis |
| **PCR & primers** | Design PCR, qPCR, sequencing, LAMP, bisulfite and degenerate primers; compute melting temperatures from published thermodynamic tables; simulate PCR products, fusion and multiplex reactions |
| **Genome editing** | Design and score CRISPR guides, check off-targets, and quantify editing outcomes from Sanger traces |
| **Sequence verification** | Align Sanger reads to a reference and confirm a construct base by base |
| **qPCR & dPCR** | Fit amplification curves to Cq, call melt-curve Tm, read RDML run files, gate droplets and estimate concentration |
| **Alignment & evolution** | Build multiple sequence alignments and phylogenetic trees |
| **Design & expression** | Optimise codons for a host, back-translate proteins, design RBS sites and barcodes, annotate features automatically |
| **Public data** | Search and fetch records from NCBI, EMBL-EBI, UCSC and UniProt, then hand them straight to any tool |
| **Pipelines** | Chain tools into a reproducible workflow and run it in a single call |

Every tool returns structured data that matches a declared schema, and where a result is a picture
(a plasmid map, a gel, a trace, a tree) you get it as both SVG and PNG.

## Try asking

> *"Design primers to amplify GFP from my plasmid with BamHI and XhoI sites, and give me the Tm of each."*
>
> *"Which enzymes cut this plasmid exactly once? It is circular."*
>
> *"Here are my four fragments. Plan a Gibson assembly and tell me the overlaps."*
>
> *"Align these Sanger reads to my construct and tell me whether the insert is correct."*
>
> *"Rank these sgRNAs by predicted efficiency and off-target risk."*
>
> *"Analyse this qPCR run and give me ΔΔCq for the target against GAPDH."*

A small honesty test: ask for EcoRI sites on the circular sequence `AATTCTTAGGATCCG`. The only site
spans the point where the circle closes, so an answer that reads the sequence as a straight line
finds nothing. Jean finds it.

## Why scientists trust the numbers

- **Checked, not guessed.** Each engine is tested against the reference implementations the field
  already relies on, on their own data, before it ships.
- **Explained.** Results carry the model, parameters and inputs behind them, so a reviewer can
  reproduce any number.
- **Honest refusals.** Ask for an enzyme that does not exist and Jean says so by name, instead of
  returning an empty list that reads as "no sites".
- **Private by design.** The server is stateless: nothing you send is stored, and nothing is carried
  between calls.

## Also a workbench

The same engine runs in your browser at [**jeanslabs.vercel.app**](https://jeanslabs.vercel.app):
a plasmid and sequence editor with cloning simulation, primer design, gel and Sanger views, free and
with no account.

## About this repository

This repository is the public home of the Jean MCP listing. It contains no source code: Jean is
proprietary software by **Melad Labs** (© Melad Labs, all rights reserved), offered as the hosted
service above. Its registry entry, `io.github.genmnz/jean`, is kept current automatically.

Found a wrong answer, or want a tool added? [Open an issue](https://github.com/genmnz/jean-by-melad-labs/issues).

<sub>**Keywords:** MCP server · Model Context Protocol · remote MCP · bioinformatics · molecular biology ·
computational biology · life sciences · genomics · synthetic biology · DNA · RNA · protein · plasmid ·
plasmid map · vector design · cloning · molecular cloning · in silico cloning · restriction enzyme ·
restriction digest · ligation · Gibson assembly · Golden Gate · recombination cloning · site-directed
mutagenesis · PCR · primer design · qPCR · RT-qPCR · ΔΔCq · digital PCR · ddPCR · melting temperature ·
Tm calculator · LAMP · bisulfite sequencing · degenerate primers · CRISPR · Cas9 · sgRNA · guide RNA
design · off-target · genome editing · Sanger sequencing · chromatogram · sequence alignment ·
multiple sequence alignment · MSA · phylogenetics · phylogenetic tree · codon optimization ·
back-translation · RBS design · DNA barcodes · GenBank · FASTA · RDML · NCBI · EMBL-EBI · UCSC ·
UniProt · AI for science · AI scientist · Claude connector · ChatGPT app · Cursor · VS Code · LLM tools</sub>
