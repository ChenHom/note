#!/usr/bin/env python3
import argparse
import json
import re
import urllib.request
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


def post_json(url: str, payload: dict):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode('utf-8'))


def fetch_json(url: str):
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', required=True)
    p.add_argument('--document-id', required=True)
    p.add_argument('--title', required=True)
    p.add_argument('--source-type', default='manual-summary')
    p.add_argument('--source-uri', default='local://generated')
    p.add_argument('--mime-type', default='text/markdown')
    p.add_argument('--worker-base', default='http://127.0.0.1:8011')
    p.add_argument('--api-base', default='http://127.0.0.1:8010')
    p.add_argument('--query', default=None)
    p.add_argument('--output-dir', default='.')
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

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    payload_path = out_dir / f'{args.document_id}.payload.json'
    payload_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')

    write_result = post_json(f"{args.worker_base}/ingest", payload)

    verify = {'document_id': args.document_id}
    try:
        verify['document_detail'] = fetch_json(f"{args.api_base}/documents/{args.document_id}")
    except Exception as e:
        verify['document_detail_error'] = str(e)

    if args.query:
        try:
            verify['search_result'] = post_json(f"{args.api_base}/search", {
                'query': args.query,
                'limit': 5,
                'hybrid': True,
            })
        except Exception as e:
            verify['search_error'] = str(e)

    summary = {
        'payload_path': str(payload_path),
        'write_result': write_result,
        'verify': verify,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
