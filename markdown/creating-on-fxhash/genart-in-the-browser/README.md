---
title: "Genart in the Browser"
description: "An overview of the different methods with which graphics can be rendered to the browser."
source: https://docs.fxhash.xyz/creating-on-fxhash/genart-in-the-browser
archived: https://web.archive.org/web/20260311120914/https://docs.fxhash.xyz/creating-on-fxhash/genart-in-the-browser
captured: 2026-03-11
---
# Genart in the Browser

*An overview of the different methods with which graphics can be rendered to the browser.*

fxhash projects are web based generative artworks that display graphics in the browser. We’ve now had a look at all of the tools that fxhash provides to facilitate this endeavour, and also had a look at the fxhash API that provides helper functions to create a compatible generative artwork. Now we still need to discuss some notions that are related to developing a robust generative artwork, that displays itself properly in the canvas, works across different browsers, and implements some user friendly features. These things aren’t directly related to fxhash, but are quite important to get right.

In the following sections we will discuss some of the important notions involved in the creation of a generative artwork for fxhash:

### [Canvas Element & API](canvas-element-and-api.md)

The canvas API and the function that it exposes.

### How to use Libraries

Including and working with 3rd party libraries.

### [Responsive Browser Projects](responsive-browser-projects.md)

Approaches for creating responsive and resizeable art in the browser.

### [Deterministic Randomness](deterministic-randomness.md)

Using PRNGs correctly and pitfalls to avoid.

### [User Input & Media Export](user-input-and-media-exports.md)

Handling user inputs and how to export your art in various formats.

### [Testing Browser Compatibility](testing-browser-compatibility.md)

Testing your code's compatibility with the different modern browsers.

There are primarily two technologies to create graphics in the browser, they are:

- **The HTML Canvas:** the html canvas element is a rectangular bitmap area (essentially a raster/grid of pixels) that can be displayed within an HTML page, and allows the control over individual pixels via javascript. It comes with an attached rendering context that provides several useful functions for drawing to that canvas. Most modern generative art makes use of this canvas element and its associated API. Furthermore, many libraries are built on top of this Canvas API that further facilitate the creation of graphics. We will talk in detail about this canvas element in the coming sections.
- **SVGs - Scalable Vector Graphics:** in contrast to the pixel based canvas element, scalable vector graphics are a resolution independent alternative to creating graphics in the browser. SVGs are based on XML and describes 2D graphics in a vector format. An SVG is essentially a document of shapes and paths that can be drawn, and the browser renders it as needed. There are also javascript libraries that facilitate the creation of these SVGs, and make it possible to make art with them, but it is overall a bit trickier than making art with the canvas element.
