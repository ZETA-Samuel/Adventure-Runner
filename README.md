# Adventure-Runner

A simple 2D platformer made with Pygame.

## Play in your browser

After GitHub Pages is enabled and the deployment workflow has completed, play here:

https://zeta-samuel.github.io/Adventure-Runner/

The workflow builds the Pygbag web version and deploys it to GitHub Pages whenever
changes are pushed to the `main` branch. You can also run it manually from the
repository's **Actions** tab by choosing **Build and deploy game** and selecting
**Run workflow**.

### Enable GitHub Pages

In the repository, open **Settings → Pages** and set **Build and deployment →
Source** to **GitHub Actions**. Then push this workflow to `main` or run it
manually from **Actions**. GitHub will show the deployment URL in the workflow
run and under **Settings → Pages**.

## Run locally

Install Pygame and run:

```bash
python main.py
```

To build the browser version locally, install Pygbag in the project's `.venv` and
run:

```bash
./build_web.sh
```

The generated site is written to `build/web`.
