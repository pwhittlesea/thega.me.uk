---
title: "Project Decomposition"
date: 2024-07-21 12:00:00 +0000
last_modified_at: 2024-10-21 20:30:48 +0000
categories: code
tags: [engineering]
---

As an architect, I frequently assist software engineers in breaking down project scope into manageable chunks.
Here is one of the techniques I use.

<!--more-->

<!-- markdownlint-disable MD028 -->

> [!INFO] Update 2024/07/25
> So this process should be called 'User Story Mapping' and is featured in its own [O'Reilly book](https://www.oreilly.com/library/view/user-story-mapping/9781663728661/) by Jeff Patton and Roy McCrerey.
>
> I struggled to find anything about it because I did not know the correct name.
> But now I do, I have found lots of _far_ better blogs out there on this process (e.g. [1](https://www.easyagile.com/blog/the-ultimate-guide-to-user-story-maps/), [2](https://plan.io/blog/user-story-mapping/) and [3](https://www.nngroup.com/articles/user-story-mapping/)).
>
> There is also a [video](https://www.youtube.com/watch?v=AorAgSrHjKM) featuring one of the authors of the book.
>
> In fact, this blog probably now only serves as a writing exercise :smile:.
> I plan on buying and reading the book so I can correct all the terminology on this page.

> [!INFO] Original 2024/07/21
> :blue_heart: I do not know the origin of this process, but if you do, let me know so I can attribute it correctly.

<!-- markdownlint-enable MD028 -->

## Why do we need decomposition?

When given a new project, it's very easy for a team to balk at the full scope of what they are being asked to achieve.

> You want us to build a social media site for ducks?
> From scratch?
> That's going to take years!
>
> &mdash; The Engineering Team

Any project of sufficient size will need to be broken down into tasks for the team to work on; but where do you start?

I have spent over a decade delivering projects in teams that follow [the agile manifesto](https://en.wikipedia.org/wiki/Agile_software_development) and I have used this process for many years, but I believe this will also help in other delivery styles as well, particularly [waterfall](https://en.wikipedia.org/wiki/Waterfall_model).

## The Process

### Step 1 - Feature Enumeration

Get the engineers to enumerate the aspects/features of what you want to build.
These don't have to be detailed, because at this stage you almost definitely don't know the full scope of what you are building or how the technology involved actually functions.

In our example above we are making a social media site for Ducks.
This will almost certainly require a Front end with Javascript and CSS, but will also need a collection of back end APIs[^1] to power it.

[^1]: Technically all protocols are APIs but we all use API to mean HTTP Request/Response APIs

Write these aspects down as columns of a table, lets focus on just the back end APIs;

<!-- markdownlint-disable MD033 -->
<table>
<thead>
<tr>
<th style="text-align:center">Post APIs</th>
<th style="text-align:center">User Settings APIs</th>
<th style="text-align:center">Authentication</th>
<th style="text-align:center">Threat Protection</th>
<th style="text-align:center">Logging</th>
</tr>
</thead>
<tbody>
</tbody>
</table>
<!-- markdownlint-enable MD033 -->

Here we have a couple of randomly selected aspects of the APIs (for very large projects I've seen ~100 columns):

- Post APIs - support the users Posts pages
- User Settings APIs - support the user's Settings page
- Authentication - Checking the caller is who the caller says they are
- Threat Protection - We have lots of competitors who want to see us fail, how do we make sure they don't break our service?
- Logging - What logs should our back end create?

Teams will not manage to put everything here first time, as they work through this process they will discover more.

> [!WARNING]
> This is a good time to remember all of those other business systems your application needs to integrate with (like Salesforce)

### Step 2 - Slicing

Take each column and write down slices of that aspect, each increasing in value and complexity:

<!-- markdownlint-disable MD033 -->
<table>
<thead>
<tr>
<th style="text-align:center">Post APIs</th>
<th style="text-align:center">User Settings APIs</th>
<th style="text-align:center">Authentication</th>
<th style="text-align:center">Threat Protection</th>
<th style="text-align:center">Logging</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center">None</td>
<td style="text-align:center">None</td>
<td style="text-align:center">None</td>
<td style="text-align:center">None</td>
<td style="text-align:center">None</td>
</tr>
<tr>
<td style="text-align:center">List</td>
<td style="text-align:center">View</td>
<td style="text-align:center">Fixed API Key</td>
<td style="text-align:center">IP Allow List</td>
<td style="text-align:center">Container</td>
</tr>
<tr>
<td style="text-align:center">Create</td>
<td style="text-align:center">Edit</td>
<td style="text-align:center">Generated Keys</td>
<td style="text-align:center" markdown="span">WAF</td>
<td style="text-align:center">Elasticsearch</td>
</tr>
<tr>
<td style="text-align:center">Delete</td>
<td style="text-align:center">Delete Account</td>
<td style="text-align:center">OAuth Tokens</td>
<td style="text-align:center">AWS Shield</td>
<td style="text-align:center">Archive</td>
</tr>
<tr>
<td style="text-align:center">Edit</td>
<td style="text-align:center"></td>
<td style="text-align:center"></td>
<td style="text-align:center"></td>
<td style="text-align:center"></td>
</tr>
</tbody>
</table>
<!-- markdownlint-enable MD033 -->

If we take column 1 'Post APIs' as an example.
The team could deliver no APIs related to posting.
Then they could deliver an API which allows you to list posts.
Then they could deliver an API which supports listing and creating, and so on.

These slices help the team understand how they can build up to the final solution but **not all slices will need to be delivered**.
Some of the slices will never be needed, like 'Edit' in 'Post APIs'.
We might just decide that we want users to have to delete then re-create posts when they spell something wrong.

At this point the team can take a look at the content in the columns and see if any of them need to be expanded upon.

Now we have the aspects above we can perform the next step; defining the MVP.

### Step 3 - Minimum Viable Product (MVP)

> The minimum viable product, or MVP, is the simplest version of a product that you need to build to sell it to a market.
>
> &mdash; [Atlassian](https://www.atlassian.com/agile/product-management/minimum-viable-product)

Which slices of each aspect/feature do we need to deliver before we can say we have an acceptable product we can put out into the world.
This might form the first Task/Story/Epic for the team, depending how big the project is.

In my opinion this is the most powerful output of this process; a team being able to _visualise_ when they reach one of the biggest milestones of any delivery.

Obviously this is going to take lots of work with the Product Owner to decide what we do/don't need to do to get to this milestone.

<!-- markdownlint-disable MD033 -->
<table>
<thead>
<tr>
<th style="text-align:center">Post APIs</th>
<th style="text-align:center">User Settings APIs</th>
<th style="text-align:center">Authentication</th>
<th style="text-align:center">Threat Protection</th>
<th style="text-align:center">Logging</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center">None</td>
<td style="text-align:center">None</td>
<td style="text-align:center">None</td>
<td style="text-align:center">None</td>
<td style="text-align:center">None</td>
</tr>
<tr>
<td style="text-align:center">List</td>
<td style="text-align:center">View</td>
<td style="text-align:center">Fixed API Key</td>
<td style="text-align:center;border-bottom:5px solid red">IP Allow List</td>
<td style="text-align:center;border-bottom:5px solid red">Container</td>
</tr>
<tr>
<td style="text-align:center;border-bottom:5px solid red">Create</td>
<td style="text-align:center;border-bottom:5px solid red">Edit</td>
<td style="text-align:center;border-right:5px solid red">Generated Keys</td>
<td style="text-align:center">WAF</td>
<td style="text-align:center">Elasticsearch</td>
</tr>
<tr>
<td style="text-align:center">Delete</td>
<td style="text-align:center">Delete Account</td>
<td style="text-align:center;border-left:5px solid red;border-bottom:5px solid red;border-right:5px solid red">OAuth Tokens</td>
<td style="text-align:center">AWS Shield</td>
<td style="text-align:center">Archive</td>
</tr>
<tr>
<td style="text-align:center">Edit</td>
<td style="text-align:center"></td>
<td style="text-align:center"></td>
<td style="text-align:center"></td>
<td style="text-align:center"></td>
</tr>
</tbody>
</table>
<!-- markdownlint-enable MD033 -->

Here, the team can say that they need to support listing and creating posts, before they can say they are ready to go to market.
Similarly they _need_ to have an API that allows editing user settings, but **not** an API that allows account deletion (for now, users can email us to get their account deleted).
Again, the engineers need to be able to see container logs, but for now we can deal with them not being archived or aggregated into Elasticsearch.

Hopefully by this point the team are beginning to get an idea of _what_ they need to build.

### Step 4 - Minimum Loveable Product (MLP) [optional]

> A Minimum Lovable Product (MLP) is an initial offering that users love from the start.
> It represents the minimum that is required for customers to adore a product, rather than merely tolerating it.
>
> &mdash; [Aha](https://www.aha.io/roadmapping/guide/plans/what-is-a-minimum-lovable-product)

If we think back to our MVP, we said that we will not allow users to delete their posts if they make a mistake.
This is not a very enjoyable experience for the users, but they _might_ tolerate it.
If we want our users to really _love_ our product we are going to have to deliver more than just the bare minimum.

Time for another line.

<!-- markdownlint-disable MD033 -->
<table>
<thead>
<tr>
<th style="text-align:center">Post APIs</th>
<th style="text-align:center">User Settings APIs</th>
<th style="text-align:center">Authentication</th>
<th style="text-align:center">Threat Protection</th>
<th style="text-align:center">Logging</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center">None</td>
<td style="text-align:center">None</td>
<td style="text-align:center">None</td>
<td style="text-align:center">None</td>
<td style="text-align:center">None</td>
</tr>
<tr>
<td style="text-align:center">List</td>
<td style="text-align:center">View</td>
<td style="text-align:center">Fixed API Key</td>
<td style="text-align:center;border-bottom:5px solid red">IP Allow List</td>
<td style="text-align:center;border-bottom:5px solid blue">Container</td>
</tr>
<tr>
<td style="text-align:center;border-bottom:5px solid red">Create</td>
<td style="text-align:center;border-bottom:5px solid red">Edit</td>
<td style="text-align:center;border-right:5px solid red">Generated Keys</td>
<td style="text-align:center;border-bottom:5px solid blue;border-right:5px solid blue">WAF</td>
<td style="text-align:center">Elasticsearch</td>
</tr>
<tr>
<td style="text-align:center;border-bottom:5px solid blue">Delete</td>
<td style="text-align:center;border-bottom:5px solid blue">Delete Account</td>
<td style="text-align:center;border-left:5px solid red;border-bottom:5px solid blue;border-right:5px solid blue">OAuth Tokens</td>
<td style="text-align:center">AWS Shield</td>
<td style="text-align:center">Archive</td>
</tr>
<tr>
<td style="text-align:center">Edit</td>
<td style="text-align:center"></td>
<td style="text-align:center"></td>
<td style="text-align:center"></td>
<td style="text-align:center"></td>
</tr>
</tbody>
</table>
<!-- markdownlint-enable MD033 -->

We can now see a couple of things playing out:

1. We want our customers to be able to delete their mistakes, so 'Delete' under 'Post APIs' is now included.
2. We also want our support team to love us; so instead of handling hundreds of 'Please delete my account' emails, we will let customers do it themselves.
3. Having to provide an IP address is incredibly impractical for {{< term "B2C" >}} applications as most customers do not know how do get, or even what an IP address is. IP allow lists are good for getting started but a {{< term "WAF" >}} will help us reach more customers by being internet accessible.

## Summary

Hopefully the above, admittedly convoluted, example helps you understand this process of decomposition.

It should help the team gain some confidence that the project that awaits them is not, in fact, impenetrable.

It should also help the team convert upcoming cards into technical activities, as well as knowing if something needs to be extensible for future slices.
I have even seen teams use this process to schedule spikes into their sprints, to try out prototyping upcoming features that need to be built.

I will admit it blurs the lines of an 'agile project' because it relies on knowing the 'end state' of the project.
But in my (arguably limited) experience, no project is so blurry that you don't know the general goals of the customer.
That, and we are not wasting too much time on this process, we are only discussing what features _could_ exist.

## Parting Thoughts

1. Try and do this collaboratively.
   Every member of the team member should be present.
2. Whiteboards are my go to for anything like this, but this requires a co-located team who can come to the office.
   A shared space like a Confluence page/Word document will do.
3. This is a living document.
   Change it as you see fit throughout the project.
   Security team changed their systems, so now you need to push logs into Azure Sentinel?
   Add a slice.
4. There is no limit on how many lines you should draw.
   I've seen teams do one-per-card.
   I've seen teams do one-per-project.
   This is a resource for the team, by the team.
5. Don't force it if you don't need it.
