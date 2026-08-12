---
title: "Bye-Bye GitHub Pages Gem"
date: 2025-04-27 23:13:00 +0200
last_modified_at: 2025-05-05 14:30:36 +0100
categories: ["update"]
tags: ["jekyll", "github"]
---

I moved away from the branch build and `github-pages` Gem for this site, and now I have an up-to-date, and more configurable build.

<!--more-->

## Background

[Back at the beginning of 2024]({{< ref "2024-02-17-new-beginnings" >}}) I switched from an old raggedy single page website, to a new blog;
powered by [Jekyll](https://jekyllrb.com).

I originally picked the [Minima](https://github.com/jekyll/minima) theme:

> Minima meets my needs as far as themes go
>
> &mdash; Me, 17th Feb 2024 at 17:07

But almost immediately &mdash; 18th Feb 2024 at 14:25 &mdash; I [switched](https://github.com/pwhittlesea/pwhittlesea.github.com/commit/8fe8b9dea8c2b5e65334104de431446b8ea168f0) to the [Minimal Mistakes](https://github.com/mmistakes/minimal-mistakes) plugin, so I can't be trusted it seems.

Up until this week, I have relied on the [`github-pages`](https://github.com/github/pages-gem) Ruby Gem to configure this sites build environment.
It enabled me to run the site locally, and on GitHub, with the same dependency tree and configuration.

The `github-pages` gem works by restricting which plugins can be used by the site, setting the versions of those plugins, and by setting [some](https://github.com/github/pages-gem/blob/v232/lib/github-pages/configuration.rb) key Jekyll properties to values that GitHub mandates.
GitHub does this for security reasons[^1].

[^1]: And because supporting every plugin would take a lot of time.

As I was using this Gem, I also took advantage of the 'out-of-the-box' [GitHub deployment process](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) where all the build steps are managed for you, and GitHub pushes your site from a given branch.

A managed dependency tree and build pipeline are great for getting started quickly, and keeping my development environment the same as GitHubs deployment environment.

But if it's so good, why did I move away from it?

## End of Life

Several things compounded together that resulted in me looking to factor it out of my build:

- The [last release](https://github.com/github/pages-gem/releases/tag/v232) of the Gem was back in August 2024
- Issues [like this one](https://github.com/github/pages-gem/issues/890) &mdash; raised in September 2023 &mdash; go unanswered; leading to the feeling the repo is almost un-maintained by GitHub
- The plugin only supports Jekyll 3, but Jekyll 4 was released in August 2019, and there's no sign of any progress to support it in the Gem
- I have occasionally wanted to try plugins that are not on the allowed list
- The theme I use leverages plugins that are not supported on branch built GitHub Pages projects (like [Pagination v2](https://github.com/sverrirs/jekyll-paginate-v2))
- GitHub themselves say to move away from the 'branch build' and to a GitHub Actions build [if you want Jekyll 4+](https://github.blog/news-insights/product-news/github-pages-now-uses-actions-by-default/#how-can-i-upgrade-to-jekyll-4)

Oh.
OH.
That last part seems kind of important.
:facepalm:

So it appears that GitHub have just 'quiet quit' the `github-pages` Gem, and are advising people to move away through their blog posts.
Which would be great, **IF** their documentation agreed, and pushed you in that direction.
Unfortunately the documentation makes it seem like the branch build process, and the Gem, are still the way to go:

> You can publish your site when changes are pushed to a specific branch, or you can write a GitHub Actions workflow to publish your site.
>
> **If you do not need any control over the build process for your site, we recommend that you publish your site when changes are pushed to a specific branch.** You can specify which branch and folder to use as your publishing source. The source branch can be any branch in your repository, and the source folder can either be the root of the repository (/) on the source branch or a /docs folder on the source branch. Whenever changes are pushed to the source branch, the changes in the source folder will be published to your GitHub Pages site.
>
> If you want to use a build process **other than Jekyll** or you do not want a dedicated branch to hold your compiled static files, we recommend that you write a GitHub Actions workflow to publish your site. GitHub provides workflow templates for common publishing scenarios to help you write your workflow.
>
> &mdash; [GitHub Pages Documentation - 2025](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site#about-publishing-sources)

I've highlighted the key parts that informed my original decision last year.
I did not need more control, _and_ I am using Jekyll, so I don't need a full GitHub Actions pipeline.

Nothing here reads 'we will not be updating the branch build environment to support Jekyll 4 and above'.

I found this out, not from the blogs &mdash; which never returned in a search, or were otherwise easy to discover &mdash; but from a [GitHub comment](https://github.com/github/pages-gem/issues/651#issuecomment-2712968982)[^2].
The Gem is practically end of life by GitHubs own admission[^3].

[^2]: Thankfully that same person has raised an [issue](https://github.com/github/docs/issues/36740) for GitHub to update their documentation to remove all references to the deprecated pipeline.

[^3]: End `</rant>`

## Newer Beginnings

So I knew I wanted to be on the latest version of Jekyll, but jumping in one go would be risky, if I wanted to keep this site up.

So I settled for a multiphase approach:

1. I would keep the same dependency tree, but build and deploy using a [GitHub Actions pipeline](https://jekyllrb.com/docs/continuous-integration/github-actions/) &mdash; this would give me the ability to inspect the built site before pushing it live
2. Copy all the transitive dependencies from `github-pages` into my `Gemfile` &mdash; ensuring that when I remove the pages Gem, I don't lose any functionality
3. Remove the `github-pages` Gem
4. Remove the dependencies added in step to one-by-one to see what is not needed for my site (e.g. `github-pages` has lots of themes included)
5. Switch to the Gem version of my theme from the remote theme plugin
6. Update to the latest version of Jekyll by removing all versions from dependencies (except the theme) unless they need to be pinned due to bugs
7. Leverage any new features Jekyll has in v4+ that I couldn't use before

At each step of this process I downloaded the generated site from GitHub Actions (current) and compared it against the one built locally using the `bundle exec jekyll build` command.

To do this I used plain old Linux `diff` (but I'm sure a better tool exists):

```bash
diff -bur ~/Downloads/current_site ./_site
```

It was mostly plain sailing but step 3 and 6 had issues.

On step 3, when I removed the pages Gem, my `404.html` stopped having a page title of `404`.

This functionality was actually provided by the `jekyll-titles-from-headings` plugin which the GitHub pages Gem forces into the build.
So when I removed the pages Gem, the behaviour disappeared.

It took me about 3 hours of on-and-off debugging to figure that out, so if you are also doing this, hopefully it makes the update slightly easier.

On step 6, a lot of SASS deprecation warnings appeared.
This is a [known issue](https://github.com/mmistakes/minimal-mistakes/issues/4054) with my theme, and all I had to do was pin `jekyll-sass-converter` to a previous version.

## Fin

Now I have a nice new Jekyll 4 based blog :smile:

_And_, complete control over my build pipeline.

_And_, branch builds to check the impact of changes first[^4].

[^4]: I might look to do a diff between the deployed and the branch as a build step later.
      If the mood takes me.

Win, win, win!

The best part of the upgrade is that Jekyll 4 includes relative [post_url](https://jekyllrb.com/docs/liquid/tags/#linking-to-posts) resolution, making the `jekyll-relative-links` plugin redundant (for my use case):

```diff
- [Click here](../_posts/2024-11-24-12-days-of-short-stories.md) to read the explanation of why I'm writing them.
+ [Click here]({% post_url 2024-11-24-12-days-of-short-stories %}) to read the explanation of why I'm writing them.
```

Thanks for reading!
