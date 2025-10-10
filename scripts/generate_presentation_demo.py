#!/usr/bin/env python3
import asyncio
import sys
from pathlib import Path


# Ensure the src/ package directory is on the path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from services.utils import generate_presentation_pdf  # type: ignore

async def main() -> None:
    # Realistic demo context matching services/utils/template.html
    context = {
        "title": "Water Heater Replacement Options",
        "subtitle": "Homeowner: Jane Doe • 123 Maple St • Assessed: 2025-10-13",
        "level_1": {
            "time": 2.0,
            "entry": (
                "Flush tank to remove sediment and restore partial efficiency. "
                "Replace anode rod to slow corrosion and extend tank life. "
                "Test and replace T&P valve as needed to ensure safety compliance. "
                "Inspect burner assembly; clean debris and verify flame quality. "
            ),
        },
        "level_2": {
            "time": 2.5,
            "entry": (
                "Replace with 40-gallon standard efficiency gas heater (like-for-like). "
                "Includes removal/haul-away of old unit and all disposal fees. "
                "Bring up to current code: seismic strapping and venting as needed. "
            ),
        },
        "level_3": {
            "time": 3.0,
            "entry": (
                "Upgrade to 50-gallon high-recovery model for faster reheat times. "
                "Add thermal expansion tank to protect plumbing and fixtures. "
                "Replace aging flue components; confirm draft and clearances. "
                "Install new water shutoff, dielectric unions, and supply lines. "
            ),
        },
        "level_4": {
            "time": 3.5,
            "entry": (
                "Install 50-gallon high-efficiency hybrid heat-pump water heater. "
                "Significantly reduces energy usage and operating costs. "
                "Integrate smart leak sensor with automatic shutoff capability. "
                "Dedicated drain for condensate management and pan overflow. "
            ),
        },
    }

    output_path = ROOT / "presentation.pdf"
    await generate_presentation_pdf(context, output_path)
    print(f"Saved PDF → {output_path}")


if __name__ == "__main__":
    asyncio.run(main())


