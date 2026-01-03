---
aliases:
  - "/code/adding-maps-to-my-travel-posts/"
title: "Adding Maps to my Travel Posts"
date: 2024-09-28 21:31:00 +0100
last_modified_at: 2025-04-27 11:49:52 +0000
categories: [code]
tags: [git, precommit, maps]

summary: My travel posts lacked visual context, so I added SVG maps to them.

maps:
  - name: an_example_map
    line: true
    zoom: 11
    points:
      - name: West Meon Hut
        lat: 51.02723146222851
        lon: -1.070542321616099
      - lat: 51.01362567610521
        lon: -1.0918283325358271
      - name: Washford
        lat: 51.00433689443536
        lon: -1.1127710206987853
      - name: Meonstoke
        lat: 50.97300054462535
        lon: -1.1285638675101963
      - lat: 50.95916259806181
        lon: -1.1419534550242187
      - name: Upper Swanmore
        lat: 50.953323477967594
        lon: -1.1704492438361127
---

> [!TIP]
> This post is inspired by Josh Erb's blog: [How I Added Maps to my Travel Posts](https://cyberb.space/notes/2024/how-i-added-maps-to-my-travel-posts/).

{{< map name="an_example_map" >}}

I recently started writing a travel blog on my visit to [New Zealand]({{< ref "/tags/new-zealand/" >}}) and something was missing.
Posts lacked a bit of context as to where I was and where the blog would be taking the reader.

