---
title: "What is ONCHFS?"
description: "ONCHFS is a file storage system that improves security, interoperability, and flexibility for on-chain generative art."
source: https://docs.fxhash.xyz/onchfs/what-is-onchfs
archived: https://web.archive.org/web/20260311044836/https://docs.fxhash.xyz/onchfs/what-is-onchfs
captured: 2026-03-11
---
# What is ONCHFS?

*ONCHFS is a file storage system that improves security, interoperability, and flexibility for on-chain generative art.*

The idea for ONCHFS came together when fxhash geared up for it’s 2.0 launch in December of 2023. Alongside integrating fxhash into the Ethereum eco-system, we also wanted to provide artists with the possibility to store their projects fully onchain, as an alternative to the default IPFS based storage method. This led us to investigate the current state of onchain storage for genart projects, and how other platforms were doing it.

One common approach can be describe as ***html reconstruction***, which generally involves 2 things:

- JavaScript code proper to the project in question, uploaded as a string, and usually encoded, minified, and compressed in various ways.
- A list of dependencies pointing to scripts previously uploaded by a central entity. In most cases without the option for users to upload additional libraries for others to use in a convenient way.

The actual content is stored in a [Content-Addressable Store](https://en.wikipedia.org/wiki/Content-addressable_storage), and some logic is responsible for reconstructing the chunks of content into digestable files. Two notable projects towards that end are:

- [ethfs](https://github.com/holic/ethfs): general-purpose Content-Addressable Store + shared name-based file system
- [scripty](https://github.com/intartnft/scripty.sol): HTML reconstruction built on top of ETHFs

While this approach provides on-demand HTML reconstruction as long as a node is available, it presents strong disadvantages for what we would consider to be a long-lasting backbone for an open Generative Art ecosystem:

- **interferences on artistic practices**: artists have not only to think about implementing each platform API for their project to be compliant, but also they must obey to some predefined code structure as eventually their whole code is going to be one string
- **inter-operability between assets**: while file data is content-addressed, files are addressed by their name on the system; this introduces major inter-operability issues as user can never fully trust some name faily describe the data it contains
- **security, vector for Supply Chain Attacks**: users have to rely on central entities to provide a list of verified files, which in essence can be composed of any arbitrary data which can only be verified by querying and inspecting such file. This introduces a vector for injecting malicious code in what would seem to be a legit and trusted file (imagine embedding a wallet drainer which would trigger past a given date on a file named `processing-1.3.1.min.js`, yet exposing all the features of its valid counterpart). While this approach may work for centralized & semi-centralized platforms, if we want to build an open ecosystem where anyone can provide libraries for public access, such system cannot fully be trusted.
- **too specialised**: outside of HTML reconstruction, it becomes hard to extend current approaches for any kind of file-based application

ONCHFS aims at solving what we consider to be core issues, at a cost we consider to be negligable. To give a quick overview, our approach solves all the points above but requires a file resolver (which can be an http-proxy or a service worker).
