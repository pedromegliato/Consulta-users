const quote = (files) => files.map((file) => `"${file}"`).join(' ');

export default {
  'backend/**/*.py': (files) => [
    `uv run --directory backend ruff format ${quote(files)}`,
    `uv run --directory backend ruff check --fix ${quote(files)}`,
  ],
  'frontend/**/*.{ts,tsx}': () => 'npm --prefix frontend run typecheck',
};
