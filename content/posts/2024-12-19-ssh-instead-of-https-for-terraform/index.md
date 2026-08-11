---
title: "Use ssh instead of https for Terraform modules"
date: 2024-12-19 22:39:00 +0100
last_modified_at: 2024-12-22 10:57:13 +0000
categories: [code]
tags: [github, terraform]

summary: Redirect your `http` Terraform modules to connect over `ssh` instead.
---

When you use Terraform modules that are hosted on GitHub, you tend to set up the module reference with `https` as the protocol because you can use an auth token in CI/CD.
This then requires you to use a Personal Access Token when working locally.
What if you could use ssh instead?

There are several environmental factors that required me to use this solution:

1. My business is using a [GitHub Organisation](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/about-organizations#about-organizations)
2. Access to this Organisation is federated with our businesses Active Directory
3. We are hosting repositories containing Terraform modules in the private organisation
4. I don't want to use 'Personal Access Tokens' because I have a perfectly good ssh key

My organisation have set up your modules to look like so:

```hcl
module "my_module" {

  source = "git::https://github.com/[org]/[project].git?ref=v1.2.3"

  // variables
}
```

This is fantastic for a fully GitHub ecosystem, but when I try to run `terraform get` on my laptop &mdash; so IntelliJ can resolve the required variables for the module &mdash; Terraform prompts me for my GitHub username/password:

```console
$ terraform get
Downloading git::https://github.com/[org]/[project].git?ref=v1.2.3 for my_module...
Username for 'https://github.com':
Password for 'https://pwhittlesea@github.com':

Error: Failed to download module

Could not download module "my_module" source code from "git::https://github.com/[org]/[project].git?ref=v1.2.3": error downloading
remote: Support for password authentication was removed on August 13, 2021.
remote: Please see https://docs.github.com/en/get-started/getting-started-with-git/about-remote-repositories#cloning-with-https-urls for information on currently recommended modes of authentication.
fatal: Authentication failed for 'https://github.com/[org]/[project].git/'
```

When you head over to the [documentation](https://docs.github.com/en/get-started/getting-started-with-git/about-remote-repositories#cloning-with-https-urls) you are recommended to use a 'Personal Access Token' to download the HTTPS module.

I _could_ create a Classic Personal Access Token and configure SSO to authorise it for my organisation, but given I already have my ssh key configured, why don't I use that instead?

If I add the following to `~/.gitconfig` then when downloading each module, Terraform will switch out the `https` for `ssh`:

```ini
[url "ssh://git@github.com"]
    insteadOf = https://github.com
```

Now when I run `terraform get`:

```console
$ terraform get
Downloading git::https://github.com/[org]/[project].git?ref=v1.2.3 for my_module...
- my_module in .terraform/modules/my_module
```

Success!
