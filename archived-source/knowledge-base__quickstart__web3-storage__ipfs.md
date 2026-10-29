# IPFS

{% hint style="info" %}
**What is IPFS?**

IPFS is an abbreviation for Inter Planetary File System. In essence, as the name suggests, IPFS is a file system designed for the storage of various types of files. It functions vastly differently from the regular file systems that one might be used to.

Here, the phrase "Inter Planetary" is a play on words that symbolises the decentralised character of this file system. Decentralization being a core value of Web3 technology makes IPFS a good fit and has therefore received wide adoption.
{% endhint %}

A good introduction to IPFS in video format can be found here:

{% embed url="<https://www.youtube.com/watch?v=5Uj6uR3fp-U>" %}

### A Decentralized Peer-to-Peer Network

Traditionally, in Web2.0, files are stored on centralized servers, centralized in this setting means that these servers are owned by specific entities, companies and individuals. Although users can view and interact with that data via the web, they are always reliant on this central authority to serve that data.

Instead of relying on such a centralized approach to file storage, IPFS uses a decentralized approach that distributes files over a network of nodes - where these nodes are simply the machines of the users that choose to participate in the network.

Moreover, in this setting, each user's device on the network is both a client and a server. This is in contrast to the client-server model where users connect to a central server to request data. With IPFS, users can request and share data directly with each other. Peers on the network collaborate to share and distribute files, creating a more resilient and scalable system.

### Content Based Addressing

Traditionally, when requesting a file from a server we are essentially asking the server to retrieve his file from a certain location by means of an address (urls basically), this is known as location based addressing.

Instead of location based addressing, IPFS makes use of content based addressing. This is because the same file could be stored on several nodes throughout the network, hence we would simply need to retrieve that file from one of these nodes. In this case it doesn't matter where the file comes from, simply that the correct file is requested. This can be done by assigning a unique identifier (a hash essentially) to each file on the network.

Files and all of their versions are uniquely identified using content-addressed hyperlinks, meaning that the content of a file is used to generate its unique identifier (hash). This hash is then used to locate the file on the IPFS network. This hash isn't generated at random, but rather is derived from the data itself, meaning that the data predicates what this hash will look like, making it such that there is a 1-to-1 mapping between the hashes and the files.

Having the hash derived from the data itself has several inbuilt advantages:

1. **Security**: when requesting a file by its hash, the data needs to match the hash otherwise it is not valid. This makes it such that Files can't be tampered with by actors on the network.
2. **Deduplication**: If two files are identical, they will produce the same hash, meaning that there is no reason to store the file a second time.
3. **Immutability**: Once a file is added to IPFS and given a hash, the content cannot be changed. If you modify the file, you create a new hash. This ensures data integrity and allows anyone to verify that the content they retrieve matches the expected hash.
4. **Versioning:** The technical details of how this is implemented are beyond the scope of this resource, but IPFS also makes it easy to update files by providing a versioning system. Every change to a file results in a new identifier, allowing for easy versioning and tracking of changes, where the new file adds a pointer to the previous one.

### Downsides of IPFS

While IPFS has many advantages and innovative features, it's important to be aware of some potential downsides and challenges associated with the technology. Some of them are:

1. **Content Availability:** most notably the biggest flaw of IPFS, for files to be available on the network, there needs to be at least a single node hosting that file and making it available. If this node for some reason goes offline, as a consequence, the files that are only hosted by this node also become unavailable.
2. **Speed:** The speed at which you can retrieve content from IPFS depends on the popularity of the content and the number of nodes (peers) hosting it. Less popular content might take longer to retrieve, and some content may not be available if there are not enough nodes hosting it.

One countermeasure to content becoming unavailable is "pinning" (from the verb to pin), where the IPFS network is explicitely instructed to retain a specific piece of content regardless of it being accessed by nodes or not. There are certain dedicated services for this purpose than can automate this pinning process, such as ClubNFT, but can equivalently be done from your own local machine, which would require a little setup however.

### How does IPFS integrate into fxhash?

IPFS is often used for various applications, including decentralized websites, file sharing, and data distribution. It aims to create a more resilient and censorship-resistant internet by changing the way data is stored and retrieved, making it less dependent on centralized servers, thus making it a popular solution in that regard.
