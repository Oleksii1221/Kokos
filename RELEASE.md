# Release Process

Kokos uses a conservative branch model.

## Branches

- `dev` receives active development.
- `master` contains stable releases only.

## Versioning

Use semantic versioning:

- `MAJOR` for breaking operational or data changes.
- `MINOR` for backward-compatible features.
- `PATCH` for fixes and documentation-only release updates.

## Checklist

1. Confirm `dev` is green:

```bash
python -m compileall app
python -m pytest
docker build -t kokos-bot:release-check .
```

2. Update `CHANGELOG.md`.
3. Merge or promote `dev` to `master`.
4. Tag the release:

```bash
git tag -a vX.Y.Z -m "Kokos X.Y.Z"
git push origin master
git push origin vX.Y.Z
```

5. Confirm GitHub Actions and the release page.

