#!/usr/bin/env python3
"""
build_georgia_mining.py — Static site generator for the Georgia Mining Research site.

Reads a directory of pre-written HTML articles and generates an earth-toned
research homepage with search, category filtering, and a data catalog section,
then syncs to S3.

Usage:
    python3 build_georgia_mining.py \\
        --source /path/to/articles/ \\
        --s3-bucket s3://my-bucket/path/ \\
        --data-dir /path/to/data/
"""

import os
import sys
import shutil
import argparse
import subprocess
import json
import re
from datetime import datetime

try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

# ---------------------------------------------------------------------------
# HTML Templates
# ---------------------------------------------------------------------------

DATA_PAGE_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Repository | {site_name}</title>
    <meta name="description" content="Downloadable datasets for Georgia geological and mining research">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Inter:wght@300;400;500;600&family=Space+Mono&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="georgia_mining.css">
    <style>
        .data-page-container {{
            max-width: var(--max-width);
            margin: 0 auto;
            padding: 2.5rem 1.5rem;
        }}
        .data-page-header {{
            margin-bottom: 2.5rem;
        }}
        .data-page-header h1 {{
            font-family: var(--serif);
            font-size: 2rem;
            font-weight: 700;
            color: var(--geo-slate);
            border-bottom: 3px solid var(--geo-gold);
            padding-bottom: 0.75rem;
            margin-bottom: 0.75rem;
        }}
        .data-page-header p {{
            color: var(--gray-500);
            font-size: 0.95rem;
        }}
        .data-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 1px;
            background: var(--gray-200);
            border: 1px solid var(--gray-200);
            margin-bottom: 2.5rem;
        }}
        .data-stats .dst {{
            background: var(--white);
            padding: 1.25rem;
            text-align: center;
        }}
        .data-stats .dst-val {{
            font-family: var(--serif);
            font-size: 1.75rem;
            font-weight: 900;
            color: var(--geo-green);
            line-height: 1;
        }}
        .data-stats .dst-lbl {{
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: var(--gray-500);
            margin-top: 0.35rem;
            font-weight: 600;
        }}
        .data-search {{
            margin-bottom: 2rem;
        }}
        .data-search input {{
            width: 100%;
            border: 2px solid var(--gray-200);
            border-bottom: 2px solid var(--geo-slate);
            padding: 0.75rem 1rem;
            font-size: 0.95rem;
            font-family: var(--sans);
            outline: none;
        }}
        .data-search input:focus {{
            border-color: var(--geo-green);
            border-bottom-color: var(--geo-green);
        }}

        /* ── File cards ── */
        .data-file-list {{
            display: flex;
            flex-direction: column;
            gap: 0;
        }}
        .data-file-card {{
            border: 1px solid var(--gray-200);
            border-bottom: none;
            background: var(--white);
            transition: background 0.15s;
        }}
        .data-file-card:last-child {{ border-bottom: 1px solid var(--gray-200); }}
        .data-file-card:hover {{ background: var(--gray-50); }}
        .data-file-card.active {{ background: var(--gray-50); border-color: var(--geo-gold); }}
        .data-file-card.active + .data-file-card {{ border-top-color: var(--geo-gold); }}
        .file-card-header {{
            display: grid;
            grid-template-columns: 50px 1fr auto auto auto;
            align-items: center;
            gap: 1rem;
            padding: 1rem 1.25rem;
            cursor: pointer;
        }}
        @media (max-width: 700px) {{
            .file-card-header {{
                grid-template-columns: 50px 1fr;
                gap: 0.5rem;
            }}
            .file-card-header .fsize,
            .file-card-header .fdate,
            .file-card-header .preview-btn {{ grid-column: 1 / -1; }}
        }}
        .fmt-badge {{
            display: inline-block;
            background: var(--geo-slate);
            color: var(--geo-gold);
            font-family: var(--mono);
            font-size: 0.65rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            padding: 0.25rem 0.5rem;
            text-transform: uppercase;
            text-align: center;
            min-width: 36px;
        }}
        .file-card-info {{}}
        .file-card-info .fname {{
            font-family: var(--mono);
            font-size: 0.88rem;
            font-weight: 700;
        }}
        .file-card-info .fname a {{
            color: var(--geo-green);
            text-decoration: none;
        }}
        .file-card-info .fname a:hover {{ text-decoration: underline; }}
        .file-card-info .fdesc {{
            font-size: 0.82rem;
            color: var(--gray-500);
            margin-top: 0.2rem;
            line-height: 1.4;
        }}
        .file-card-info .fsource {{
            font-size: 0.75rem;
            margin-top: 0.15rem;
        }}
        .file-card-info .fsource a {{
            color: var(--geo-copper);
            text-decoration: underline;
            text-decoration-thickness: 1px;
            word-break: break-all;
        }}
        .fsize {{
            font-family: var(--mono);
            font-size: 0.8rem;
            color: var(--gray-500);
            white-space: nowrap;
        }}
        .fdate {{
            font-family: var(--mono);
            font-size: 0.78rem;
            color: var(--gray-400);
            white-space: nowrap;
        }}
        .preview-btn {{
            background: var(--white);
            border: 1.5px solid var(--geo-slate);
            color: var(--geo-slate);
            padding: 0.35rem 0.85rem;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            cursor: pointer;
            font-family: var(--sans);
            transition: all 0.15s;
            white-space: nowrap;
        }}
        .preview-btn:hover {{
            background: var(--geo-slate);
            color: var(--geo-gold);
        }}
        .active .preview-btn {{
            background: var(--geo-slate);
            color: var(--geo-gold);
        }}

        /* ── Preview drawer ── */
        .preview-drawer {{
            display: none;
            border-top: 2px solid var(--geo-gold);
            background: var(--gray-50);
            padding: 1.5rem;
            max-height: 75vh;
            overflow: auto;
        }}
        .data-file-card.active .preview-drawer {{ display: block; }}

        /* ── PDF Embed ── */
        .pdf-embed {{
            width: 100%;
            height: 70vh;
            border: 1px solid var(--gray-200);
            background: var(--white);
        }}

        /* ── CSV Preview ── */
        .csv-meta {{
            display: flex;
            gap: 2rem;
            flex-wrap: wrap;
            margin-bottom: 1.25rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid var(--gray-200);
        }}
        .csv-meta-item {{
            font-family: var(--sans);
            font-size: 0.82rem;
        }}
        .csv-meta-item .label {{
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-size: 0.68rem;
            color: var(--gray-500);
            display: block;
        }}
        .csv-meta-item .value {{
            font-family: var(--mono);
            font-size: 0.95rem;
            color: var(--geo-slate);
            font-weight: 700;
        }}
        .csv-table-wrap {{
            overflow-x: auto;
            max-width: 100%;
            -webkit-overflow-scrolling: touch;
            margin-bottom: 1.5rem;
            border: 1px solid var(--gray-200);
        }}
        .csv-preview-table {{
            width: 100%;
            border-collapse: collapse;
            font-family: var(--mono);
            font-size: 0.78rem;
        }}
        .csv-preview-table th {{
            background: var(--geo-slate);
            color: var(--geo-gold);
            padding: 0.5rem 0.75rem;
            text-align: left;
            font-size: 0.68rem;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            font-weight: 700;
            white-space: nowrap;
            position: sticky;
            top: 0;
            cursor: pointer;
        }}
        .csv-preview-table th:hover {{ background: #2a3540; }}
        .csv-preview-table td {{
            padding: 0.4rem 0.75rem;
            border-bottom: 1px solid var(--gray-200);
            white-space: nowrap;
            max-width: 300px;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .csv-preview-table tr:nth-child(even) td {{ background: rgba(0,0,0,0.02); }}
        .csv-preview-table tr:hover td {{ background: rgba(212,160,23,0.06); }}
        .csv-truncated {{
            text-align: center;
            font-size: 0.78rem;
            color: var(--gray-400);
            padding: 0.5rem;
            font-style: italic;
            background: var(--gray-50);
            border: 1px solid var(--gray-200);
            border-top: none;
        }}

        /* ── Column Stats ── */
        .col-stats {{
            margin-top: 1rem;
        }}
        .col-stats h4 {{
            font-family: var(--serif);
            font-size: 1rem;
            font-weight: 700;
            color: var(--geo-slate);
            margin-bottom: 0.75rem;
            border-bottom: 2px solid var(--geo-slate);
            padding-bottom: 0.4rem;
        }}
        .col-stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 1rem;
        }}
        .col-stat-card {{
            background: var(--white);
            border: 1px solid var(--gray-200);
            padding: 0.85rem 1rem;
        }}
        .col-stat-card .col-name {{
            font-family: var(--mono);
            font-size: 0.78rem;
            font-weight: 700;
            color: var(--geo-green);
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 0.4rem;
        }}
        .col-stat-card .col-detail {{
            font-size: 0.78rem;
            color: var(--gray-600);
            line-height: 1.6;
        }}
        .col-stat-card .col-detail strong {{
            color: var(--geo-slate);
        }}
        .top-val {{
            display: inline-block;
            background: var(--gray-100);
            padding: 0.1rem 0.4rem;
            margin: 0.1rem 0.15rem;
            font-family: var(--mono);
            font-size: 0.72rem;
            border-radius: 2px;
        }}

        .no-data-msg {{
            text-align: center;
            color: var(--gray-500);
            padding: 4rem 0;
            font-style: italic;
        }}
    </style>
</head>
<body class="site-wrapper">

<header class="site-header">
    <a href="index.html" class="site-title"><span class="title-accent">⛏</span> {site_name}</a>
    <nav style="display: flex; gap: 1.5rem;">
        <a href="index.html" style="color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.06em;">Research</a>
        <a href="data.html" style="color: var(--geo-gold); text-decoration: none; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 700;">Data</a>
        <a href="map.html" style="color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.06em;">Map</a>
        <a href="analyze.html" style="color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.06em;">Analyze</a>
    </nav>
</header>

<main class="data-page-container">
    <div class="data-page-header">
        <h1>Data Repository</h1>
        <p>Publicly available datasets mirrored for Georgia geological and mining research. Click any file to preview — PDFs open inline, CSVs show an interactive table with column analytics.</p>
    </div>

    {data_stats_html}

    <div class="data-search">
        <input type="text" id="data-search" placeholder="Search datasets by name, format, or description..." autocomplete="off">
    </div>

    {data_cards_html}
</main>

<footer class="site-footer">
    <span class="footer-name">⛏ {site_name}</span>
    <p>Building a comprehensive open research base on Georgia&rsquo;s geological heritage and mineral wealth.</p>
</footer>

<script>
/* ── Search ── */
const searchInput = document.getElementById('data-search');
const cards = document.querySelectorAll('.data-file-card');
searchInput.addEventListener('input', function() {{
    const q = this.value.toLowerCase().trim();
    cards.forEach(card => {{
        const text = card.textContent.toLowerCase();
        card.style.display = (!q || text.includes(q)) ? '' : 'none';
    }});
}});

/* ── Preview toggle ── */
function togglePreview(fileId) {{
    const card = document.getElementById('card-' + fileId);
    const wasActive = card.classList.contains('active');
    // Close all open
    cards.forEach(c => c.classList.remove('active'));
    if (!wasActive) {{
        card.classList.add('active');
        // Lazy-load PDF if needed
        const pdfFrame = card.querySelector('.pdf-embed[data-src]');
        if (pdfFrame && !pdfFrame.src) {{
            pdfFrame.src = pdfFrame.getAttribute('data-src');
        }}
    }}
}}

/* ── CSV Preview ── */
const csvPreviews = {csv_previews_json};

function renderCsvPreview(fileId) {{
    const data = csvPreviews[fileId];
    if (!data) return;
    const container = document.getElementById('csv-preview-' + fileId);
    if (container.dataset.rendered) return;
    container.dataset.rendered = '1';

    const rows = data.rows;
    const cols = data.columns;
    const totalRows = data.total_rows;
    const stats = data.stats;

    // Build table
    let tableHtml = '<div class="csv-meta">';
    tableHtml += `<div class="csv-meta-item"><span class="label">Rows</span><span class="value">${{totalRows.toLocaleString()}}</span></div>`;
    tableHtml += `<div class="csv-meta-item"><span class="label">Columns</span><span class="value">${{cols.length}}</span></div>`;
    tableHtml += `<div class="csv-meta-item"><span class="label">Preview</span><span class="value">First ${{rows.length}} rows</span></div>`;
    tableHtml += '</div>';

    tableHtml += '<div class="csv-table-wrap"><table class="csv-preview-table"><thead><tr>';
    cols.forEach(c => {{ tableHtml += `<th>${{c}}</th>`; }});
    tableHtml += '</tr></thead><tbody>';
    rows.forEach(row => {{
        tableHtml += '<tr>';
        cols.forEach(c => {{
            const val = row[c] ?? '';
            const display = String(val).length > 60 ? String(val).substring(0, 57) + '...' : String(val);
            tableHtml += `<td title="${{String(val).replace(/"/g, '&quot;')}}">${{display}}</td>`;
        }});
        tableHtml += '</tr>';
    }});
    tableHtml += '</tbody></table></div>';
    if (rows.length < totalRows) {{
        tableHtml += `<div class="csv-truncated">Showing ${{rows.length}} of ${{totalRows.toLocaleString()}} rows \u00b7 <a href="data/${{fileId}}" download style="color:var(--geo-green);">Download full CSV</a></div>`;
    }}

    // Column stats
    if (stats && Object.keys(stats).length) {{
        tableHtml += '<div class="col-stats"><h4>Column Analytics</h4><div class="col-stats-grid">';
        cols.forEach(c => {{
            const s = stats[c];
            if (!s) return;
            let detail = `<strong>${{s.unique}}</strong> unique values<br>`;
            if (s.nulls > 0) detail += `<strong>${{s.nulls}}</strong> null/empty<br>`;
            if (s.top && s.top.length) {{
                detail += 'Top: ';
                s.top.forEach(t => {{
                    detail += `<span class="top-val">${{t[0]}} <span style="color:var(--gray-400)">\u00d7${{t[1]}}</span></span>`;
                }});
            }}
            tableHtml += `<div class="col-stat-card"><div class="col-name">${{c}}</div><div class="col-detail">${{detail}}</div></div>`;
        }});
        tableHtml += '</div></div>';
    }}

    container.innerHTML = tableHtml;
}}

document.querySelectorAll('.data-file-card[data-csv]').forEach(card => {{
    const observer = new MutationObserver(() => {{
        if (card.classList.contains('active')) {{
            renderCsvPreview(card.dataset.csv);
        }}
    }});
    observer.observe(card, {{ attributes: true, attributeFilter: ['class'] }});
}});
</script>
</body>
</html>
"""

INDEX_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_name}</title>
    <meta name="description" content="{site_tagline}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Inter:wght@300;400;500;600&family=Space+Mono&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="georgia_mining.css">
    <style>
        /* ── Hero Section ── */
        .hero {{
            background: var(--geo-slate);
            color: var(--white);
            padding: 4rem 2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        .hero::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background:
                repeating-linear-gradient(
                    0deg,
                    transparent,
                    transparent 40px,
                    rgba(212,160,23,0.03) 40px,
                    rgba(212,160,23,0.03) 41px
                ),
                repeating-linear-gradient(
                    90deg,
                    transparent,
                    transparent 40px,
                    rgba(212,160,23,0.03) 40px,
                    rgba(212,160,23,0.03) 41px
                );
            pointer-events: none;
        }}
        .hero h1 {{
            font-family: var(--serif);
            font-size: clamp(2rem, 5vw, 3.5rem);
            font-weight: 900;
            margin-bottom: 0.75rem;
            line-height: 1.1;
            position: relative;
        }}
        .hero h1 .accent {{ color: var(--geo-gold); }}
        .hero p {{
            font-size: 1.15rem;
            color: rgba(255,255,255,0.75);
            max-width: 650px;
            margin: 0 auto;
            position: relative;
        }}
        .hero .strata {{
            height: 6px;
            margin-top: 2rem;
            background: repeating-linear-gradient(
                90deg,
                var(--geo-copper) 0px, var(--geo-copper) 4px,
                var(--geo-gold) 4px, var(--geo-gold) 8px,
                var(--geo-green) 8px, var(--geo-green) 12px,
                var(--geo-clay) 12px, var(--geo-clay) 16px,
                var(--geo-mica) 16px, var(--geo-mica) 20px
            );
            position: relative;
        }}

        /* ── Search Bar ── */
        .search-bar {{
            background: var(--white);
            padding: 1.25rem 1.5rem;
            border-bottom: 1px solid var(--gray-200);
        }}
        .search-bar-inner {{
            max-width: var(--max-width);
            margin: 0 auto;
            display: flex;
            align-items: center;
            gap: 1rem;
            flex-wrap: wrap;
        }}
        .search-bar label {{
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: var(--geo-copper);
            white-space: nowrap;
        }}
        .search-input {{
            flex: 1;
            min-width: 200px;
            border: 2px solid var(--gray-200);
            border-bottom: 2px solid var(--geo-slate);
            padding: 0.65rem 1rem;
            font-size: 0.95rem;
            font-family: var(--sans);
            background: var(--white);
            outline: none;
            transition: all 0.2s;
        }}
        .search-input:focus {{
            border-color: var(--geo-copper);
            border-bottom-color: var(--geo-copper);
        }}
        .search-input::placeholder {{ color: var(--gray-400); font-style: italic; }}
        .filter-select {{
            flex: 0 0 220px;
            border: 2px solid var(--gray-200);
            border-bottom: 2px solid var(--geo-slate);
            padding: 0.65rem 1rem;
            font-size: 0.9rem;
            font-family: var(--sans);
            background: var(--white);
            outline: none;
            cursor: pointer;
        }}

        /* ── Content Area ── */
        .main-content {{
            max-width: var(--max-width);
            margin: 0 auto;
            padding: 2.5rem 1.5rem;
        }}

        /* ── Stats Banner ── */
        .stats-banner {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1px;
            background: var(--gray-200);
            border: 1px solid var(--gray-200);
            margin-bottom: 3rem;
        }}
        .stats-banner .stat {{
            background: var(--white);
            padding: 1.25rem 1.5rem;
            text-align: center;
        }}
        .stats-banner .stat-val {{
            font-family: var(--serif);
            font-size: 2rem;
            font-weight: 900;
            color: var(--geo-copper);
            line-height: 1;
        }}
        .stats-banner .stat-lbl {{
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: var(--gray-500);
            margin-top: 0.35rem;
            font-weight: 600;
        }}

        /* ── Section Headers ── */
        .section-header {{
            font-family: var(--serif);
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--geo-slate);
            border-bottom: 3px solid var(--geo-slate);
            padding-bottom: 0.5rem;
            margin-bottom: 2rem;
            display: flex;
            justify-content: space-between;
            align-items: baseline;
        }}
        .section-header .count {{
            font-family: var(--mono);
            font-size: 0.8rem;
            color: var(--gray-500);
        }}

        /* ── Article Grid ── */
        .article-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }}
        .article-card {{
            border: 1px solid var(--gray-200);
            background: var(--white);
            padding: 1.75rem;
            transition: all 0.2s;
            display: flex;
            flex-direction: column;
            box-shadow: 0 2px 4px rgba(0,0,0,0.03);
        }}
        .article-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.08);
            border-color: var(--geo-gold);
        }}
        .article-card a {{
            text-decoration: none;
            color: inherit;
            display: flex;
            flex-direction: column;
            height: 100%;
        }}
        .article-card .card-tag {{
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: var(--geo-copper);
            margin-bottom: 0.75rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid var(--gray-100);
        }}
        .article-card .card-headline {{
            font-family: var(--serif);
            font-size: 1.35rem;
            font-weight: 700;
            line-height: 1.25;
            margin-bottom: 0.75rem;
            color: var(--geo-slate);
            transition: color 0.15s;
        }}
        .article-card:hover .card-headline {{ color: var(--geo-copper); }}
        .article-card .card-dek {{
            font-size: 0.95rem;
            color: var(--gray-500);
            line-height: 1.6;
            margin-bottom: 1.5rem;
            flex: 1;
        }}
        .article-card .card-date {{
            font-size: 0.78rem;
            color: var(--gray-400);
            font-family: var(--mono);
            text-transform: uppercase;
        }}

        /* ── Search Results ── */
        #search-results {{
            display: none;
        }}
        #search-results.visible {{ display: block; }}
        .search-result-item {{
            border-bottom: 1px solid var(--gray-200);
            padding: 1.25rem 0;
        }}
        .search-result-item a {{ text-decoration: none; color: inherit; display: block; }}
        .search-result-headline {{
            font-family: var(--serif);
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--geo-slate);
            margin-bottom: 0.35rem;
            transition: color 0.15s;
        }}
        .search-result-item a:hover .search-result-headline {{ color: var(--geo-copper); }}
        .search-result-meta {{
            font-size: 0.8rem;
            color: var(--gray-500);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
        }}
        .search-result-dek {{
            font-size: 0.95rem;
            color: var(--gray-500);
            margin-top: 0.25rem;
        }}
        .search-no-results {{
            font-size: 1rem;
            color: var(--gray-500);
            padding: 2rem 0;
            font-style: italic;
            text-align: center;
        }}

        /* ── Data section ── */
        .data-section {{
            background: var(--gray-50);
            border: 1px solid var(--gray-200);
            padding: 2rem;
            margin-bottom: 3rem;
        }}
        .data-list {{
            list-style: none;
            padding: 0;
        }}
        .data-list li {{
            padding: 0.6rem 0;
            border-bottom: 1px solid var(--gray-200);
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}
        .data-list li:last-child {{ border-bottom: none; }}
        .data-list .data-icon {{
            font-family: var(--mono);
            font-size: 0.75rem;
            color: var(--geo-green);
            font-weight: 700;
            text-transform: uppercase;
            flex-shrink: 0;
            width: 50px;
        }}
        .data-list .data-name {{
            font-weight: 600;
            color: var(--geo-slate);
        }}
    </style>
</head>
<body class="site-wrapper">

<header class="site-header">
    <a href="index.html" class="site-title"><span class="title-accent">⛏</span> {site_name}</a>
    <nav style="display: flex; gap: 1.5rem;">
        <a href="index.html" style="color: var(--geo-gold); text-decoration: none; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 700;">Research</a>
        <a href="data.html" style="color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.06em;">Data</a>
        <a href="map.html" style="color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.06em;">Map</a>
        <a href="analyze.html" style="color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.06em;">Analyze</a>
    </nav>
</header>

<div class="hero">
    <h1>Georgia <span class="accent">Geological</span> &amp; Mining Research</h1>
    <p>{site_tagline}</p>
    <div class="strata"></div>
</div>

<div class="search-bar">
    <div class="search-bar-inner">
        <label for="search-input">Explore:</label>
        <input type="text" id="search-input" class="search-input" placeholder="Search research articles, minerals, regions..." autocomplete="off">
        <select id="category-filter" class="filter-select">
            <option value="">All Categories</option>
            <option value="deep dive">Deep Dives</option>
            <option value="mine profile">Mine Profiles</option>
            <option value="commodity">Commodity Reports</option>
            <option value="data">Data Catalog</option>
            <option value="timeline">Timelines</option>
            <option value="regulatory">Regulatory</option>
            <option value="economic">Economic</option>
            <option value="comparative">Comparative</option>
        </select>
    </div>
</div>

<main class="main-content">
    <div id="search-results" role="region" aria-label="Search results"></div>

    <div id="article-listing">
        {stats_banner_html}
        {data_section_html}
        {article_listing_html}
    </div>
</main>

<footer class="site-footer">
    <span class="footer-name">⛏ {site_name}</span>
    <p>{site_tagline} &nbsp;·&nbsp; {today}</p>
    <p style="margin-top:0.5rem">Building a comprehensive open research base on Georgia&rsquo;s geological heritage and mineral wealth.</p>
</footer>

<script>
const searchIndex = {search_index_json};

const searchInput = document.getElementById('search-input');
const categoryFilter = document.getElementById('category-filter');
const searchResults = document.getElementById('search-results');
const articleListing = document.getElementById('article-listing');

function escapeHtml(str) {{
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}}

function executeSearch() {{
    const q = searchInput.value.toLowerCase().trim();
    const cat = categoryFilter.value.toLowerCase();

    if (!q && !cat) {{
        searchResults.classList.remove('visible');
        searchResults.innerHTML = '';
        articleListing.style.display = '';
        return;
    }}

    articleListing.style.display = 'none';
    searchResults.classList.add('visible');

    const matches = searchIndex.filter(a => {{
        const textMatch = !q || a.title.toLowerCase().includes(q) || (a.dek && a.dek.toLowerCase().includes(q));
        const catMatch = !cat || (a.tag && a.tag.toLowerCase().includes(cat));
        return textMatch && catMatch;
    }});

    if (matches.length === 0) {{
        searchResults.innerHTML = '<p class="search-no-results">No research articles found matching those criteria.</p>';
        return;
    }}

    searchResults.innerHTML = matches.map(m => `
        <div class="search-result-item">
            <a href="${{m.path}}">
                <div class="search-result-meta">${{escapeHtml(m.tag)}} &nbsp;·&nbsp; ${{escapeHtml(m.date)}}</div>
                <div class="search-result-headline">${{escapeHtml(m.title)}}</div>
                <div class="search-result-dek">${{escapeHtml(m.dek)}}</div>
            </a>
        </div>
    `).join('');
}}

searchInput.addEventListener('input', executeSearch);
categoryFilter.addEventListener('change', executeSearch);
</script>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

DATE_RE = re.compile(r'^(\d{4}-\d{2}-\d{2})_(.+)\.(html?|md)$')

def parse_filename(filename):
    m = DATE_RE.match(filename)
    if m:
        return m.group(1), m.group(2).replace('-', ' ').title()
    return None, os.path.splitext(filename)[0]

def extract_article_meta(filepath, filename):
    date, slug_title = parse_filename(filename)
    title = slug_title
    dek = ""
    tag = "Research"

    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()

    if filepath.endswith('.html') or filepath.endswith('.htm'):
        m = re.search(r'<title>([^<]+)</title>', raw, re.IGNORECASE)
        if m:
            title = m.group(1).strip()
        m = re.search(r'<meta[^>]+name=["\']title["\'][^>]+content=["\']([^"\']+)["\']', raw, re.IGNORECASE)
        if not m:
            m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']title["\']', raw, re.IGNORECASE)
        if m:
            title = m.group(1).strip()
        m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', raw, re.IGNORECASE)
        if not m:
            m = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']description["\']', raw, re.IGNORECASE)
        if m:
            dek = m.group(1).strip()
        m = re.search(r'<meta[^>]+name=["\'](?:tag|category)["\'][^>]+content=["\']([^"\']+)["\']', raw, re.IGNORECASE)
        if m:
            tag = m.group(1).strip()
        if not dek:
            m = re.search(r'<h1[^>]*>.*?</h1>\s*(?:<[^>]+>\s*)*<p[^>]*>(.*?)</p>', raw, re.IGNORECASE | re.DOTALL)
            if m:
                inner = re.sub(r'<[^>]+>', '', m.group(1)).strip()
                dek = inner[:220] + ('…' if len(inner) > 220 else '')
    else:
        lines = raw.splitlines()
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                dek = stripped[:220] + ('…' if len(stripped) > 220 else '')
                break

    return {
        "title": title,
        "dek": dek,
        "date": date or "2026",
        "tag": tag,
        "tags_set": set(t.strip().lower() for t in tag.replace('|', ',').split(',') if t.strip()),
    }


def related_articles(current, all_articles, n=4):
    others = [a for a in all_articles if a['filename'] != current['filename']]
    cur_tags = current.get('tags_set', set())
    def score(a):
        overlap = len(cur_tags & a.get('tags_set', set()))
        return (overlap, a['date'])
    return sorted(others, key=score, reverse=True)[:n]


def build_sidebar_html(related):
    if not related:
        return ''
    items = ''
    for art in related:
        url = art['filename'].replace('.md', '.html')
        tag_display = art['tag'].split('|')[0].strip()
        items += f'''
        <div style="padding: 0.8rem 0; border-bottom: 1px solid var(--gray-200);">
            <a href="{url}" style="text-decoration:none; color:inherit;">
                <span style="font-size:0.65rem; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:var(--geo-copper); display:block; margin-bottom:0.25rem;">{tag_display}</span>
                <div style="font-family:var(--serif); font-size:0.95rem; font-weight:700; line-height:1.3;">{art['title']}</div>
                <div style="font-size:0.72rem; color:var(--gray-400); margin-top:0.2rem;">{art['date']}</div>
            </a>
        </div>'''
    return f'''
    <aside style="width:260px; flex-shrink:0;">
        <div style="border-top:3px solid var(--geo-slate); padding-top:1rem;">
            <div style="font-size:0.68rem; font-weight:700; letter-spacing:0.18em; text-transform:uppercase; color:var(--gray-600); margin-bottom:1rem;">Related Research</div>
            {items}
        </div>
    </aside>'''


def post_process_article(html, sidebar_html, meta):
    import html as html_lib
    title = html_lib.escape(meta.get('title', 'Research Article'))
    dek = html_lib.escape(meta.get('dek', ''))

    html = re.sub(r'<!DOCTYPE html>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'</?html[^>]*>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'</?head[^>]*>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'</?body[^>]*>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<div class="metadata" style="display:none;">.*?</div>', '', html, flags=re.IGNORECASE | re.DOTALL)

    full_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Georgia Mining Research</title>
    <meta name="description" content="{dek}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Inter:wght@300;400;500;600&family=Space+Mono&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="georgia_mining.css">
</head>
<body class="site-wrapper">
    <header class="site-header">
        <a href="index.html" class="site-title"><span class="title-accent">⛏</span> Georgia Mining Research</a>
        <nav style="display:flex;gap:1.5rem;align-items:center;">
            <a href="index.html" style="color:rgba(255,255,255,0.8);text-decoration:none;font-size:0.85rem;">← Research</a>
            <a href="data.html" style="color:rgba(255,255,255,0.8);text-decoration:none;font-size:0.85rem;">Data</a>
            <a href="map.html" style="color:rgba(255,255,255,0.8);text-decoration:none;font-size:0.85rem;">Map</a>
            <a href="analyze.html" style="color:rgba(255,255,255,0.8);text-decoration:none;font-size:0.85rem;">Analyze</a>
        </nav>
    </header>

    <div class="geo-container">
{html}
    </div>

    <footer class="site-footer">
        <span class="footer-name">⛏ Georgia Geological & Mining Research</span>
        <p style="font-size:0.8rem; color:var(--gray-500);">Building a comprehensive open research base on Georgia's geological heritage</p>
    </footer>
</body>
</html>"""
    return full_page


def format_file_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def parse_manifest(data_dir):
    """Parse MANIFEST.md for metadata about downloaded files."""
    manifest_path = os.path.join(data_dir, 'MANIFEST.md')
    entries = {}
    if not os.path.exists(manifest_path):
        return entries
    with open(manifest_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line.startswith('|') or line.startswith('| Filename') or line.startswith('|---'):
                continue
            parts = [p.strip() for p in line.split('|')]
            parts = [p for p in parts if p]  # Remove empty from leading/trailing |
            if len(parts) >= 6:
                entries[parts[0]] = {
                    'source': parts[1],
                    'date': parts[2],
                    'format': parts[3],
                    'size': parts[4],
                    'description': parts[5],
                }
    return entries


def build_data_file_list(data_dir):
    """Walk the data directory and return list of file info dicts."""
    files = []
    if not os.path.isdir(data_dir):
        return files
    for root, dirs, fnames in os.walk(data_dir):
        for fname in fnames:
            if fname.startswith('.') or fname == 'MANIFEST.md':
                continue
            full = os.path.join(root, fname)
            rel = os.path.relpath(full, data_dir)
            size = os.path.getsize(full)
            ext = os.path.splitext(fname)[1].upper().lstrip('.')
            mtime = datetime.fromtimestamp(os.path.getmtime(full)).strftime('%Y-%m-%d')
            files.append({
                'filename': fname,
                'rel_path': rel,
                'size_bytes': size,
                'size_str': format_file_size(size),
                'ext': ext or 'FILE',
                'mtime': mtime,
            })
    files.sort(key=lambda f: f['filename'])
    return files


def build_csv_preview(filepath, max_rows=50, max_top=5):
    """Parse a CSV and return a preview dict with rows and column stats."""
    import csv as csv_mod
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv_mod.DictReader(f)
            columns = reader.fieldnames or []
            all_rows = list(reader)
    except Exception:
        return None

    if not columns or not all_rows:
        return None

    total_rows = len(all_rows)
    preview_rows = all_rows[:max_rows]

    # Column stats
    stats = {}
    for col in columns:
        values = [row.get(col, '') for row in all_rows]
        non_empty = [v for v in values if v and v.strip()]
        nulls = total_rows - len(non_empty)
        unique = len(set(non_empty))

        # Top values
        from collections import Counter
        counts = Counter(non_empty)
        top = counts.most_common(max_top)

        stats[col] = {
            'unique': unique,
            'nulls': nulls,
            'top': top,
        }

    return {
        'columns': columns,
        'rows': [{col: row.get(col, '') for col in columns} for row in preview_rows],
        'total_rows': total_rows,
        'stats': stats,
    }


def build_data_page(data_dir, site_name):
    """Generate the data.html sub-index page content."""
    files = build_data_file_list(data_dir)
    manifest = parse_manifest(data_dir)

    total_size = sum(f['size_bytes'] for f in files)
    formats = set(f['ext'] for f in files)

    # Stats
    data_stats_html = f"""
    <div class="data-stats">
        <div class="dst"><div class="dst-val">{len(files)}</div><div class="dst-lbl">Files</div></div>
        <div class="dst"><div class="dst-val">{format_file_size(total_size)}</div><div class="dst-lbl">Total Size</div></div>
        <div class="dst"><div class="dst-val">{len(formats)}</div><div class="dst-lbl">Formats</div></div>
    </div>
"""

    csv_previews = {}

    if not files:
        data_cards_html = '<p class="no-data-msg">No datasets downloaded yet. Run the research task to start acquiring data.</p>'
    else:
        cards = ''
        for f in files:
            m = manifest.get(f['filename'], {})
            source = m.get('source', '')
            desc = m.get('description', '')
            date = m.get('date', f['mtime'])
            file_id = f['filename'].replace('.', '_').replace(' ', '_')

            source_html = ''
            if source:
                trunc = source[:60] + ('...' if len(source) > 60 else '')
                source_html = f'<div class="fsource"><a href="{source}" target="_blank">{trunc}</a></div>'

            desc_html = f'<div class="fdesc">{desc}</div>' if desc else ''

            # Build preview drawer content
            ext_lower = f['ext'].lower()
            if ext_lower == 'pdf':
                drawer_content = f'<iframe class="pdf-embed" data-src="data/{f["rel_path"]}" title="Preview {f["filename"]}"></iframe>'
            elif ext_lower == 'csv':
                csv_path = os.path.join(data_dir, f['rel_path'])
                preview = build_csv_preview(csv_path)
                if preview:
                    csv_previews[f['filename']] = preview
                drawer_content = f'<div id="csv-preview-{f["filename"]}">Loading CSV preview...</div>'
            else:
                drawer_content = f'<p style="color:var(--gray-500); text-align:center; padding:2rem; font-style:italic;">Preview not available for {f["ext"]} files. <a href="data/{f["rel_path"]}" download style="color:var(--geo-green);">Download file</a></p>'

            csv_attr = f' data-csv="{f["filename"]}"' if ext_lower == 'csv' else ''

            cards += f"""
            <div class="data-file-card" id="card-{file_id}"{csv_attr}>
                <div class="file-card-header" onclick="togglePreview('{file_id}')">
                    <span class="fmt-badge">{f['ext']}</span>
                    <div class="file-card-info">
                        <div class="fname"><a href="data/{f['rel_path']}" download onclick="event.stopPropagation();">{f['filename']}</a></div>
                        {desc_html}
                        {source_html}
                    </div>
                    <span class="fsize">{f['size_str']}</span>
                    <span class="fdate">{date}</span>
                    <button class="preview-btn" onclick="event.stopPropagation(); togglePreview('{file_id}');">Preview</button>
                </div>
                <div class="preview-drawer">
                    {drawer_content}
                </div>
            </div>"""

        data_cards_html = f'<div class="data-file-list">{cards}</div>'

    return DATA_PAGE_TEMPLATE.format(
        site_name=site_name,
        data_stats_html=data_stats_html,
        data_cards_html=data_cards_html,
        csv_previews_json=json.dumps(csv_previews, default=str),
    )



def build_stats_banner(articles, data_files, data_dir=None):
    n_articles = len(articles)
    categories = set()
    for a in articles:
        for t in a.get('tags_set', set()):
            categories.add(t)
    n_categories = len(categories)
    n_datasets = len(data_files)
    total_size = '0 B'
    if data_dir and os.path.isdir(data_dir):
        total = sum(os.path.getsize(os.path.join(r, f))
                    for r, _, fs in os.walk(data_dir)
                    for f in fs if not f.startswith('.') and f != 'MANIFEST.md')
        total_size = format_file_size(total)

    return f"""
    <div class="stats-banner">
        <div class="stat">
            <div class="stat-val">{n_articles}</div>
            <div class="stat-lbl">Research Articles</div>
        </div>
        <div class="stat">
            <div class="stat-val">{n_datasets}</div>
            <div class="stat-lbl">Datasets</div>
        </div>
        <div class="stat">
            <div class="stat-val">{total_size}</div>
            <div class="stat-lbl">Data Downloaded</div>
        </div>
        <div class="stat">
            <div class="stat-val">{n_categories}</div>
            <div class="stat-lbl">Categories</div>
        </div>
    </div>
"""


def build_data_section(data_files):
    if not data_files:
        return ''

    items = ''
    for f in data_files[:10]:
        ext = os.path.splitext(f)[1].upper().lstrip('.')
        if not ext:
            ext = 'FILE'
        items += f'''
            <li>
                <a href="data.html" style="text-decoration:none; color:inherit; display:flex; align-items:center; gap:0.75rem; width:100%;">
                    <span class="data-icon">{ext}</span>
                    <span class="data-name">{f}</span>
                </a>
            </li>'''

    more_link = f'<p style="margin-top:1rem; text-align:right;"><a href="data.html" style="color:var(--geo-green); font-weight:600; font-size:0.85rem;">Browse all {len(data_files)} files →</a></p>' if len(data_files) > 10 else ''

    return f"""
    <div class="data-section">
        <div class="section-header">
            <span><a href="data.html" style="text-decoration:none; color:inherit;">Data Repository</a></span>
            <span class="count"><a href="data.html" style="text-decoration:none; color:inherit;">{len(data_files)} files</a></span>
        </div>
        <ul class="data-list">
            {items}
        </ul>
        {more_link}
    </div>
"""


def build_article_listing(articles):
    if not articles:
        return '<p style="color:var(--gray-500); font-style:italic; text-align:center; padding: 4rem 0;">No research articles published yet. Run the research task to start building the knowledge base.</p>'

    sorted_arts = sorted(articles, key=lambda a: a['date'], reverse=True)

    def article_url(art):
        return art['filename'].replace('.md', '.html')

    html = f"""
    <div class="section-header">
        <span>Research Articles</span>
        <span class="count">{len(sorted_arts)} articles</span>
    </div>
    <div class="article-grid">
"""
    for art in sorted_arts:
        html += f"""
        <div class="article-card">
            <a href="{article_url(art)}">
                <span class="card-tag">{art['tag']}</span>
                <div class="card-headline">{art['title']}</div>
                <div class="card-dek">{art['dek']}</div>
                <div class="card-date">{art['date']}</div>
            </a>
        </div>
"""
    html += "    </div>\n"
    return html


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# MAP PAGE
# ---------------------------------------------------------------------------
MAP_PAGE_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Map — {site_name}</title>
<link rel="stylesheet" href="georgia_mining.css">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<style>
  #map {{ height: calc(100vh - 200px); min-height: 500px; width: 100%; border-radius: 8px; border: 2px solid var(--geo-copper); }}
  .map-container {{ max-width: 1300px; margin: 0 auto; padding: 1.5rem 2rem 3rem; }}
  .map-controls {{ display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1rem; align-items: center; }}
  .layer-toggle {{ display: flex; align-items: center; gap: 0.4rem; padding: 0.4rem 0.8rem; background: var(--gray-800); border-radius: 6px; font-size: 0.8rem; color: var(--gray-300); cursor: pointer; border: 1px solid var(--gray-700); transition: all 0.2s; }}
  .layer-toggle:hover {{ border-color: var(--geo-copper); }}
  .layer-toggle.active {{ border-color: var(--geo-green); color: var(--geo-green); }}
  .layer-toggle input {{ accent-color: var(--geo-green); }}
  .map-stats {{ display: flex; gap: 2rem; margin-bottom: 1.5rem; }}
  .map-stat {{ text-align: center; }}
  .map-stat-val {{ font-family: var(--font-display); font-size: 1.5rem; color: var(--geo-gold); }}
  .map-stat-lbl {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--gray-500); }}
  .no-geo-msg {{ text-align: center; padding: 4rem 2rem; color: var(--gray-500); font-style: italic; }}
  .no-geo-msg h3 {{ color: var(--gray-400); font-family: var(--font-display); }}
</style>
</head>
<body class="site-wrapper" style="overflow: hidden;">
<header class="site-header">
    <a href="index.html" class="site-title"><span class="title-accent">⛏</span> {site_name}</a>
    <nav style="display: flex; gap: 1.5rem;">
        <a href="index.html" style="color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.06em;">Research</a>
        <a href="data.html" style="color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.06em;">Data</a>
        <a href="map.html" style="color: var(--geo-gold); text-decoration: none; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 700;">Map</a>
        <a href="analyze.html" style="color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.06em;">Analyze</a>
    </nav>
</header>
{map_content}

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const mapData = {map_data_json};

if (mapData.layers.length > 0) {{
    const map = L.map('map').setView([32.7, -83.5], 7);
    L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
        attribution: '© OpenStreetMap contributors © CARTO',
        subdomains: 'abcd', maxZoom: 19
    }}).addTo(map);

    const colors = ['#d4a017', '#cd7f32', '#4a9e6e', '#6fa8dc', '#e06c75', '#c678dd', '#e5c07b', '#61afef'];
    const overlayMaps = {{}};

    mapData.layers.forEach((layer, i) => {{
        const color = colors[i % colors.length];
        const group = L.layerGroup();

        layer.features.forEach(f => {{
            const lat = f.lat, lon = f.lon;
            if (lat && lon && !isNaN(lat) && !isNaN(lon)) {{
                const popupLines = Object.entries(f.properties || {{}})
                    .filter(([k,v]) => v && k !== 'lat' && k !== 'lon' && k !== 'latitude' && k !== 'longitude')
                    .slice(0, 10)
                    .map(([k,v]) => `<b>${{k}}</b>: ${{v}}`)
                    .join('<br>');
                L.circleMarker([lat, lon], {{
                    radius: 5, fillColor: color, color: '#222', weight: 1, opacity: 0.9, fillOpacity: 0.75
                }}).bindPopup(`<div style="max-width:250px;font-size:12px;">${{popupLines || 'No details'}}</div>`).addTo(group);
            }}
        }});
        group.addTo(map);
        overlayMaps[`<span style="color:${{color}};">&#9679;</span> ${{layer.name}} (${{layer.count.toLocaleString()}})`] = group;
    }});

    L.control.layers(null, overlayMaps, {{collapsed: false}}).addTo(map);

    // Fit bounds to all features
    const allPoints = [];
    mapData.layers.forEach(l => l.features.forEach(f => {{
        if (f.lat && f.lon && !isNaN(f.lat) && !isNaN(f.lon)) allPoints.push([f.lat, f.lon]);
    }}));
    if (allPoints.length > 1) map.fitBounds(allPoints, {{ padding: [30, 30] }});
}}
</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# ANALYSIS PAGE
# ---------------------------------------------------------------------------
ANALYSIS_PAGE_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Analyze — {site_name}</title>
<link rel="stylesheet" href="georgia_mining.css">
<style>
  .analyze-container {{ max-width: 1300px; margin: 0 auto; padding: 1.5rem 2rem 3rem; }}
  .query-section {{ background: var(--gray-800); border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem; border: 1px solid var(--gray-700); }}
  .file-select {{ background: var(--gray-900); color: var(--gray-200); border: 1px solid var(--gray-600); border-radius: 6px; padding: 0.6rem 1rem; font-size: 0.9rem; width: 100%; margin-bottom: 1rem; }}
  .file-select:focus {{ outline: none; border-color: var(--geo-gold); }}
  .sql-input {{ width: 100%; background: var(--gray-900); color: var(--geo-gold); border: 1px solid var(--gray-600); border-radius: 6px; padding: 0.8rem 1rem; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; resize: vertical; min-height: 60px; }}
  .sql-input:focus {{ outline: none; border-color: var(--geo-gold); }}
  .sql-input::placeholder {{ color: var(--gray-600); }}
  .btn-row {{ display: flex; gap: 0.8rem; margin-top: 0.8rem; flex-wrap: wrap; }}
  .btn {{ padding: 0.5rem 1.2rem; border-radius: 6px; font-size: 0.8rem; cursor: pointer; border: none; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600; transition: all 0.2s; }}
  .btn-primary {{ background: var(--geo-green); color: #fff; }}
  .btn-primary:hover {{ filter: brightness(1.15); }}
  .btn-secondary {{ background: var(--gray-700); color: var(--gray-300); }}
  .btn-secondary:hover {{ background: var(--gray-600); }}
  .results-section {{ background: var(--gray-800); border-radius: 8px; padding: 1.5rem; border: 1px solid var(--gray-700); }}
  .results-info {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; color: var(--gray-400); font-size: 0.85rem; }}
  .results-table-wrap {{ overflow-x: auto; max-width: 100%; -webkit-overflow-scrolling: touch; max-height: 600px; overflow-y: auto; }}
  .results-table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
  .results-table th {{ position: sticky; top: 0; background: var(--gray-900); color: var(--geo-gold); padding: 0.6rem 0.8rem; text-align: left; border-bottom: 2px solid var(--geo-copper); cursor: pointer; white-space: nowrap; user-select: none; }}
  .results-table th:hover {{ color: #fff; }}
  .results-table td {{ padding: 0.5rem 0.8rem; border-bottom: 1px solid var(--gray-700); color: var(--gray-200); white-space: normal; max-width: 300px; word-wrap: break-word; line-height: 1.4; }}
  .results-table tr:hover td {{ background: rgba(212,160,23,0.05); }}
  .error-msg {{ color: #e06c75; background: rgba(224,108,117,0.1); padding: 0.8rem 1rem; border-radius: 6px; font-size: 0.85rem; margin-top: 1rem; }}
  .helper-text {{ color: var(--gray-500); font-size: 0.8rem; margin-top: 0.5rem; }}
  .helper-text code {{ color: var(--geo-gold); background: var(--gray-900); padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 0.78rem; }}
  .quick-queries {{ display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.6rem; }}
  .quick-q {{ padding: 0.3rem 0.6rem; background: var(--gray-900); color: var(--gray-400); border: 1px solid var(--gray-700); border-radius: 4px; font-size: 0.72rem; cursor: pointer; font-family: 'JetBrains Mono', monospace; transition: all 0.2s; }}
  .quick-q:hover {{ border-color: var(--geo-gold); color: var(--geo-gold); }}
  .dataset-info {{ background: var(--gray-900); border-radius: 6px; padding: 0.8rem 1rem; margin-bottom: 1rem; display: none; }}
  .dataset-info .cols {{ display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.5rem; }}
  .dataset-info .col-tag {{ padding: 0.2rem 0.5rem; background: var(--gray-800); color: var(--geo-copper); border-radius: 3px; font-size: 0.75rem; font-family: monospace; }}
</style>
</head>
<body class="site-wrapper">
<header class="site-header">
    <a href="index.html" class="site-title"><span class="title-accent">⛏</span> {site_name}</a>
    <nav style="display: flex; gap: 1.5rem;">
        <a href="index.html" style="color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.06em;">Research</a>
        <a href="data.html" style="color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.06em;">Data</a>
        <a href="map.html" style="color: rgba(255,255,255,0.8); text-decoration: none; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.06em;">Map</a>
        <a href="analyze.html" style="color: var(--geo-gold); text-decoration: none; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 700;">Analyze</a>
    </nav>
</header>

<div class="analyze-container">
    <h1 style="font-family: var(--font-display); font-size: 2rem; color: var(--gray-100); margin-bottom: 0.5rem;">Data Analysis Tool</h1>
    <div style="width: 80px; height: 3px; background: var(--geo-gold); margin-bottom: 1rem;"></div>
    <p style="color: var(--gray-400); margin-bottom: 1.5rem;">Query any CSV dataset using SQL. Select a file, write a query, and explore the data.</p>

    <div class="query-section">
        <select id="file-select" class="file-select" onchange="loadDataset()">
            <option value="">— Select a dataset —</option>
            {csv_options}
        </select>

        <div id="dataset-info" class="dataset-info">
            <span style="color:var(--gray-400);font-size:0.8rem;">Columns:</span>
            <div class="cols" id="col-tags"></div>
        </div>

        <textarea id="sql-input" class="sql-input" placeholder="SELECT * FROM data WHERE code_list LIKE '%AU%' LIMIT 50" rows="2"></textarea>
        <div class="helper-text">Table name is <code>data</code>. Use standard SQL syntax. Examples:</div>
        <div class="quick-queries" id="quick-queries"></div>

        <div class="btn-row">
            <button class="btn btn-primary" onclick="runQuery()">▶ Run Query</button>
            <button class="btn btn-secondary" onclick="exportCSV()">↓ Export CSV</button>
            <button class="btn btn-secondary" onclick="document.getElementById('sql-input').value='SELECT * FROM data LIMIT 100'; runQuery();">Show All</button>
        </div>
    </div>

    <div class="results-section">
        <div class="results-info">
            <span id="results-count">Select a dataset to begin.</span>
            <span id="query-time"></span>
        </div>
        <div class="results-table-wrap" id="results-wrap">
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/alasql@4/dist/alasql.min.js"></script>
<script>
const csvData = {csv_data_json};
let currentData = null;
let lastResults = null;

window.onload = function() {{
    const sel = document.getElementById('file-select');
    if (sel.options.length > 1 && !sel.value) {{
        sel.selectedIndex = 1;
        loadDataset();
    }}
}};

function loadDataset() {{
    const sel = document.getElementById('file-select');
    const fname = sel.value;
    const info = document.getElementById('dataset-info');
    const colTags = document.getElementById('col-tags');
    const quickQ = document.getElementById('quick-queries');

    if (!fname || !csvData[fname]) {{
        info.style.display = 'none';
        currentData = null;
        return;
    }}

    const ds = csvData[fname];
    currentData = ds.rows;

    // Load into AlaSQL
    alasql('DROP TABLE IF EXISTS data');
    alasql('CREATE TABLE data');
    alasql.tables.data.data = currentData;

    // Show column tags
    info.style.display = 'block';
    colTags.innerHTML = ds.columns.map(c => `<span class="col-tag">${{c}}</span>`).join('');

    // Quick queries
    const queries = [
        `SELECT * FROM data LIMIT 50`,
        `SELECT COUNT(*) AS total FROM data`,
    ];
    if (ds.columns.length > 1) {{
        const col = ds.columns[1];
        queries.push(`SELECT ${{col}}, COUNT(*) AS n FROM data GROUP BY ${{col}} ORDER BY n DESC LIMIT 20`);
    }}
    quickQ.innerHTML = queries.map(q =>
        `<span class="quick-q" onclick="document.getElementById('sql-input').value=this.textContent;runQuery();">${{q}}</span>`
    ).join('');

    document.getElementById('sql-input').value = `SELECT * FROM data LIMIT 50`;
    document.getElementById('results-count').textContent = `Loaded ${{currentData.length}} rows · ${{ds.columns.length}} columns`;
    runQuery();
}}

function runQuery() {{
    if (!currentData) {{ alert('Select a dataset first.'); return; }}
    const sql = document.getElementById('sql-input').value.trim();
    if (!sql) return;

    const t0 = performance.now();
    try {{
        const res = alasql(sql);
        const elapsed = ((performance.now() - t0) / 1000).toFixed(3);
        lastResults = res;

        if (!Array.isArray(res) || res.length === 0) {{
            document.getElementById('results-wrap').innerHTML = '<p style="color:var(--gray-500);text-align:center;padding:2rem;">No results.</p>';
            document.getElementById('results-count').textContent = '0 rows';
            document.getElementById('query-time').textContent = `${{elapsed}}s`;
            return;
        }}

        const cols = Object.keys(res[0]);
        let html = '<table class="results-table"><thead><tr>';
        cols.forEach(c => {{ html += `<th>${{c}}</th>`; }});
        html += '</tr></thead><tbody>';
        res.forEach(row => {{
            html += '<tr>';
            cols.forEach(c => {{
                const v = row[c] != null ? row[c] : '';
                html += `<td title="${{String(v).replace(/"/g, '&quot;')}}">${{v}}</td>`;
            }});
            html += '</tr>';
        }});
        html += '</tbody></table>';

        document.getElementById('results-wrap').innerHTML = html;
        document.getElementById('results-count').textContent = `${{res.length}} row${{res.length !== 1 ? 's' : ''}}`;
        document.getElementById('query-time').textContent = `${{elapsed}}s`;
    }} catch(e) {{
        document.getElementById('results-wrap').innerHTML = `<div class="error-msg">SQL Error: ${{e.message}}</div>`;
    }}
}}

function exportCSV() {{
    if (!lastResults || !lastResults.length) {{ alert('Run a query first.'); return; }}
    const cols = Object.keys(lastResults[0]);
    let csv = cols.join(',') + '\\n';
    lastResults.forEach(row => {{
        csv += cols.map(c => {{
            let v = row[c] != null ? String(row[c]) : '';
            if (v.includes(',') || v.includes('"') || v.includes('\\n')) v = '"' + v.replace(/"/g, '""') + '"';
            return v;
        }}).join(',') + '\\n';
    }});
    const blob = new Blob([csv], {{ type: 'text/csv' }});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'query_results.csv'; a.click();
    URL.revokeObjectURL(url);
}}

// Keyboard shortcut: Ctrl/Cmd+Enter to run query
document.getElementById('sql-input').addEventListener('keydown', function(e) {{
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {{ e.preventDefault(); runQuery(); }}
}});
</script>
</body>
</html>
"""


def build_map_data(data_dir):
    """Scan data dir for mappable files and return a dict for the map page."""
    import csv as csv_mod
    layers = []
    lat_names = {'latitude', 'lat', 'y', 'lat_dd', 'latitude_dd', 'declatitude'}
    lon_names = {'longitude', 'lon', 'lng', 'x', 'long', 'lon_dd', 'longitude_dd', 'declongitude'}

    if not data_dir or not os.path.isdir(data_dir):
        return {'layers': []}

    for root, dirs, files in os.walk(data_dir):
        for fname in files:
            fpath = os.path.join(root, fname)
            ext = fname.rsplit('.', 1)[-1].lower() if '.' in fname else ''

            # GeoJSON files
            if ext in ('geojson', 'json'):
                try:
                    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                        data = json.load(f)
                    if data.get('type') in ('FeatureCollection', 'Feature') or 'features' in data:
                        features = data.get('features', [data] if data.get('type') == 'Feature' else [])
                        mapped = []
                        for feat in features[:2000]:
                            geom = feat.get('geometry', {})
                            coords = geom.get('coordinates', [])
                            if geom.get('type') == 'Point' and len(coords) >= 2:
                                mapped.append({
                                    'lat': coords[1], 'lon': coords[0],
                                    'properties': feat.get('properties', {})
                                })
                        if mapped:
                            layers.append({'name': fname, 'count': len(mapped), 'features': mapped})
                except Exception:
                    pass

            # CSV files with lat/lon columns
            elif ext == 'csv':
                try:
                    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                        reader = csv_mod.DictReader(f)
                        cols = [c.lower().strip() for c in (reader.fieldnames or [])]
                        lat_col = next((c for c in reader.fieldnames if c.lower().strip() in lat_names), None)
                        lon_col = next((c for c in reader.fieldnames if c.lower().strip() in lon_names), None)
                        if lat_col and lon_col:
                            mapped = []
                            for row in reader:
                                try:
                                    lat = float(row[lat_col])
                                    lon = float(row[lon_col])
                                    if -90 <= lat <= 90 and -180 <= lon <= 180:
                                        mapped.append({
                                            'lat': lat, 'lon': lon,
                                            'properties': {k: v for k, v in row.items() if k != lat_col and k != lon_col}
                                        })
                                except (ValueError, TypeError):
                                    pass
                                if len(mapped) >= 5000:
                                    break
                            if mapped:
                                layers.append({'name': fname, 'count': len(mapped), 'features': mapped})
                except Exception:
                    pass

    return {'layers': layers}


def build_map_page(data_dir, site_name):
    """Generate the map.html page."""
    map_data = build_map_data(data_dir)

    if map_data['layers']:
        map_content = '<div id="map" style="height: calc(100vh - 72px); width: 100%;"></div>'
    else:
        map_content = """
        <div class="map-container" style="max-width: 800px; margin: 0 auto; padding: 4rem 2rem;">
            <div class="no-geo-msg">
                <h3>No Mappable Data Yet</h3>
                <p>The map will auto-populate when datasets with geographic coordinates are added.<br>
                Supported: GeoJSON files, CSVs with latitude/longitude columns.</p>
                <p style="margin-top:1rem;"><a href="data.html" style="color:var(--geo-green);">View available datasets →</a></p>
            </div>
        </div>
        """

    return MAP_PAGE_TEMPLATE.format(
        site_name=site_name,
        map_content=map_content,
        map_data_json=json.dumps(map_data, default=str),
    )


def build_analysis_page(data_dir, site_name):
    """Generate the analyze.html page with SQL querying."""
    import csv as csv_mod
    csv_data = {}
    csv_options = ''

    if data_dir and os.path.isdir(data_dir):
        for root, dirs, files in os.walk(data_dir):
            for fname in sorted(files):
                if not fname.lower().endswith('.csv'):
                    continue
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                        reader = csv_mod.DictReader(f)
                        columns = reader.fieldnames or []
                        rows = list(reader)
                    if columns and rows:
                        csv_data[fname] = {
                            'columns': columns,
                            'rows': [{col: row.get(col, '') for col in columns} for row in rows],
                        }
                        csv_options += f'<option value="{fname}">{fname} ({len(rows):,} rows, {len(columns)} cols)</option>\n'
                except Exception:
                    pass

    if not csv_options:
        csv_options = '<option value="" disabled>No CSV files available</option>'

    return ANALYSIS_PAGE_TEMPLATE.format(
        site_name=site_name,
        csv_options=csv_options,
        csv_data_json=json.dumps(csv_data, default=str),
    )


def main():
    parser = argparse.ArgumentParser(description="Georgia Mining Research static site generator")
    parser.add_argument("--source", required=True, help="Directory of HTML/MD article files")
    parser.add_argument("--s3-bucket", required=False, help="S3 path, e.g. s3://bucket/path/")
    parser.add_argument("--data-dir", required=False, help="Directory of downloaded data files to catalog")
    parser.add_argument("--site-name", default="Georgia Geological & Mining Research", help="Site name")
    parser.add_argument("--site-tagline", default="Building a comprehensive research base on Georgia's geological heritage and mineral wealth", help="Tagline")
    args = parser.parse_args()

    source_dir = os.path.abspath(args.source)
    if not os.path.isdir(source_dir):
        print(f"Error: source directory '{source_dir}' does not exist.")
        sys.exit(1)

    build_dir = os.path.join(os.path.dirname(__file__), "build_out_georgia_mining")
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.makedirs(build_dir)

    articles = []
    data_files = []

    # Copy CSS
    css_src = os.path.join(os.path.dirname(__file__), "georgia_mining.css")
    if os.path.exists(css_src):
        shutil.copy2(css_src, os.path.join(build_dir, "georgia_mining.css"))
        print(f"  → Copied georgia_mining.css to {build_dir}/")
    else:
        print(f"  ⚠  georgia_mining.css not found at {css_src}")

    # Copy images if any
    images_src = os.path.join(source_dir, "images")
    images_dst = os.path.join(build_dir, "images")
    if os.path.isdir(images_src):
        shutil.copytree(images_src, images_dst, dirs_exist_ok=True)
        print(f"  → Copied images/ to {images_dst}/")

    # Catalog data files
    if args.data_dir and os.path.isdir(args.data_dir):
        data_dst = os.path.join(build_dir, "data")
        shutil.copytree(args.data_dir, data_dst, dirs_exist_ok=True)
        for root, dirs, files in os.walk(args.data_dir):
            for f in files:
                if not f.startswith('.'):
                    rel = os.path.relpath(os.path.join(root, f), args.data_dir)
                    data_files.append(rel)
        data_files.sort()
        print(f"  → Cataloged {len(data_files)} data file(s)")

    # Process articles
    for fname in sorted(os.listdir(source_dir)):
        if not (fname.endswith('.html') or fname.endswith('.htm') or fname.endswith('.md')):
            continue
        if fname.startswith('_') or fname.startswith('.'):
            continue

        src_path = os.path.join(source_dir, fname)
        meta = extract_article_meta(src_path, fname)
        meta['filename'] = fname
        meta['src_path'] = src_path
        articles.append(meta)

    # Write articles
    for meta in articles:
        fname = meta['filename']
        src_path = meta['src_path']

        if fname.endswith('.md'):
            with open(src_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            if HAS_MARKDOWN:
                md = markdown.Markdown(extensions=['fenced_code', 'tables', 'sane_lists'])
                body = md.convert(md_content)
            else:
                body = "<pre>" + md_content.replace("&","&amp;").replace("<","&lt;") + "</pre>"
            html = f"<main class='geo-body'>{body}</main>"
            out_name = fname.replace('.md', '.html')
            meta['filename'] = out_name
        else:
            with open(src_path, 'r', encoding='utf-8') as f:
                html = f.read()
            out_name = fname

        related = related_articles(meta, articles)
        sidebar_html = build_sidebar_html(related)
        html = post_process_article(html, sidebar_html, meta)

        with open(os.path.join(build_dir, out_name), 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"  + {fname}  →  \"{meta['title']}\"  (related: {len(related)})")

    # Build search index
    search_index = [
        {
            "title": a["title"],
            "dek": a["dek"],
            "tag": a["tag"],
            "date": a["date"],
            "path": a["filename"].replace('.md', '.html'),
        }
        for a in articles
    ]

    today = datetime.now().strftime("%B %-d, %Y")

    # Build index.html
    data_dir_abs = os.path.abspath(args.data_dir) if args.data_dir else None
    stats_banner_html = build_stats_banner(articles, data_files, data_dir_abs)
    data_section_html = build_data_section(data_files)
    article_listing_html = build_article_listing(articles)

    index_html = INDEX_TEMPLATE.format(
        site_name=args.site_name,
        site_tagline=args.site_tagline,
        today=today,
        stats_banner_html=stats_banner_html,
        data_section_html=data_section_html,
        article_listing_html=article_listing_html,
        search_index_json=json.dumps(search_index),
    )
    with open(os.path.join(build_dir, "index.html"), 'w', encoding='utf-8') as f:
        f.write(index_html)

    with open(os.path.join(build_dir, "search_index.json"), 'w', encoding='utf-8') as f:
        json.dump(search_index, f)

    # Build data.html
    if data_dir_abs and os.path.isdir(data_dir_abs):
        data_page = build_data_page(data_dir_abs, args.site_name)
        with open(os.path.join(build_dir, "data.html"), 'w', encoding='utf-8') as f:
            f.write(data_page)
        print(f"  → Built data.html with {len(data_files)} file(s)")

    # Build map.html
    map_page = build_map_page(data_dir_abs, args.site_name)
    with open(os.path.join(build_dir, "map.html"), 'w', encoding='utf-8') as f:
        f.write(map_page)
    print(f"  → Built map.html")

    # Build analyze.html
    analysis_page = build_analysis_page(data_dir_abs, args.site_name)
    with open(os.path.join(build_dir, "analyze.html"), 'w', encoding='utf-8') as f:
        f.write(analysis_page)
    print(f"  → Built analyze.html")

    print(f"\nBuilt {len(articles)} article(s) + data.html + map.html + analyze.html → {build_dir}/")

    if args.s3_bucket:
        bucket = args.s3_bucket.rstrip('/') + '/'
        print(f"\nDeploying to {bucket} ...")
        cmd = ["aws", "s3", "sync", build_dir, bucket, "--delete"]
        try:
            subprocess.run(cmd, check=True)
            print("Successfully published to S3.")
        except subprocess.CalledProcessError as e:
            print(f"Error deploying to S3: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
