RSS Catalog
-----------
RSS catalog is a collection of RSS feeds of articles organized in a machine-readable way.

In order to meaningfully organize articles, we must describe them somehow. This project aspires to be fairly objective (about as objective as, say, Wikipedia). It's better to have a description that is somewhat true than no description at all. For example, it's more useful to describe the New York Times as left-of-center in America than to argue about what should count as left-of-center in America.

What goes in this collection?
-----------------------------
There are a lot of sticky definitions here, so at some point we'll need to fall back to "good judgment."

### Articles
A valid article is an HTML page that you would describe as an "article". It should have 1000 or more non-whitespace characters of *content*. This excludes ads, navbars, hidden text and other things that aren't content. The meat of an article should be text. Pages that primarily feature images, video, or other multimedia content aren't articles.

### RSS Feeds
A valid RSS is one where >= 50% of items are valid articles.

Project structure
-----------------
Each subdirectory contains a README pertaining to that subdirectory.

`build` contains the organized collection of RSS feeds
`python` contains Python scripts that convert our inputs into fully-built outputs
`resources` contains data files that are fed into the Python scripts
