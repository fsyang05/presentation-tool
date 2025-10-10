from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Mapping, Any

from jinja2 import Environment, FileSystemLoader, select_autoescape
from playwright.async_api import async_playwright

TEMPLATES_DIR = Path(__file__).parent
TEMPLATE_FILE = TEMPLATES_DIR / "template.html"

def render_template(context: Mapping[str, Any]) -> str:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("./presentation/template.html")
    # Ensure static_base is available to resolve local assets like logo-wahl.png
    # Use file:// scheme so Chromium can load the local image
    ctx = dict(context)
    ctx.setdefault("static_base", "file://" + TEMPLATES_DIR.as_posix() + "/")
    return template.render(**ctx)

async def html_to_pdf(html_content: str, output_path: Path) -> Path:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        # Wait for network to be idle to ensure images load
        await page.set_content(html_content, wait_until="networkidle")
        await page.wait_for_function("() => Array.from(document.images).every(img => img.complete)")
        await page.pdf(
            path=str(output_path),
            format="A4",
            margin={"top": "20mm", "right": "12mm", "bottom": "20mm", "left": "12mm"},
            print_background=True,
        )
        await browser.close()
    return output_path

async def generate_presentation_pdf(context: Mapping[str, Any], output_path: Path) -> Path:
    html = render_template(context)
    return await html_to_pdf(html, output_path)