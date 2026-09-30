from pathlib import Path
import hashlib
import json
import shutil
import zipfile


ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / 'output/submission-ready'
FILES = {
    '01-cover.png': 'assets/cover-final.png',
    '02-pitch-slides.pdf': 'assets/slides/secondline-pitch-v3.pdf',
    '03-submission-copy.md': 'docs/submission-draft.md',
    '04-submission-fields.json': 'docs/submission-fields.json',
    '05-handoff.md': 'docs/submission-handoff.md',
}

missing = [source for source in FILES.values() if not (ROOT / source).is_file()]
if missing:
    raise SystemExit('Required packet inputs are missing: ' + ', '.join(missing))

DESTINATION.mkdir(parents=True, exist_ok=True)
manifest = {'video_attached': False, 'final_submitted': False, 'files': []}
for name, relative_source in FILES.items():
    source = ROOT / relative_source
    target = DESTINATION / name
    shutil.copyfile(source, target)
    manifest['files'].append({
        'filename': name,
        'source': relative_source,
        'bytes': target.stat().st_size,
        'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
    })

(DESTINATION / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
archive = ROOT / 'output/secondline-submission-ready.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as package:
    for name in (*FILES.keys(), 'manifest.json'):
        package.write(DESTINATION / name, arcname='secondline-submission/' + name)
print(f'Prepared {archive}; video and final submission remain pending.')
