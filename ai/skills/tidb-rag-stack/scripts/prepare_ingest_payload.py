#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


def split_chunks(text: str) -> list[str]:
    blocks = [b.strip() for b in re.split(r'\n\s*\n+', text) if b.strip()]
    chunks = []
    buf = []
    size = 0
    for block in blocks:
        blen = len(block)
        if buf and size + blen > 700:
            chunks.append('\n\n'.join(buf).strip())
            buf = [block]
            size = blen
        else:
            buf.append(block)
            size += blen
    if buf:
        chunks.append('\n\n'.join(buf).strip())
    return chunks


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--document-id', required=True)
    p.add_argument('--title', required=True)
    p.add_argument('--source-type', default='manual-summary')
    p.add_argument('--source-uri', default='local://generated')
    p.add_argument('--mime-type', default='text/markdown')
    args = p.parse_args()

    text = Path(args.input).read_text(encoding='utf-8')
    payload = {
        'document_id': args.document_id,
        'title': args.title,
        'source_type': args.source_type,
        'source_uri': args.source_uri,
        'mime_type': args.mime_type,
        'chunks': split_chunks(text),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
