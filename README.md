# picplate

## What's this?
Picplate *(**pic**ture tem**plate**)* is an image templating micro-engine to make generation of dynamic images easier.

## How it works?
 - You create an `XML` describing how will the resulting image look like.
 - You render your image via this lib. Voila!

## Example

Let's create a ticket with 4 blocks including 2 background images, 1 logo and text blocks.
Consider we have created this XML:

```
<?xml version="1.0" encoding="UTF-8" ?>
<block font-family="lato.ttf" color="#FFFFFF">
    <block top="0%" left="0%" width="50%" height="60%" background-color="#17F" background-size="cover" background-image="http://www.dhasselhoff.net/blog/wp-content/uploads/2014/03/slide1.jpg">
    </block>
    <block top="0%" left="50%" width="50%" height="60%" background-color="#050C2E">
        <block top="16%" left="10%" width="100%" height="10%" font-size="5%">
            {{ title }}
        </block>
        <block top="37%" left="10%" width="100%" height="10%" font-size="5%">
            {{ date }}
        </block>
        <block top="58%" left="10%" width="100%" height="10%" font-size="5%">
            {{ club }}
        </block>
        <block top="79%" left="10%" width="100%" height="10%" font-size="5%">
            {{ address }}
        </block>
    </block>
    <block top="60%" left="0%" width="50%" height="40%" background-color="#050C2E">
        <block top="25%" left="25%" height="50%" width="50%" background-size="fit" background-image="https://assets-cdn.github.com/images/modules/logos_page/Octocat.png"></block>
    </block>
    <block top="60%" left="50%" width="50%" height="40%" background-size="cover" background-image="http://darkfestivals.ru/wp-content/uploads/2012/02/375984_10150396170709005_246749614004_8638267_472527038_n.jpg">
        <block top="10px" left="20px" width="30px" height="40px" font-family="lato.ttf" color="#FFF" font-size="36px">Map</block>
    </block>
</block>
```

Next, we're creating a `picplate` `Ticket` instance:

    t = Ticket(filename='file.xml', width=900, height=900)
    t.assign(
        title='Some activity',
        date='Some date',
        club='Wherever',
        address='Somewhere'
    )
    img = t.render()
    img.save('out.png')

Voila. After running this script, `out.png` will be written in current directory:

[!Ticket result](http://static.dun.ai/public/img/picplate1.jpg "Ticket result")

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
