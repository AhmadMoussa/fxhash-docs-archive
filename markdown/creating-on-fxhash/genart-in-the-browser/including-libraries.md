---
title: "Including Libraries"
description: "An overview of some of the popular libraries for creating generative art on fxhash."
source: https://docs.fxhash.xyz/creating-on-fxhash/genart-in-the-browser/including-libraries
archived: https://web.archive.org/web/20260311055049/https://docs.fxhash.xyz/creating-on-fxhash/genart-in-the-browser/including-libraries
captured: 2026-03-11
---
# Including Libraries

*An overview of some of the popular libraries for creating generative art on fxhash.*

While the Canvas API is already quite versatile, it can at the same time be a little clunky and hard to work with. In this section, we'd like to introduce some of the popular libraries that can be used to create various kinds of graphics in the browser and streamline certain approaches for making generative art.

### Including Libraries in your Project

> [!CAUTION]
> **Libraries cannot be linked as scripts that fetch an external URL**. Any library that you might use for your project needs to be included as standalone file inside of your project.

**Projects on fxhash cannot make any network requests.** This means that they cannot communicate with a server, nor send or fetch data over the internet. For example, we cannot fetch a library from a CDN like cdnjs or jsdelivr:

```html
<!-- this is not allowed -->
<script src="<https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.8.0/p5.js>"></script>
```

The reasons why this is not allowed:

- **It ensures the longevity of fxhash projects**: projects should be self contained bundles of code that can run independently of external resources.
- **A measure against malicious intent**: It prevents bad actors actors from building malicious fxhash projects intending to preform certain malicious actions on your device.

It is necessary that any libraries used in the project is included as standalone script file within the project's directory, and referenced correctly via its relative path.

The proper way to use a library is thus simply by downloading it from its official website, then moving/pasting it in the project's directory. In our `index.html` file we then reference the library (generally in the head tag before your artwork script runs) such that the library's functions are available in our own script:

```html
<!-- The p5 script is inside a folder called 'libraries' -->
<script src="./libraries/p5.min.js"></script>
```

If you're using node.js to develop your project, you can also download libraries via npm, and them simply bundle your project for fxhash.

### A Note on Library Licenses

When using a library, it's crucial to ensure it's distributed under a permissible license that allows for derivative commercial use. Licensing can be complex; some licenses grant full open-source rights, allowing you to use the code however you like, and even modify it for your own purposes, whereas others impose restrictions on derivative work and how the library can be redistributed.

We discuss these concepts in more detail on our Licensing page.

**What is a permissible license?** A "permissible license" is a software license that allows specific activities without infringing on the granted rights. This term often applies to open-source software licenses, which clearly outline the permissions and restrictions for using, modifying, and distributing the software.

### Reusing Libraries stored with ONCHFS

In case you are intending to store your project onchain via ONCHFS, then storage costs are something to be considered as they might get pricey

### P5

Built on top of the canvas API, [P5](https://p5js.org/) is the spiritual successor to the Processing language. It powers creative coding in the browser, and is by far the most popular library for making generative art on fxhash, many projects make use of it.

The main strength of P5 is that it is very easy to get into, and makes coding accessible to a large group of people. Moreover, it is an open-source library, which allows you to freely use and include it in your projects. It also has a flourishing community around it and there's a plethora of resources out there specifically for making visuals with code.

Here's a simple example of what the code for a P5 sketch looks like:

```jsx
function setup(){
	createCanvas(400, 400)
}

function draw(){
	ellipse(200, 200, 200)
}
```

P5 has two integral functions setup() and draw() - and as their name suggests, the setup function should contain all of the code that you want to run before drawing things to the canvas, whereas the draw function usually contains the code that draws things to the canvas.

One immediate useful thing about P5 is that you don't even have to create a canvas element manually, it provides a function that does this for you. By invoking the createCanvas() function P5 will create a canvas element and insert into the html of the page that it is run in. You should also specify the dimensions of the canvas as input parameters to that function. Then all of the p5 drawing functions will automatically draw to that canvas. P5 is very versatile, so there's a lot more that can be done here.

The advantage of using P5 in this scenario is that it adds a layer of abstraction on top of we don't have to write as much code as we would have to with pure CSS and Javascript.

### A note on running P5 in global mode with fxlens (and in other bundlers)

When using P5 with a bundler—like when you do when using fxlens—you will find that the `setup` and `draw` functions won't trigger when using P5's global mode. For example, placing this code in the **index.js** file will not render a canvas to your html page using fxlens:

```javascript
function setup(){
    createCanvas(400, 400);
    background(220);
}

function draw(){
    ellipse(p.mouseX, p.mouseY, 50, 50);
}
```

In global mode, p5.js relies on attaching its functions (like `setup()`, `draw()`, `ellipse()`, etc.) to the global `window` object so they can be accessed without a prefix.

Bundlers however encapsulate modules in local scopes to avoid polluting the global namespace. As a result, p5 can't find those functions on the global `window` object and won't automatically run `setup()` or `draw()`. To work around this, you could use P5's **instance mode:**

```javascript
const sketch = (p) => {
  p.setup = () => {
    p.createCanvas(400, 400);
    p.background(220);
  };

  p.draw = () => {
    p.ellipse(p.mouseX, p.mouseY, 50, 50);
  };
};

new p5(sketch);
```

 Or explicitly bind your functions to the `window` object as such:

```javascript
window.setup = function () {
  createCanvas(400, 400);
  background(220);
};

window.draw = function () {
  ellipse(mouseX, mouseY, 50, 50);
};
```

> [!WARNING]
> Alternatively, if you run P5 in global mode from another file—that's not named index.js—or runn it directly inside a script tag in your html, the P5 functions might end up on `window`, triggering global mode behavior. But to reliably use global mode in a bundler, you have to either attach your p5 functions to `window` manually, or use instance mode to avoid scope issues altogether.

### Other popular libraries

There are other popular libraries that are also used for the purpose of making generative art on fxhash, some of them aren’t directly libraries that draw graphics to the canvas, but rather in some cases act as auxiliary helper functions for making certain tasks easier. Some popular ones are:

- Paper.js
- chroma.js
- Spectral.js
- p5.brush
- More added soon

There are many more libraries that can be used.
