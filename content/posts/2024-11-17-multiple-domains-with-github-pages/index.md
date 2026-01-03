---
aliases:
  - "/code/multiple-domains-with-github-pages/"
title: "Multiple custom domains with GitHub Pages"
date: 2024-11-17 18:59:00 +0100
last_modified_at: 2025-04-27 11:49:52 +0000
categories: [code]
tags: [github, html]

summary: "I moved all of my domains to GitHub pages"
---

## Background

I own a couple of domains that are not the one you are on right now. At the time of writing I own four:

1. `thega.me.uk`
2. `pwhittlesea.com`
3. `pwhittlesea.co.uk`
4. `wedfest-2017.uk`

I've spent a while working on `thega.me.uk` as it's my main domain.
You could argue I use this domain name like a brand as it appears in my Email and other social media, such as my Bluesky handle.

I have not, however, spent any time working on the other three; leaving them to languish.

`pwhittlesea.com` and `pwhittlesea.co.uk` redirected to an [About Me](https://about.me) page, but _only_ on HTTP.
No HTTPS.
In the current day and age where TLS certificates are free, and browser settings such as Firefox's [HTTPS-Only Mode](https://support.mozilla.org/en-US/kb/https-only-prefs), this is not really acceptable anymore.

This 'About Me' page was super out of date as well &mdash; pre-dating my [original GitHub page]({{< ref "2024-02-17-new-beginnings" >}}) for this domain &mdash; so I had to update it eventually.

![My About Me](about_me_pwhittlesea.png)
{style="width: 50%;"}

The final domain, `wedfest-2017.uk`, was a site I built for my wedding back in 2017 (obviously).
It contained details of the day, and had a form allowing guests to RSVP.
It was a simple [S3 Hosted Website](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html) which was mostly built with Bootstrap and jQuery.

On brand, I never went back and updated it after the wedding day.

Unbeknownst to me, at some point in the last 7 years, the DNS nameservers stopped resolving.
So it had been broken for a long time.

## Requirements

After a bit of thought, I decided to target the following requirements:

1. I wanted to have my `pwhittlesea` domains redirect to `thega.me.uk`.
2. Have a single 'Project Closed' page on the `wedfest-2017.uk` domain.
3. Get TLS working for all 3 forgotten domains.
4. Most importantly, I didn't want to run any infrastructure.
5. Bonus: I didn't want to pay any ongoing costs.

This pointed me squarely at GitHub Pages.

Unfortunately you cannot have more than one custom domain on a repository, otherwise I would have added my `pwhittlesea` domains to this blog and had them all auto-redirect to `thega.me.uk`.

GitHub does allow you to have unlimited 'Project Sites' which normally show up as a sub-path of your main 'User Site' (e.g. `https://username.github.io/my-project-repo`).
You can however add a custom domain to them.

## Implementation

So today I have replaced `pwhittlesea.com` and `pwhittlesea.co.uk` with small GitHub Pages sites which do nothing except redirect to this site.
For each of my redirect domains I performed the following steps:

1. Create a new blank repository
2. Add a new file called `index.html` with the following content:

   ```html
   <!DOCTYPE html>
   <html lang="en">
     <head>
       <meta charset="utf-8">
       <title>Redirecting to https://thega.me.uk/</title>
       <meta http-equiv="refresh" content="0; URL=https://thega.me.uk/">
       <link rel="canonical" href="https://thega.me.uk/">
     </head>
     <body>
       <p>You will be redirected to thega.me.uk soon!</p>
     </body>
   </html>
   ```

3. Configure the DNS settings of the domain to have the correct `A`, `AAAA`, and `CNAME` records ([documentation here](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site#dns-records-for-your-custom-domain)).
   For me these looked like:

   | DNS record type | DNS record name | DNS record values     |
   | --------------- | --------------- | --------------------- |
   | A               | @               | 185.199.108.153       |
   | A               | @               | 185.199.109.153       |
   | A               | @               | 185.199.110.153       |
   | A               | @               | 185.199.111.153       |
   | AAAA            | @               | 2606:50c0:8000::153   |
   | AAAA            | @               | 2606:50c0:8001::153   |
   | AAAA            | @               | 2606:50c0:8002::153   |
   | AAAA            | @               | 2606:50c0:8003::153   |
   | CNAME           | www             | pwhittlesea.github.io |

4. Wait for the DNS to propagate.
5. In the settings tab of the repo, under `Pages`, select the main branch source (which enables pages) and input your custom domain.
6. Save and refresh the page.
   It's a bit temperamental, but GitHub should show you a green `DNS Check Successful` message.
7. (Optional) GitHub will also show you a box for the provisioning of the TLS certificate.
   Once complete, refresh and enable `Enforce HTTPS`

Then, when someone browses to the custom domain they are then redirected to the destination URL by the HTML shown above ([Meta Refresh](https://en.wikipedia.org/wiki/Meta_refresh)).

For my `wedfest-2017.uk` domain I have followed the same process, but I have modified the HTML to show a 'Project Closed' page.

## Downsides

So GitHub pages are free, but it does have two downsides that I have noticed.

The first issue is with the sub-paths.
I mentioned earlier that 'Project Sites' show up as a sub-path of your main 'User Site' where the path is the name of the repo you created.
Even with a custom domain, these sub-paths are still present.

<!-- markdown-link-check-disable-next-line -->
Right now you can go to [`https://thega.me.uk/pwhittlesea.com`](https://thega.me.uk/pwhittlesea.com), [`https://thega.me.uk/pwhittlesea.co.uk`](https://thega.me.uk/pwhittlesea.co.uk), and [`https://thega.me.uk/wedfest-2017.uk`](https://thega.me.uk/wedfest-2017.uk), which will redirect you to the custom domains (which might then redirect you back here).

This is not an issue for me because I have chosen to name my repositories after the domains themselves.
I think if you picked a more generic name it might conflict with some routing on your main site.

The second downside is speculative, but it's possible that users using the "Back" button on the final page may get sent back to the redirecting page, whereupon the redirect will occur again.
This may cause a reader to get "stuck".
