---
title: "Simple QR Code Command"
date: 2024-03-01 21:34:00 +0000
last_modified_at: 2024-10-21 20:30:48 +0000
categories: [code]
tags: [osx]
summary: "A simple function to create a QR code for a URL, so you can 'send' a link to your phone."
---

Sometimes you need to open a URL on your phone that you found on your company laptop, but there's no simple way to send it between the two devices.
This simple command allow you to turn a URL into a QR code you can scan on your phone.

For this to work you will need to install [`qrencode`](https://formulae.brew.sh/formula/qrencode):

```sh
brew install qrencode
```

Place the following in your `~/.bashrc` file:

```sh
function qr() {
  qrencode "$1" -o /tmp/qr.png; open /tmp/qr.png
}
```

Now you can run the following which will open a new QR code in Preview:

```sh
qr https://thega.me.uk
```
