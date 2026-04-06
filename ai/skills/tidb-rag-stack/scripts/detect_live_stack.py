#!/usr/bin/env python3
import json
import os
import re
from pathlib import Path

CANDIDATES = [
    Path('/home/hom/services/rag-stack'),
]

COMPOSE_NAMES = ['docker-compose.yml', 'compose.yml', 'compose.yaml']


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8')
    except Exception:
        return ''


def find_project() -> Path | None:
    for p in CANDIDATES:
        if p.exists() and p.is_dir():
            return p
    return None


def detect_compose(project: Path) -> Path | None:
    for name in COMPOSE_NAMES:
        p = project / name
        if p.exists():
            return p
    return None


def parse_env(env_path: Path) -> dict:
    data = {}
    if not env_path.exists():
        return data
    for line in read_text(env_path).splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        data[k.strip()] = v.strip()
    return data


def redact_env(env: dict) -> dict:
    redacted = {}
    for k, v in env.items():
        if any(x in k.upper() for x in ['KEY', 'PASSWORD', 'SECRET', 'TOKEN']):
            redacted[k] = '[REDACTED]'
        else:
            redacted[k] = v
    return redacted


def detect_services(compose_text: str) -> list[str]:
    found = []
    for name in ['qdrant', 'minio', 'rag-api', 'rag-worker']:
        if re.search(rf'^\s{{2}}{re.escape(name)}:\s*$', compose_text, re.M):
            found.append(name)
    return found


def detect_endpoints(py_text: str) -> list[str]:
    endpoints = []
    for method in ['get', 'post', 'delete', 'put', 'patch']:
        pattern = rf'@app\.{method}\("([^"]+)"'
        for m in re.finditer(pattern, py_text):
            endpoints.append(f'{method.upper()} {m.group(1)}')
    return sorted(set(endpoints))


def main():
    project = find_project()
    if not project:
        print(json.dumps({'ok': False, 'error': 'project_not_found'}))
        return

    compose_path = detect_compose(project)
    env_path = project / '.env'
    sql_path = project / 'sql' / '001_init.sql'
    api_path = project / 'app' / 'api' / 'server.py'
    worker_path = project / 'app' / 'worker' / 'server.py'

    compose_text = read_text(compose_path) if compose_path else ''
    api_text = read_text(api_path)
    worker_text = read_text(worker_path)
    env = parse_env(env_path)

    result = {
        'ok': True,
        'project_path': str(project),
        'compose_path': str(compose_path) if compose_path else None,
        'env_path': str(env_path) if env_path.exists() else None,
        'sql_path': str(sql_path) if sql_path.exists() else None,
        'services': detect_services(compose_text),
        'api_endpoints': detect_endpoints(api_text),
        'worker_endpoints': detect_endpoints(worker_text),
        'env': redact_env({
            k: env[k] for k in [
                'RAG_API_PORT', 'RAG_WORKER_PORT', 'TIDB_HOST', 'TIDB_PORT',
                'QDRANT_COLLECTION', 'EMBEDDING_PROVIDER', 'EMBEDDING_MODEL', 'EMBEDDING_DIMENSIONS'
            ] if k in env
        }),
    }

    preferred = None
    if 'POST /ingest' in result['worker_endpoints']:
        preferred = 'POST /ingest'
    elif 'POST /upload' in result['worker_endpoints']:
        preferred = 'POST /upload'
    result['preferred_write_path'] = preferred

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
