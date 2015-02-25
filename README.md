# picplate

## What's this?
Picplate *(**pic**ture tem**plate**)* is an image templating micro-engine to make generation of dynamic images easier.

## How it works?
 - You create an `XML` describing how will the resulting image look like.
 - You render your image via this lib. Voila!

## Important technical info

 - Known block attributes:
     - `top`- defaults to `0`
     - `left`- defaults to `0`
     - `width` - defaults to `100%`
     - `height` - defaults to `100%`
     - `font-size` - defaults to `12px`, **is inherited**
     - `font-family` (should contain path to local `.TTF`-file), **is inherited**
     - `background-color` - defaults to transparent
     - `color` - font color, defaults to `#000000`, **is inherited**
     - `background-size` - can be `stretch`, `fit` or `cover`, defauts to `stretch`
     - `background-image` - URL of background image, defaults to none.

 - All blocks dimensions are calculated basing on the parent block size & position (similarily to CSS `position: relative`).
 - Values in percentage format (e. g. `50%`) will be calculated based on parent block's `width` and `height`.
 - Rendering flow is **similar to web**:
     - children **over** parents;
     - text **over** background image **over** background color.
 - You can nest te blocks as much as you like.
 - You can include `{{ template_placeholders }}` to set some values programmatically.
 - For the moment, you cannot have both text and child `<block>`'s in one parent.

## Contribution
You are highhly encouraged to participate in the project and help me improve it. I hope it makes your life easier, too!
