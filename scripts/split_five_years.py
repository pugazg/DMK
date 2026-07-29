#!/usr/bin/env python3
"""Split Five_years.txt into one Markdown file per contents/index entry.

The printed page number in the contents is one less than the source image number:
printed page 18 begins at `DMK 5 YEARS ACHIEVEMENTS 19.jpg`.
"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "Five_years.txt"
OUTPUT = ROOT / "five-years"


@dataclass(frozen=True)
class Entry:
    page: int
    title: str
    category: str
    byline: str = ""


ENTRIES = [
    Entry(18, "தமிழர் வரலாற்றில் ஒரு திருப்புமுனை", "ஆளுமைகளின் பார்வையில்", "ஆர். பாலகிருஷ்ணன், இ.ஆ.ப., (ஓய்வு)"),
    Entry(26, "நீதிக்கட்சிக் காலம் முதல் நீண்டுவரும் திராவிட இயக்கத் தன்மானத் தமிழ்ச் சங்கிலி", "ஆளுமைகளின் பார்வையில்", "புலவர் முத்து. வாலாசி"),
    Entry(32, "நகர்ப்புற வளர்ச்சிக்கு இணையான சமச்சீர் ஊரக வளர்ச்சி", "ஆளுமைகளின் பார்வையில்", "மூ. அப்பணசாமி"),
    Entry(38, "பொருளாதார வளர்ச்சியில் முதலிடம்", "ஆளுமைகளின் பார்வையில்", "எம். ரமேஷ்"),
    Entry(44, "புண்ணியம் செய்வார்க்கு பூ உள — இந்து சமய அறநிலையத்துறை", "ஆளுமைகளின் பார்வையில்", "ஸ்ரீராம் சர்மா"),
    Entry(50, "குறையொன்றுமில்லை — முதல்வரின் முகவரித்துறை", "ஆளுமைகளின் பார்வையில்", "பெ. அரவிந்தன்"),
    Entry(54, "மாற்றுத்திறனாளிகளின் மனம் குளிர்விக்கும் அரசு", "ஆளுமைகளின் பார்வையில்", "இலட்சுமி பாலகிருஷ்ணன்"),
    Entry(58, "பெண்மை வெல்க என்று கூத்திடுவோம்", "ஆளுமைகளின் பார்வையில்", "முனைவர் ந. கவிதா"),
    Entry(64, "நிற்க அதற்குத் தக — பள்ளிக்கல்வித் துறை", "ஆளுமைகளின் பார்வையில்", "முனைவர் தீ. பரமேசுவரி"),
    Entry(72, "இந்தியாவிற்கு முன்னோடியான திராவிட மாடல் அரசின் திட்டங்கள்", "ஆளுமைகளின் பார்வையில்", "வெற்றிச்செல்வன்"),
    Entry(78, "கொள்கை வழி அரசு!", "ஆளுமைகளின் பார்வையில்", "சே.மெ. மதிவதனி"),
    Entry(84, "இளைஞர் ஏக்கம் உடைத்து ஊக்கம் படைத்த திராவிட மாடல்!", "ஆளுமைகளின் பார்வையில்", "இந்திரகுமார் தேரடி"),
    Entry(90, "விளையாட்டிலும் சமூக நீதி: எல்லாருக்கும் எல்லாம்!", "ஆளுமைகளின் பார்வையில்", "தினேஷ் அகிரா"),
    Entry(96, "சமூகநீதியின் சாதனைகள்", "ஆளுமைகளின் பார்வையில்", "சிவக்குமார் முத்தையா"),
    Entry(103, "தமிழ்நாடு முதலமைச்சர் — மு.க. ஸ்டாலின்", "துறை வாரியாக சாதனைகள்"),
    Entry(131, "நீர்வளத்துறை — துரைமுருகன்", "துறை வாரியாக சாதனைகள்"),
    Entry(151, "தமிழ்நாடு துணை முதலமைச்சர் — உதயநிதி ஸ்டாலின்", "துறை வாரியாக சாதனைகள்"),
    Entry(225, "நகராட்சி நிர்வாகத்துறை — கே.என். நேரு", "துறை வாரியாக சாதனைகள்"),
    Entry(263, "ஊரக வளர்ச்சித்துறை — இ. பெரியசாமி", "துறை வாரியாக சாதனைகள்"),
    Entry(281, "பொதுப்பணித்துறை — எ.வ. வேலு", "துறை வாரியாக சாதனைகள்"),
    Entry(329, "வேளாண்மை மற்றும் உழவர் நலத்துறை — எம்.ஆர்.கே. பன்னீர்செல்வம்", "துறை வாரியாக சாதனைகள்"),
    Entry(365, "வருவாய் மற்றும் பேரிடர் மேலாண்மைத்துறை — கே.கே.எஸ்.எஸ்.ஆர். ராமச்சந்திரன்", "துறை வாரியாக சாதனைகள்"),
    Entry(389, "நிதி, சுற்றுச்சூழல் மற்றும் காலநிலை மாற்றத்துறை — தங்கம் தென்னரசு", "துறை வாரியாக சாதனைகள்"),
    Entry(429, "இயற்கை வளங்கள் துறை — எஸ். ரகுபதி", "துறை வாரியாக சாதனைகள்"),
    Entry(445, "வீட்டுவசதி, மதுவிலக்கு மற்றும் ஆயத்தீர்வைத் துறை — சு. முத்துசாமி", "துறை வாரியாக சாதனைகள்"),
    Entry(455, "கூட்டுறவுத்துறை — கே.ஆர். பெரியகருப்பன்", "துறை வாரியாக சாதனைகள்"),
    Entry(467, "குறு, சிறு மற்றும் நடுத்தரத் தொழில் நிறுவனங்கள் துறை — தா.மோ. அன்பரசன்", "துறை வாரியாக சாதனைகள்"),
    Entry(481, "தமிழ் வளர்ச்சி மற்றும் செய்தித்துறை — மு.பெ. சாமிநாதன்", "துறை வாரியாக சாதனைகள்"),
    Entry(547, "சமூக நலன் மற்றும் மகளிர் உரிமைத்துறை — பி. கீதா ஜீவன்", "துறை வாரியாக சாதனைகள்"),
    Entry(585, "மீன்வளம், மீனவர் நலன் மற்றும் கால்நடை பராமரிப்புத்துறை — அனிதா ஆர். ராதாகிருஷ்ணன்", "துறை வாரியாக சாதனைகள்"),
    Entry(613, "வனம் மற்றும் கதர்த்துறை — ஆர்.எஸ். ராஜகண்ணப்பன்", "துறை வாரியாக சாதனைகள்"),
    Entry(621, "சுற்றுலாத்துறை — ஆர். ராஜேந்திரன்", "துறை வாரியாக சாதனைகள்"),
    Entry(637, "உணவு மற்றும் உணவுப்பொருள் வழங்கல்துறை — அர. சக்கரபாணி", "துறை வாரியாக சாதனைகள்"),
    Entry(649, "கைத்தறி மற்றும் துணிநூல்துறை — ஆர். காந்தி", "துறை வாரியாக சாதனைகள்"),
    Entry(663, "மருத்துவம் மற்றும் மக்கள் நல்வாழ்வுத்துறை — மா. சுப்பிரமணியன்", "துறை வாரியாக சாதனைகள்"),
    Entry(699, "வணிகவரி மற்றும் பதிவுத்துறை — பி. மூர்த்தி", "துறை வாரியாக சாதனைகள்"),
    Entry(707, "போக்குவரத்து மற்றும் மின்சாரத்துறை — எஸ்.எஸ். சிவசங்கர்", "துறை வாரியாக சாதனைகள்"),
    Entry(723, "இந்து சமயம் மற்றும் அறநிலையத்துறை — பி.கே. சேகர்பாபு", "துறை வாரியாக சாதனைகள்"),
    Entry(739, "உயர் கல்வித்துறை — முனைவர் கோவி. செழியன்", "துறை வாரியாக சாதனைகள்"),
    Entry(763, "தகவல் தொழில்நுட்பவியல் மற்றும் டிஜிட்டல் சேவைகள் துறை — முனைவர் பழனிவேல் தியாக ராஜன்", "துறை வாரியாக சாதனைகள்"),
    Entry(783, "சிறுபான்மையினர் நலன் மற்றும் வெளிநாடு வாழ் தமிழர் நலத்துறை — எஸ்.எம். நாசர்", "துறை வாரியாக சாதனைகள்"),
    Entry(805, "பள்ளிக்கல்வித்துறை — முனைவர் அன்பில் மகேஸ் பொய்யாமொழி", "துறை வாரியாக சாதனைகள்"),
    Entry(849, "பிற்படுத்தப்பட்டோர் நலத்துறை — சிவ.வீ. மெய்யநாதன்", "துறை வாரியாக சாதனைகள்"),
    Entry(861, "தொழிலாளர் நலன் மற்றும் திறன் மேம்பாட்டுத்துறை — சி.வி. கணேசன்", "துறை வாரியாக சாதனைகள்"),
    Entry(873, "பால் வளத்துறை — த. மனோ தங்கராஜ்", "துறை வாரியாக சாதனைகள்"),
    Entry(879, "தொழில்துறை — முனைவர் டி.ஆர்.பி. ராஜா", "துறை வாரியாக சாதனைகள்"),
    Entry(889, "ஆதிதிராவிடர் நலத்துறை — மரு. மா. மதிவேந்தன்", "துறை வாரியாக சாதனைகள்"),
    Entry(903, "மனிதவள மேலாண்மைத்துறை — என். கயல்விழி செல்வராஜ்", "துறை வாரியாக சாதனைகள்"),
]

MARKER_RE = re.compile(
    r"^(?:###\s*)?(?:கோப்பு:\s*)?DMK 5 YEARS ACHIEVEMENTS(?:\s+(\d+))?\.(?:jpe?g)"
    r"(?:\s*\(.*\))?\s*$",
    re.IGNORECASE,
)
BOILERPLATE_RE = re.compile(
    r"^(?:Here is the word(?:-for-word| to-word).*|"
    r"Here is the word-to-word text extraction.*|"
    r"\(This page (?:is blank|contains only template borders).*)$",
    re.IGNORECASE,
)


def slugify(value: str) -> str:
    value = value.replace("—", "-").replace("–", "-")
    value = re.sub(r"[^\w\u0B80-\u0BFF]+", "-", value, flags=re.UNICODE)
    return re.sub(r"-+", "-", value).strip("-").lower()


def split_pages(text: str) -> dict[int, list[str]]:
    pages: dict[int, list[str]] = {}
    current: int | None = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        marker = MARKER_RE.match(line.strip())
        if marker:
            current = int(marker.group(1) or "1")
            pages.setdefault(current, [])
            continue
        if current is None or BOILERPLATE_RE.match(line.strip()):
            continue
        pages[current].append(line)
    return pages


def trim(lines: list[str]) -> list[str]:
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return lines


def yaml_quote(value: str) -> str:
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


def render(entry: Entry, end_page: int | None, pages: dict[int, list[str]]) -> str:
    start_image = entry.page + 1
    end_image_exclusive = (end_page + 1) if end_page is not None else (max(pages) + 1)
    body: list[str] = []
    used_images: list[int] = []

    for image_number in range(start_image, end_image_exclusive):
        page_lines = trim(list(pages.get(image_number, [])))
        if not page_lines:
            continue
        used_images.append(image_number)
        body.append(f"## மூலப் படம் {image_number}")
        body.append("")
        body.extend(page_lines)
        body.append("")

    if not used_images:
        raise RuntimeError(
            f"No source pages found for printed page {entry.page}: {entry.title}"
        )

    metadata = [
        "---",
        f"title: {yaml_quote(entry.title)}",
        f"category: {yaml_quote(entry.category)}",
        f"printed_page: {entry.page}",
        f"source_file: {yaml_quote('Five_years.txt')}",
        f"source_images: {used_images[0]}-{used_images[-1]}",
    ]
    if entry.byline:
        metadata.append(f"byline: {yaml_quote(entry.byline)}")
    metadata.extend(["---", "", f"# {entry.title}", ""])
    if entry.byline:
        metadata.extend([f"**{entry.byline}**", ""])
    return "\n".join(metadata + trim(body)) + "\n"


def write_readme(entries: list[Entry]) -> None:
    lines = [
        "# மக்கள் பணியில் மகத்தான 5 ஆண்டுகள் — பிரிக்கப்பட்ட உள்ளடக்கம்",
        "",
        "`Five_years.txt` கோப்பின் உள்ளடக்க அட்டவணையில் இடம்பெற்ற ஒவ்வொரு பதிவும் தனித்தனி Markdown கோப்பாகப் பிரிக்கப்பட்டுள்ளது.",
        "",
        "| அச்சுப் பக்கம் | பிரிவு | தலைப்பு |",
        "|---:|---|---|",
    ]
    for entry in entries:
        folder = "01-ஆளுமைகளின்-பார்வையில்" if entry.category == "ஆளுமைகளின் பார்வையில்" else "02-துறை-வாரியாக-சாதனைகள்"
        filename = f"{entry.page:03d}-{slugify(entry.title)}.md"
        lines.append(f"| {entry.page} | {entry.category} | [{entry.title}]({folder}/{filename}) |")
    (OUTPUT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Missing source file: {SOURCE}")

    pages = split_pages(SOURCE.read_text(encoding="utf-8"))
    if max(pages, default=0) < 904:
        raise RuntimeError(f"Source appears incomplete; highest image marker is {max(pages, default=0)}")

    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    (OUTPUT / "01-ஆளுமைகளின்-பார்வையில்").mkdir(parents=True)
    (OUTPUT / "02-துறை-வாரியாக-சாதனைகள்").mkdir(parents=True)

    for index, entry in enumerate(ENTRIES):
        next_page = ENTRIES[index + 1].page if index + 1 < len(ENTRIES) else None
        folder = "01-ஆளுமைகளின்-பார்வையில்" if entry.category == "ஆளுமைகளின் பார்வையில்" else "02-துறை-வாரியாக-சாதனைகள்"
        filename = f"{entry.page:03d}-{slugify(entry.title)}.md"
        target = OUTPUT / folder / filename
        target.write_text(render(entry, next_page, pages), encoding="utf-8")

    write_readme(ENTRIES)
    print(f"Generated {len(ENTRIES)} Markdown files in {OUTPUT}")


if __name__ == "__main__":
    main()
