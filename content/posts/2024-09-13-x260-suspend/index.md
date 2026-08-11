---
title: "My ThinkPad won't wake up"
date: 2024-09-13 21:23:00 +0000
last_modified_at: 2024-10-21 20:30:48 +0000
categories: [hardware]
tags: [thinkpad]
summary: "Last week I upgraded my ever-reliable Lenovo x260 ThinkPad to Ubuntu 24.04, and it would no longer wake up from a suspend state."
---

Last week I upgraded my ever-reliable Lenovo x260 ThinkPad to Ubuntu 24.04.

Somewhere in the hour long install process the installer asked me to replace my `/etc/default/grub` file with the default one in the installer.

I didn't remember updating this file, ever, so I accepted the defaults.

Isn't Ubuntu wonderful, I thought, major version updates are so smooth!
However, little did I know, that due to [a little documented issue](https://bugs.launchpad.net/ubuntu/+source/linux/+bug/2031969/) I would not be able to wake my laptop from a suspended state anymore.

When I close the lid, my laptop sleeps, never to be woken from its slumber; stirred only by the harsh application of a long-press of the power button to hard reset it.

My first guess at a cause was a bad upgrade, so I installed a fresh copy of 24.04, which yielded no love.

After a suspicion my hardware was no longer supported, I reinstalled 22.04 to little joy.

Maybe it was the boot drive encryption I dutifully enabled? No such luck.

After 3 fresh installs I scoured forums, until I came across [a comment](https://bugs.launchpad.net/ubuntu/+source/linux/+bug/2031969/comments/27) on the issue above:

> Simon Clift (ssclift-gmail) wrote 21 hours ago: #27
>
> I'm not sure exactly why, but this worked:
>
> [https://www.reddit.com/r/debian/comments/t03sd2/fresh_install_on_t460_laptop_wont_wake_after/](https://www.reddit.com/r/debian/comments/t03sd2/fresh_install_on_t460_laptop_wont_wake_after/)
>
> Change the /etc/default/grub command line to
>
> GRUB_CMDLINE_LINUX_DEFAULT="quiet splash intel_iommu=off"
>
> and my Thinkpad Carbon X1 (G4?) sleeps and wakes up as expected. I experienced the problem of not waking up after sleep on Ubuntu 22.04 and 24.04.

This rang a bell, had I changed this file before?
Maybe?

Anyway, a quick edit of my grub config file later and success!
My ThinkPad is usable again!

Thanks, Simon Clift, wherever you are!

```sh
# Added this in to help with not being able to resume from suspend
# https://bugs.launchpad.net/ubuntu/+source/linux/+bug/2031969/comments/27
# Run sudo update-grub after!
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash intel_iommu=off"
```
