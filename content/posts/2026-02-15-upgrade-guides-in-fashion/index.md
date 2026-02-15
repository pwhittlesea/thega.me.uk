---
title: Upgrade Guides are in Fashion Again
date: 2026-02-15
tags: [ai, engineering]
---

With the rise of LLM-driven development, my previously ignored upgrade guides, finally have someone who reads them.

<!--more-->

## Background

Ignoring the anthropomorphization of an LLM &mdash; which happens far too much, leading to people assigning accountability to tools, and not themselves &mdash; I am quite pleased that all the effort I have put in over my career into clear, concise, and consumable documentation, is paying off.

As I [previously mentioned]({{% ref "2025-02-19-10-years-frameworks" %}}), I have been building and maintaining an application framework for over a decade now.
Occasionally, there are unavoidable upgrades that need to happen to application code, to move from one version to the next.

The most recent example of this is the migration from Spring Boot 3 to Spring Boot 4 (the foundation on which my framework is based), where multiple breaking changes are part of the upgrade.
This migration has its own [migration guide](https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-4.0-Migration-Guide) which outlines all the breaking changes, but I decided at the same time to bundle in a couple of other breaking changes;
in for a penny, in for a pound.

For this, and changes in the past, I have written a migration guide which is very similar to [this one by the Snowflake Terraform Team](https://github.com/snowflakedb/terraform-provider-snowflake/blob/main/MIGRATION_GUIDE.md).
I outline any breaking changes, plus I give `before` and `after` examples of the code snippets in question.

And, as it turns out, this is an excellent foundation on which to direct LLMs in doing automated upgrades.

## The Prompt

> [!NOTE]
> I am by no means an expert in this, and I am positive that better prompts exist.

Here is the prompt I have been using:

> You are a software engineer responsible for upgrading this Maven application.
>
> The upgrade is described in this document https:\/\/github.com/.../v1_to_v2.md which can be accessed using the GitHub MCP server.
>
> Assume that the 'JFrog Maven Settings' and 'JFrog Docker Login' steps have already been completed by myself.
>
> Undertake the upgrade steps.
>
> Start by running 'git pull' to ensure you have the latest changes from the remote.
> Then create a new branch, as described in the migration guide.
>
> If anything is unclear (for example version numbers) then you must ask me for input before making changes.
>
> Do not, under any circumstances, commit any code or push anything to GitHub.
>
> Use version 0.3.2 as the new version of the Java Management Parent pom.
>
> "The framework" is currently unreleased, and this work is part of our preparations for its release.
> Use version 2.0.0-SNAPSHOT as the version of "the framework".

## Breakdown

Let's break down this prompt to see why each section exists.

### Cosplay

> You are a software engineer responsible for upgrading this Maven application.

I do love having to start every prompt like this.
It makes sense because LLMs are designed to mimic generalists.
Which hat are we supposed to be wearing today?

### The Guide

> The upgrade is described in this document https:\/\/github.com/.../v1_to_v2.md which can be accessed using the GitHub MCP server.

I started with only the first part of this line; telling the LLM where to download the migration guide from.
However, it was hit-and-miss that it would figure out the document was behind my companies Single-Sign-On login for our GitHub enterprise organization.

So I had to encourage it to use the authenticated GitHub MCP server for access to the repository.

Interestingly older models just 'made up' their own migration guide if they couldn't get access, but Claude Sonnet 4.5 does a better job at realizing that it shouldn't freestyle and asks for support.

### Ignore Set-Up

> Assume that the 'JFrog Maven Settings' and 'JFrog Docker Login' steps have already been completed by myself.

Part of my latest upgrade guide is to switch to a central [JFrog](https://jfrog.com/) artefact repository.
This tells the LLM to skip those steps because it was doing a poor job of realizing they had been done before (maybe because the files in question are outside the repo).

We often upgrade many applications at a time, so these steps are done by the second one we get to.

### Lift Off

> Undertake the upgrade steps.

Let's do this.

### Revision Control

> Start by running 'git pull' to ensure you have the latest changes from the remote.
> Then create a new branch, as described in the migration guide.

Now, when working on a repository, an engineer realizes over time that they need to run a `git pull` before they start working.
But, with me being an Architect now, I am becoming rusty, so I placed these lines in because I kept forgetting to do it.

### Pair Programming

> If anything is unclear (for example version numbers) then you must ask me for input before making changes.

I have spent many credits where an LLM has just spiralled off, making assumptions instead of doing what a Junior Engineer would do, and ask for clarification.

> Do not, under any circumstances, commit any code or push anything to GitHub.

I still do not trust VS Code, and it's command allow-list functionality.
This is mostly here so that I can pretend I'm not to blame (see my intro).

### Versions

> Use version 0.3.2 as the new version of the Java Management Parent pom.
>
> "The framework" is currently unreleased, and this work is part of our preparations for its release.
> Use version 2.0.0-SNAPSHOT as the version of "the framework".

And the final part, as I go through upgrading applications, I place the versions of released/unreleased libraries here.

Claude Sonnet 4.5 does a good job of checking for updated versions &mdash; assuming your upgrade guide links to where new versions can be found &mdash; and stopping to ask when it cannot determine what version to use.

This block just streamlines the process.

I also added the 'this work is part of our preparations for its release' to stop Claude asking if I was sure I wanted to use a SNAPSHOT (unreleased) version.

## Documentation

I've known for years that barely any of the engineers I work with actually read these upgrade guides.
If they do, they mostly skim them, missing important details.

I am wholly, and have always been, firmly in the camp of comments and documentation being mandatory.
This has frequently made me quite unpopular, mostly with junior engineers.
The idea that you will remember your code, and 'jump back in' was always (in my opinion) a dumb one.

> Always code as if the guy who ends up maintaining your code will be a violent psychopath who knows where you live.
>
> &mdash; John F. Woods

I find it quite amusing that these widely dismissed artefacts have now found another home and have 'become useful again'.
I hope that rise of LLMs has put to bed the idea that code is 'self describing'; that comments in code and documentation are a 'waste of time' (but I won't hold my breath).

Without these comments, and these documents, I frequently see an LLM smashing a rock against a coconut in an attempt to get anything to work.
The upgrade guides keep it on track about what might actually be the issue.

I personally still refuse to let LLMs write the documentation and upgrade guides for me, beyond prompting as to what sections would be useful.
LLM generated documentation is lifeless and frequently rambling, and I still get frequent comments that my writing style is engaging and concise.

Sure, you could run an LLM over all of these blogs and reproduce my writing style very closely, but I maintain that if someone couldn't be bothered to write it, why should I read it.

Maybe the future we are heading for is one where the vast [majority of documentation](https://www.independent.co.uk/tech/ai-author-books-amazon-chatgpt-b2287111.html) is all made by LLMs, read by LLMs, and we are finally reduced to being the consumers of summaries alone.

I hope not.
