#!/usr/bin/env python3
import argparse
import json
import urllib.request


def post_json(url: str, payload: dict):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode('utf-8'))


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--worker-base', default='http://127.0.0.1:8011')
    p.add_argument('--payload', required=True)
    args = p.parse_args()

    payload = json.loads(open(args.payload, 'r', encoding='utf-8').read())
    result = post_json(f"{args.worker_base}/ingest", payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
