---
title: "ONCHFS"
source: https://docs.fxhash.xyz/knowledge-base/quickstart/web3-storage/onchfs
archived: https://web.archive.org/web/20260411150038/https://docs.fxhash.xyz/knowledge-base/quickstart/web3-storage/onchfs
captured: 2026-04-11
---
# ONCHFS

> [!NOTE]
> **What is ONCHFS?**
>
> ONCHFS stands for On-Chain File System. ONCHFS is a permissionless unix-like content-addressable file system fully stored on-chain designed to be delivered through the http protocol, with cross-blockchain compatibility and extensibility in mind.

That's a lot to take in at once, let's address each point individually:

1. **Permissionless**: Anyone can write data, create files & directories, & reference files stored on the file system.
2. **Unix-like**: this simply means that onchfs is inspired by the unix-file system, where data is organized in a hierarchical tree-like structure of directories and files.
3. **Content Addressable**: content is addressed by unique identifiers derived from the data itself.
4. **On-Chain**: files are entirely stored on the blockchain, making them immutable and persistent as long as the respective blockchain is alive.
5. **Designed for the http protocol**: the ONCHFS protocol makes it possible to address and retrieve the stored assets with the http protocol that powers the modern web.
6. **Cross-Blockchain**: ONCHFS works on any chain, and files stored on one chain can reference files stored on other chains.
7. **Extensibility**: ONCHFS is built in such a manner that it can easily be extended and other technologies to be built on top of it.

