# -*- coding: utf-8 -*-
"""Ajoute (ou remplace) des rapports de veille dans les fichiers JSON lus par le site.

Usage, depuis la racine du dépôt :
    python3 tools/publish.py rapport.json [autre.json ...]

Chaque fichier contient un rapport validé par veille_tool.py (ou une liste de rapports).
  - quotidien : data/daily-AAAA-MM.json, un fichier par mois, clé "date"
  - hebdo     : data/weekly.json, clé "start"
  - mensuel   : data/monthly.json, clé "start"
Un rapport déjà présent pour la même clé est remplacé. Les fichiers restent triés du plus récent au plus ancien.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DROP = ("pdf",)  # identifiant de fichier propre à l'archive Claude, inutile ici


def fail(msg):
    sys.stderr.write("ERREUR : %s\n" % msg)
    sys.exit(1)


def target(doc):
    kind = doc.get("kind")
    if not isinstance(doc.get("seal"), str):
        fail("rapport sans \"seal\" : il doit sortir de veille_tool.py.")
    if kind == "daily":
        day = doc.get("date", "")
        if not ISO.match(day):
            fail("rapport quotidien sans \"date\" valide.")
        return "daily-%s.json" % day[:7], "date"
    if kind in ("weekly", "monthly"):
        if not ISO.match(doc.get("start", "")):
            fail("rapport %s sans \"start\" valide." % kind)
        return "%s.json" % kind, "start"
    fail("\"kind\" doit valoir daily, weekly ou monthly.")


def load(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        docs = json.load(fh)
    if not isinstance(docs, list):
        fail("%s doit contenir une liste." % path)
    return docs


def main(paths):
    if not paths:
        fail("indique au moins un fichier de rapport.")
    incoming = []
    for p in paths:
        with open(p, encoding="utf-8") as fh:
            obj = json.load(fh)
        incoming.extend(obj if isinstance(obj, list) else [obj])
    touched = {}
    for doc in incoming:
        if not isinstance(doc, dict):
            fail("chaque rapport doit être un objet JSON.")
        name, key = target(doc)
        doc = {k: v for k, v in doc.items() if k not in DROP}
        path = os.path.join(DATA, name)
        if path not in touched:
            touched[path] = (key, load(path))
        docs = [d for d in touched[path][1] if d.get(key) != doc[key]]
        docs.append(doc)
        touched[path] = (key, docs)
        print("%s  %s" % (name, doc[key]))
    os.makedirs(DATA, exist_ok=True)
    for path, (key, docs) in touched.items():
        docs.sort(key=lambda d: d.get(key, ""), reverse=True)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(docs, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
        os.replace(tmp, path)
    print("%d rapport(s) publié(s) dans %d fichier(s)." % (len(incoming), len(touched)))


if __name__ == "__main__":
    main(sys.argv[1:])
