import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "index.html"
CSS_PATH = ROOT / "styles.css"
REQUIRED_LABEL = (
    "Imágenes publicadas en perfiles comerciales de la empresa. "
    "No representan disponibilidad actual."
)
ASSETS = {
    "logo.webp",
    "hero-marketplace-1920.webp",
    "apoyo-cargadora-cadenas.jpg",
    "apoyo-excavadora.jpg",
    "apoyo-cargadora-ruedas.jpg",
    "apoyo-manipuladora.jpg",
}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.images = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        self.tags.append((tag, values))
        if tag == "img":
            self.images.append(values)
        if tag == "a":
            self.links.append(values.get("href", ""))


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = HTML_PATH.read_text(encoding="utf-8")
        cls.css = CSS_PATH.read_text(encoding="utf-8")
        cls.parser = PageParser()
        cls.parser.feed(cls.html)

    def test_required_files_exist(self):
        for name in ("index.html", "styles.css", "script.js", "image-sources.json", "README.md"):
            self.assertTrue((ROOT / name).is_file(), name)
        self.assertEqual({p.name for p in (ROOT / "assets").iterdir() if p.is_file()}, ASSETS)

    def test_semantic_and_accessible_structure(self):
        tags = [tag for tag, _ in self.parser.tags]
        for tag in ("header", "nav", "main", "section", "footer", "h1"):
            self.assertIn(tag, tags)
        self.assertTrue(all(img.get("alt") is not None for img in self.parser.images))
        self.assertIn('name="viewport"', self.html)
        self.assertIn("@media(max-width:900px)", self.css)

    def test_contact_details(self):
        self.assertIn("629 11 35 82", self.html)
        self.assertIn("tel:+34629113582", self.parser.links)
        self.assertIn("mailto:sanlucarmaquinarias@gmail.com", self.parser.links)
        self.assertIn("Avenida Sudáfrica 88", self.html)

    def test_all_declared_images_exist(self):
        local_sources = [i["src"] for i in self.parser.images if i.get("src", "").startswith("assets/")]
        local_sources.append("assets/hero-marketplace-1920.webp")
        self.assertEqual({Path(src).name for src in local_sources}, ASSETS)
        for src in local_sources:
            self.assertTrue((ROOT / src).is_file(), src)

    def test_editorial_image_limits_and_label(self):
        self.assertGreaterEqual(self.html.count(REQUIRED_LABEL), 2)
        self.assertNotIn("background:url('assets/hero-marketplace-1920.webp')", self.css)
        self.assertRegex(self.css, r"\.archive-thumb\{[^}]*max-width:240px")
        self.assertIn("Archivo de perfil comercial", self.html)
        self.assertRegex(self.css, r"\.machine-card img\{[^}]*max-width:308px")
        hero_thumb = [i for i in self.parser.images if "hero-marketplace" in i.get("src", "")]
        self.assertEqual(len(hero_thumb), 1)
        self.assertEqual((hero_thumb[0].get("width"), hero_thumb[0].get("height")), ("240", "135"))
        thumbs = [i for i in self.parser.images if "apoyo-" in i.get("src", "")]
        self.assertEqual(len(thumbs), 4)
        self.assertTrue(all(i.get("width") == "308" and i.get("height") == "231" for i in thumbs))

    def test_image_manifest(self):
        data = json.loads((ROOT / "image-sources.json").read_text(encoding="utf-8"))
        self.assertEqual(data["required_label"], REQUIRED_LABEL)
        self.assertEqual({Path(i["file"]).name for i in data["images"]}, ASSETS)

    def test_no_prohibited_commercial_claims(self):
        visible = re.sub(r"<[^>]+>", " ", self.html).lower()
        forbidden = ("precio", "garantía", "años de experiencia", "en stock", "maquinaria agrícola", "repuestos")
        for phrase in forbidden:
            self.assertNotIn(phrase, visible)

    def test_marker_present(self):
        self.assertIn("MAQUINARIAS-SANLUCAR-DEMO-20260726", self.html)


if __name__ == "__main__":
    unittest.main()
