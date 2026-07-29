---
title: {{ replace .File.ContentBaseName "-" " " | title }}
date: {{ .Date | time.Format "2006-01-02" }}
categories: []
tags: []

summary: ""

galleries:
  example:
  - image_path:
    title:
    alt:

maps:
- name: map_example
  points:
  - name: Location
    lat: 1
    lon: 1
---
