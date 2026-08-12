---
title: "Bye-Bye GPG"
date: 2024-02-20 12:49:00 +0000
last_modified_at: 2024-10-21 20:30:48 +0000
categories: [code]
tags: [gpg, ssh, security, git]
summary: "So I have been using GPG to sign my Git commits for about 5 years now and every year, when my keys expire, it's a nightmare to renew the keys for another year. Here's how to set up SSH signing keys."
---

So I have been using GPG to sign my Git commits for about 5 years now and every year, when my keys expire, it's a nightmare to renew the keys for another year.

Now one option would be to make the keys last longer, but that would leave me with the same problem; it's non-intuitive and hard to renew GPG keys.

Add to that the fact that some systems (**cough** OSX) need additional software installed to give you a prompt for the password when you want to unlock the key.
It's just, annoying.

So recently, a blog from [Mendhak](https://code.mendhak.com/keepassxc-sign-git-commit-with-ssh/) pointed me at using SSH keys to sign your Git commits.
Colour me interested.
Maybe this could be easier than managing GPG keys.

Oh, it was everything I dreamed of...

There are many, many, many blogs on this topic.
There is event extensive documentation on [GitHub](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits).
But for my future reference, here are the steps.

Generate a signing key:

```sh
ssh-keygen -t ed25519 -C "your_email@example.com"
```

Add the new key to your SSH agent and get the fingerprint for signing:

```sh
ssh-add ~/.ssh/<key_location>
ssh-add -L
```

You should see something like:

```txt
ssh-ed25519 <fingerprint> your_email@example.com
```

Add (or create) a new allowed signers file:

```sh
echo "your_email@example.com ssh-ed25519 <fingerprint>" >>  ~/.ssh/allowed_signers
```

Set up Git to use the new key and signers file:

```sh
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/<key_location>
git config --global commit.gpgsign true
git config --global gpg.ssh.allowedSignersFile ~/.ssh/allowed_signers
```

Now when you run `git show --show-signature` on a signed commit you should see:

```txt
Good "git" signature for your_email@example.com with ED25519 key <fingerprint>
```

:boom: Done!
