---
title: Demo
date: 2025-01-01 00:00:00
build:
  list: never

maps:
  - name: great_circle
    line: true
    points:
      - name: London
        lat: 51.5074
        lon: -0.1278
      - name: New York
        lat: 40.7128
        lon: -74.0060
  - name: four_points_and_line
    line: true
    points:
      - name: Heathrow
        lat: 51.470022
        lon: -0.454295
      - name: Manchester
        lat: 53.365408
        lon: -2.272112
      - name: Glasgow
        lat: 55.864237
        lon: -4.251806
      - name: Dublin
        lat: 53.426448
        lon: -6.249321
  - name: three_points
    points:
      - name: First
        lat: -36.98423077314447
        lon: 174.78368330179273
      - name: Second
        lat: -37.976802027457616
        lon: 175.7559586435218
      - name: Third
        lat: -38.13828188586393
        lon: 176.2558456625266
  - name: two_points
    points:
      - name: Start
        lat: -38.13828188586393
        lon: 176.2558456625266
      - name: End
        lat: -38.106563710921314
        lon: 176.22083340538035
  - name: one_point
    points:
      - name: One
        lat: -38.106563710921314
        lon: 176.22083340538035

three-photos:
  - image_path: new_zealand_0647.jpg
    title: "The Waiheke Bay"
    alt: "Some alt text"
  - image_path: new_zealand_0648.jpg
    title: "More Waiheke Bay"
  - image_path: new_zealand_0652.jpg
    title: "The view out over Stonyridge Vineyard"

two-photos:
  - image_path: new_zealand_0647.jpg
    title: "The Waiheke Bay"
  - image_path: new_zealand_0652.jpg
    title: "The view out over Stonyridge Vineyard"

one-photo:
  - image_path: new_zealand_0652.jpg
    title: "The view out over Stonyridge Vineyard"
---

This page contains a collection of markdown entities to demo/test their rendering.

## Admonitions

<!-- markdownlint-disable MD028 -->

> [!NOTE]
> Useful information that users should know, even when skimming content.
> This also has an amount of content which will need to spill onto a new line.

> [!TIP]
> Helpful advice for doing things better or more easily.

> [!INFO]
> Key information users need to know to achieve their goal.

> [!WARNING]
> Urgent info that needs immediate user attention to avoid problems.

> [!DANGER]
> Advises about risks or negative outcomes of certain actions.

> [!NOTE] Custom Title
> This is a note with a custom title.

> [!NOTE]- Expandable Note
> This is a collapsible note.
> It starts collapsed.

> [!NOTE]+ Collapsible Note
> This is a collapsible note.
> It starts expanded.

<!-- markdownlint-enable MD028 -->

## Maps

{{< map name="one_point" >}}

{{< map name="two_points" >}}

{{< map name="three_points" >}}

{{< map name="four_points_and_line" >}}

{{< map name="great_circle" caption="This is a custom caption for this great circle map" >}}

## Term

The term {{< term "D&D" >}} and {{< term "DM" >}} in some text.

[The term {{< term "LoTR" >}} in a link](https://thega.me.uk/)

## Gallery

{{< mm-gallery id="three-photos" caption="This is a custom caption for the gallery" >}}

{{< mm-gallery id="two-photos" >}}

{{< mm-gallery id="one-photo" caption="A single photo">}}

<!-- markdownlint-disable MD059 -->
{{< mm-gallery
      id="one-photo"
      caption="This should be half width with a [link](https://thega.me.uk)"
      class="tw:max-w-1/2" >}}
<!-- markdownlint-enable MD059 -->

## Image Width

Full width image:

![This is a full width image](new_zealand_0647.jpg)

Half width image:

![This is a half width image](new_zealand_0647.jpg)
{style="width:50%;"}

## Code Blocks

```html {title="code_with_title_and_highlight.html" lineNos=inline hl_lines=[4,"7-9"]}
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Example HTML5 Document</title>
</head>
<body>
  <p>Test</p>
</body>
</html>
```

Here is a link that is broken on purpose: [Broken Link](https://github.com/unknown-person/unknown-project)