As a daily lurker of 'Hacker News', almost immediately after I had posted my first blog on the 15^th^ of September,
I came across a post from the day before titled ['I Added SVG Maps to My Travel Posts'](https://news.ycombinator.com/item?id=41532958).

As someone who worked in a Geospatial company for a decade I'm ashamed to admit I had not considered maps on my posts.
Mostly because 'maps' normally equals 'Google Maps' and about 5 years ago I gave up wanting to deal with the hassle
of sorting out API Keys etc. etc...

Josh goes into detail in their [post](https://cyberb.space/notes/2024/how-i-added-maps-to-my-travel-posts/)
about why and _how_ they avoided this.

This post dives into how Josh inspired me to solve the same problem; and how I ended up with a different solution.

## Requirements

I would encourage you to read through Josh's post because I have the same base requirements as they did:

- No 3rd party platforms
- Generated at build time
- Looks consistent on mobile & desktop

To address all 3 requirements Josh uses [d3](https://d3js.org/d3-geo), writes a custom tag for his [11ty](https://www.11ty.dev/)
based site which allows them to specify the following in the Front Matter of each post:

```yaml
location: mumbai
```

Which is then passed to a custom function in the post template file:

```liquid
{% cartographer location %}
```

This results in a custom JavaScript function in the site configuration being called,
which generates a map for the given location.
When their site is built the map is generated.

![magic](magic.gif)
{style="width: 50%;"}

I would have _loved_ to have copy and pasted the solution to my own site, but my setup is a bit different.

I use [Jekyll](https://jekyllrb.com/), and my first thought was that I write a custom plugin for it.

However, I do not &mdash; currently &mdash; pre-build my site before I push it to GitHub and use GitHub Pages to deploy the site.
Unfortunately the build pipeline is not-configurable;
GitHub [has limited plugin](https://pages.github.com/versions/) support with no support for custom plugins.

So, it was at this point I could either:

1. Change to building my site locally and push resultant resources to GitHub
2. Generate the images before commit and upload the static images with the post to GitHub

The second option seemed like less of a change to my process, so that's what I picked.

## Abusing pre-commit

As I don't have a build pipeline I can control, I have opted for [pre-commit](https://pre-commit.com/) in my local repository.

If you don't know what pre-commit is, in short,
it is a way of syncing/revision controlling [Git](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks) `pre-commit` hooks;
so they are the same on any developers machine.

In my `.pre-commit-config.yml` file[^1] I put the following python hook:

[^1]: You can see my latest `.pre-commit-config.yml` [here](https://github.com/pwhittlesea/pwhittlesea.github.com/blob/main/.pre-commit-config.yaml).

```yaml
repos:
  - repo: local
    hooks:
    - id: generate-maps
      name: Generate Maps
      description: Generate all the maps used in posts
      entry: python3 .generate_maps.py
      language: python
      additional_dependencies: ["py-staticmaps", "python-frontmatter"]
      always_run: true
```

Here we are telling pre-commit to run `python3 .generate_maps.py` as a `pre-commit` Git hook.

Because everyone needs dependencies &mdash; and everyone hates having those dependencies installed globally on their system &mdash;
the `additional_dependencies` block will create a [virtual environment](https://docs.python.org/3/library/venv.html)
with the defined libraries installed.
_Neat_.

Then, on each commit or if I manually run `pre-commit`, my map generation code will run.

If I forget to do this before I commit, I will get the following failure:

```sh
$ git commit -m 'Amazing content'
Generate Maps...................................Failed
- hook id: generate-maps
- exit code: 1

New map './assets/images/maps/map.svg' generated
```

Or, if I update the generate map code (e.g. changing the font of labels), then I will get the following:

```sh
$ git commit -m 'Amazing content'
Generate Maps.....................Failed
- hook id: generate-maps
- files were modified by this hook
```

> [!DANGER]
> Currently, this hook will not pick up new maps which were unstaged (always run `git status` kids)!

## Image Generation

The first part of my solution &mdash; and probably the most important part &mdash; is the generation of the maps.
This is going to consist of 3 main parts:

1. Reading the [Front Matter](https://jekyllrb.com/docs/front-matter/) from my posts[^2].
2. Generating the SVG map
3. Integrating with pre-commit

[^2]: The 'Front Matter' in posts seemed like the most logical place to store the configuration as we can use it to generate alt text for the maps.

I found [py-staticmaps](https://github.com/flopp/py-staticmaps)[^3], and I've gotten some good millage from it;
there are probably alternatives out there, but it's a good library that allowed me to configure all the things I needed to.

[^3]: I reached for Python as I am more familiar with the tool chain; which meant I had to find an alternative to the JavaScript based D3.

> [!NOTE]
> `py-staticmaps` is not currently being pushed to pypi, so I needed to patch for an API difference in PIL.
> Thanks to the awesome community I found a quick patch [here](https://github.com/flopp/py-staticmaps/issues/39#issuecomment-2264856739).

### Reading Front Matter

Everyone of my posts has a [Front Matter](https://jekyllrb.com/docs/front-matter/) block which contains metadata on the post itself.

Using [python-frontmatter](https://github.com/eyeseast/python-frontmatter/) I can pull out structured information from the post.

Using custom Front Matter I could represent a map with a line drawn between London and Auckland like so:

```yaml
---
title: "I visited New Zealand - Part 1"
date: 2024-09-15 20:00:00 +0000
maps:
  - name: london_to_auckland
    line: true
    points:
      - name: London
        lat: 51.4775
        lon: -0.461389
      - name: Auckland
        lat: -37.008056
        lon: 174.791667
---
```

To see how I use `python-frontmatter`, take a look at [the code](https://github.com/pwhittlesea/pwhittlesea.github.com/blob/1f6f8d270d438a3d2c2a69d7915afdfc7ec6cd2e/.generate_maps.py#L76-L86)
but, in short, you can pull out information like so:

```python
with open("./_posts/2024-09-15-new-zealand-1.md") as f:
    post = frontmatter.loads(f.read())
    title = post["title"]
```

### Failing pre-commit

There are two main cases when I want pre-commit to warn me something has changed.
When a new map is created, and when an existing map is updated.

The update case is easier as pre-commit is sensitive to files changing when its running; so there's nothing to do here.

The 'new map' case is a bit harder.

If you have scanned the source code you may have noticed that the python file ends with `sys.exit(exit_code)`.
This is a way for me to signal to pre-commit that it needs to abort the in-progress commit, and warn the user.

This is not foolproof because the following events could happen:

1. I add a new post with a map definition
2. I commit
3. pre-commit fails because `generate-maps` exited with a code of 1 as it created a new unstaged file
4. An unstaged SVG is in the working directory, but I don't notice and commit again
5. `generate-maps` does not fail because it thinks nothing needs to change
6. The commit is successful :sob:

I'm open to a better way of solving this; maybe getting my python code to check for unstaged files?

### (Bonus) Waypoint Captions

Out of the box `py-staticmaps` gives you a `Marker`, `Line`, and `Area`.
Other entities are left as an [exercise for the reader](https://github.com/flopp/py-staticmaps/issues/10) and,
as I wanted to put labels on my Markers, I had to learn how SVG worked.

The example from `py-staticmaps` allowed me to get a working version with text captions quite quickly,
but they were not legible when they intersected with the line/map.
So I set about trying to put a white background behind them.

This actually took _way_ more time than I expected, but a couple of hours later I had a basic
[implementation](https://github.com/pwhittlesea/pwhittlesea.github.com/blob/1f6f8d270d438a3d2c2a69d7915afdfc7ec6cd2e/.generate_maps.py#L28-L71)
which put a white 'flood' filter on the text (shown in the example above)[^4].

[^4]: Thanks to [Robert Longson](https://stackoverflow.com/a/31013492)

## Embedding Maps

So I have the map stored in `./assets/images/maps/<name>.svg`.
Now I have to get it to show in the post as an image.

The _normal_ way of doing this is with a markdown image reference:

```markdown
![my-map](/assets/images/maps/<name>.svg "Alt text")
```

However, all the metadata of the maps are just _sat there_; right at the top of the file.
It would be a shame if I couldn't do something with it.

Which is when I stumbled upon [Jekyll without plugins](https://jekyllcodex.org/without-plugins/).

By [looking at some](https://github.com/jhvanderschee/jekyllcodex/blob/3f5bbeac8c21a94769244081768bc739ed31738f/_includes/reading-time.html)
of the Plugin-free solutions listed, I was able to cobble together a solution that looks like this:

```liquid
{% include map.html name="london_to_auckland" %}
```

This includes a custom HTML file called [map.html](https://github.com/pwhittlesea/pwhittlesea.github.com/blob/1f6f8d270d438a3d2c2a69d7915afdfc7ec6cd2e/_includes/map.html)
which then pulls all the map metadata from the Front Matter based on the given name.

This then allows me to do cool things like change the alt text of the image to include the captions of the locations when present.
Hover over the example at the top of this page to see it in action!

![more-magic](magic.gif)

## The Final Result

You can see the final result on my [New Zealand - Part 1]({{< ref "2024-09-15-new-zealand-1" >}}#wednesday-29th-flying-to-new-zealand) post.
The source code for which can be found [here](https://github.com/pwhittlesea/thega.me.uk/blob/4240ac7bf0501e542a4228dcd970c63075d68ba0/_posts/2024-09-15-new-zealand-1.md).
