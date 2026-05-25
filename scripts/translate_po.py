#!/usr/bin/env python
"""
Fill empty msgstr entries in Django .po files using a simple glossary or passthrough.

Usage:
  conda activate p
  python scripts/translate_po.py --locale en
  python scripts/translate_po.py --locale pt --all
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import polib
except ImportError:
    print('Install polib: pip install polib', file=sys.stderr)
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent.parent
LOCALE_DIR = BASE_DIR / 'locale'

# Minimal glossary for common UI strings (extend as needed)
GLOSSARY_EN = {
    'Español': 'Spanish',
    'English': 'English',
    'Português': 'Portuguese',
    'Iniciar sesión': 'Log in',
    'Cerrar sesión': 'Log out',
    'Configuración': 'Settings',
}

GLOSSARY_PT = {
    'Español': 'Espanhol',
    'English': 'Inglês',
    'Português': 'Português',
    'Iniciar sesión': 'Entrar',
    'Cerrar sesión': 'Sair',
    'Configuración': 'Configurações',
}


def translate_entry(msgid: str, locale: str) -> str:
    glossary = GLOSSARY_EN if locale == 'en' else GLOSSARY_PT if locale == 'pt' else {}
    if msgid in glossary:
        return glossary[msgid]
    if locale == 'en':
        return msgid
    return msgid


def process_po(po_path: Path, locale: str, dry_run: bool = False) -> int:
    po = polib.pofile(str(po_path))
    updated = 0
    for entry in po:
        if entry.obsolete:
            continue
        if entry.msgstr and entry.msgstr.strip():
            continue
        if not entry.msgid:
            continue
        translation = translate_entry(entry.msgid, locale)
        if translation:
            if not dry_run:
                entry.msgstr = translation
            updated += 1
    if updated and not dry_run:
        po.save(str(po_path))
    return updated


def main():
    parser = argparse.ArgumentParser(description='Fill empty Django .po translations')
    parser.add_argument('--locale', choices=['en', 'pt', 'es'], help='Target locale folder')
    parser.add_argument('--all', action='store_true', help='Process en and pt')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    locales = ['en', 'pt'] if args.all else [args.locale] if args.locale else ['en', 'pt']

    for loc in locales:
        po_path = LOCALE_DIR / loc / 'LC_MESSAGES' / 'django.po'
        if not po_path.exists():
            print(f'Skip missing: {po_path}')
            continue
        count = process_po(po_path, loc, dry_run=args.dry_run)
        print(f'{loc}: filled {count} entries in {po_path}')


if __name__ == '__main__':
    main()
