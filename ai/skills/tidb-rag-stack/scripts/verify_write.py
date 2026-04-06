#!/usr/bin/env python3
import argparse
import json
import urllib.request
import urllib.error


def fetch_json(url: str):
    with urllib.request.urlopen(url, timeout=20) as resp:
        return json.loads(resp.read().decode('utf-8'))


def post_json(url: str, payload: dict):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--api-base', default='http://127.0.0.1:8010')
    p.add_argument('--document-id', required=True)
    p.add_argument('--query', default=None)
    args = p.parse_args()

    out = {'ok': True, 'document_id': args.document_id}

    try:
        out['document_detail'] = fetch_json(f"{args.api_base}/documents/{args.document_id}")
    except Exception as e:
        out['ok'] = False
        out['document_detail_error'] = str(e)

    if args.query:
        try:
            out['search_result'] = post_json(f"{args.api_base}/search", {
                'query': args.query,
                'limit': 5,
                'hybrid': True,
            })
        except Exception as e:
            out['ok'] = False
            out['search_error'] = str(e)

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
