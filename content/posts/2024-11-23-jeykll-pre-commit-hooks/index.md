---
aliases:
  - "/code/jeykll-pre-commit-hooks/"
title: "Jekyll pre-commit Hooks"
date: 2024-11-23 18:11:00 +0000
last_modified_at: 2025-04-27 11:49:52 +0000
categories: [code]
tags: [git, jekyll]

summary: "I use multiple pre-commit hooks to make sure my posts are really ready. This is my setup."
---

You can see my full pre-commit setup [here](https://github.com/pwhittlesea/thega.me.uk/blob/f3603c1faf1b09e4d7300a0cce1f93d037c79a7e/.pre-commit-config.yaml).
There are some extras that are not mentioned on this page, but these are mostly linting tools for the various scripts I am running.

## Remove Image Metadata

A key part of a lot of my posts (especially my travel blogs) are pictures.
When you take a picture with a modern device (that knows where it is on the planet) it will embed the location of the picture, as well as other interesting/useful metadata, into the file.
This metadata is called [Exif](https://en.wikipedia.org/wiki/Exif).

When posting pictures online it's normally quite prudent to strip all the Exif information from your photos; so people can't see where you live.

I do however want to keep some Exif information; the ICC colour profile of the picture is something I want to keep so that it looks correct.
I also want to add in a Copyright; this won't stop AI's training on my images, but if I see someone profiting off one then I will hopefully have some legal recourse.

For this I need to run `exiftool` (the script can be found [here](https://github.com/pwhittlesea/thega.me.uk/blob/f3603c1faf1b09e4d7300a0cce1f93d037c79a7e/.hooks/correct_exif.sh)) which I wrap in a 'local' pre-commit hook:

```yaml
repos:
  - repo: local
    hooks:
    - id: exif-correct
      name: Exif Correct
      description: Removes all Exif data from images and sets the correct Copyright
      entry: .hooks/correct_exif.sh
      language: script
      types: [image]
      exclude_types: [svg,gif]
```

I excluded SVGs because `exiftool` does not support SVGs.
I also exclude Gifs as I am not normally the author of them (they are normally memes), so adding a copyright would be a lie.

If you wanted to just strip everything, you could use the [strip-exif](https://github.com/stefmolin/exif-stripper) pre-commit hook by Stefanie Molin.

## Update Last Modified Time

A neat feature of Jekyll is that you can have last updated times on the posts (you can see one on the bottom of this page).
This is expressed in the front matter of each blog:

```yaml
---
title: "My amazing blog!"
date: 2024-11-12 00:00:00 +0100
last_modified_at: 2025-04-27T11:49:52+00:00
---
```

I will, however, never remember to update these before I commit and push, so I have a simple [script](https://github.com/pwhittlesea/thega.me.uk/blob/f3603c1faf1b09e4d7300a0cce1f93d037c79a7e/.hooks/update_last_modified.sh) which updates them for me with the current time:

```yaml
repos:
  - repo: local
    hooks:
    - id: update-last-modified
      name: Update Last Modified
      description: Replace `last_modified_at` timestamp with current time
      entry: .hooks/update_last_modified.sh
      language: script
      always_run: true
      require_serial: true
```

Credit here entirely goes to Michael Rose who wrote a [post](https://mademistakes.com/notes/adding-last-modified-timestamps-with-git/) on this a while ago.

## Generate Maps

I wrote a [whole blog]({{< ref "2024-09-28-adding-maps-to-my-travel-posts" >}}) on how I added maps to my blogs, and a key part of that is the pre-commit hook.
Head over to that blog to read more.

## Validating Links

Almost all of my blogs link to other sites, other blogs by me, or images.
When I am writing I double-check that my links actually go somewhere and that I don't have broken images.

However, after a while these links may break.
The brilliant [markdown-link-check](https://github.com/tcort/markdown-link-check) by Thomas Cort helps check these links are still working.

## General Tidy

Finally, there are quite a few housekeeping checks that I run to ensure that my Markdown file are consistent and well-formed:

```yaml
repos:
  # Generic pre-commit hooks for all files
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
    - id: end-of-file-fixer
    - id: mixed-line-ending
    - id: trailing-whitespace
      args: ["--markdown-linebreak-ext=markdown,md"]

  # Check Markdown documents with Markdownlint
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.42.0
    hooks:
      - id: markdownlint
```