ONCHFS is inspired by [ethfs](https://github.com/holic/ethfs), [ipfs](https://ipfs.tech/), [bitcoin ordinals recursive inscriptions](https://docs.ordinals.com/inscriptions.html), [Unix filesystem](https://en.wikipedia.org/wiki/Unix_filesystem), and aims at providing a general framework for working with files stored on-chain, following modern standards & practices.

Link to revdancatt’s vid

#### Why store files on-chain?

Before we dive into the specifics: why would we want to store files fully on-chain?

Ever since NFTs have become more popular, the on-chain vs. off-chain discussion has become more and more heated. One cherished aspect of blockchain technology is longevity, security, and immutability, especially when it comes to transactions which play a big role in making generative art as collectible digital tokens possible. In the previous page, we’ve covered the IPFS storage solution, which has characteristics that closely align with Web3 technology, in turn making it a popular solution for storing content and data in the setting of NFTs. Towards the end, we learn that it also introduces an element of impermanence, which requires additional effort from artists, collectors, and platforms to ensure the availability of the content.

This could in theory all be solved by storing files directly on-chain. But there are two problems that come in tandem with this approach, firstly, the high cost of uploading and eternalizing large data loads on digital ledgers, and secondly, the absence of a good system or protocol for this purpose.

In the setting of generative art, the first problem solves itself - the actual image data (that represents the art) doesn’t need to be stored directly on the blockchain, merely the code that can generate the art. Code being simply a bunch of alphanumeric symbols, is highly compressible and can be shortened enough to not introduce exorbitant minting costs. The second problem is addressed by ONCHFS which is introduced in greater detail in what follows.

Overall, storing files on-chain is preferred by many because it is considered a purer and more persistent method for storing files that ensures the existence thereof for as long as the blockchain exists. And for the popular blockchains there is no worry for them to simply disappear overnight.

#### What problems does ONCHFS solve?

Previous attempts at on-chain storage solutions have had some inherent problems that ONCHFS tries to address. For instance, in the context of generative art projects that come in the form of self-contained web projects which the browsers can run, existing solutions don't actually fully store the entirety of the projects on the blockchain, but rather only a part of them - generally the code that creates the artwork. Generally, this code is minified and compressed into a string for it to be efficiently stored on the blockchain.

This is problematic however, because it makes it such that platforms often need to implement an additional off-chain step to reconstruct the project as a whole for it to actually run in the browser. The javascript code that generates the artwork can't run in a vacuum and needs additional files to be complete, such as an html document that serves as an entry point, a stylesheet to specify its appearance in the browser, and additional other javascript libraries that it makes use of and builds upon.

Recreating this project structure is referred to as html-reconstruction where the platform creates the index entry point that serves and displays the project in the browser. Additionally the platform needs to provide and host a specific list of dependencies that the project requires to function properly, this doesn't align with the decentralised ethos of Web3.0.

ONCHFS solves both of these issues, projects are entirely stored on-chain such that no html reconstruction step is required. Additionally libraries, dependencies, and other assets can also be freely created by users, making it possible for anyone to reference them. In this manner, it liberates code artists in their creative endeavours, ensures longevitiy of projects stored with ONCHFS, and opens the door for interesting and creative projects that make use of this on-chain file storage paradigm.

#### How does ONCHFS work?

ONCHFS is designed for the purpose of preserving the integrity and longevity of generative art projects, making it excel in that regard. The ONCHFS protocol ensures that uploaded projects are delivered in a 1:1 format, without requiring any additional steps to reconstruct the original project.

It also handles project dependencies in an elegant manner. Storing files in a content addressable manner, where each file has a unique identifier derived from the data itself (we cover this in a bit more detailed manner in the page on IPFS), makes it possible to detect if a library already exists on-chain. In this case, the library doesn't need to be re-uploaded a second time, and it will automatically link the already existing stored version. ONCHFS handles this by creating the content ids at upload time.

This introduces a paradigm of trustless and fully open resources sharing, as no one has to rely on a centralized platform to provide a library, or a set of personal tools they keep reusing over time; if they upload it once, it will become available forever for free for everyone using onchfs.

**What's more, is that the resources stored with ONCHFS are http compliant.**

\<aside> \<img src="<https://prod-files-secure.s3.us-west-2.amazonaws.com/f9d1e984-50ed-4650-a543-95d2b6c0ba90/015a834d-6092-42a9-a3c6-6ede37149fdd/fx_doc-icon_info_001.png>" alt="<https://prod-files-secure.s3.us-west-2.amazonaws.com/f9d1e984-50ed-4650-a543-95d2b6c0ba90/015a834d-6092-42a9-a3c6-6ede37149fdd/fx_doc-icon_info_001.png>" width="40px" /> **What is http?**

HTTP, or Hypertext Transfer Protocol, is the foundation of data communication on the World Wide Web. HTTP facilitates the transmission of various types of data, including text, images, and multimedia, using a request-response model. When a user enters a web address or clicks on a link, the browser sends an HTTP request to the server, specifying the desired resource. The server then processes the request and returns an HTTP response, containing the requested data or an error message.

\</aside>

This means that when files are uploaded to ONCHFS, they are also formatted in an http compliant format that can be transferred by means of the protocol. Naturally, the artist/user uploading to ONCHFS doesn't need to worry about any of this, it is automatically handled ia the fxhash minting interface. It is possible however to also manually interact with ONCHFS.

A complete documentation of ONCHFS can be found here:

[Hello from ONCHFS — On-Chain for Http File System | ONCHFS — On-Chain for Http File System](https://onchfs.com/docs/intro)

#### Chain Agnostic

One innovative aspect of ONCHFS is that it can be used to store files on any blockchain, without having their existence isolated and restricted to that particular chain. This means that a file on the one chain can reference files stored on other chains.

This can become useful if there is a need to use a cheaper blockchain for storing bigger chunks of data to be accessed more expensive blockchain. While not a typical scenario, it's worth noting the built-in onchfs support for such cases.

#### Limitations

The main limitation of ONCHFS is that it is a relatively new method for storing files on-chain, meaning that it isn't as widely adopted as other decentralized storage solutions such as IPFS. With fxhash growing as a platform and community and with more files being stored with ONCHFS it is likely to become adopted by other platforms that would like to display these generative art projects
