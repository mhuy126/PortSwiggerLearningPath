# DOM-based XSS

> In this section, we'll describe DOM-based cross-site scripting (DOM XSS), explain how to find DOM XSS vulnerabilities, and talk about how to exploit DOM XSS with different sources and sinks.
> 

# ****What is DOM-based cross-site scripting?****

DOM-based XSS vulnerabilities usually arises when JavaScript takes data from an attacker-controllable **source** (URL) → passes it into a **sink** that supports dynamic code execution (`eval()` or `innerHTML`) → Enable to execute malicious JavaScript → Allow hijacking other users’ accounts

To deliver a DOM-based XSS attack: place data into a ************source************ → it is propagated (truyền vào) to a ********************************sink******************************** → Execute malicious/arbitrary JavaScript

The most common ************source************ is the URL → Accessed by `window.location` object

Attacker can construct a link to send a victim to a vulnerable page with a payload in the query string and fragment portions of the URL

In certain circumstances (targeting a 404 page or a website running PHP), payload can also be placed in the path.

For more detail of ************sources************ and **********sinks********** → Visit the [DOM-based vulnerabilities](#)

# ****How to test for DOM-based cross-site scripting****

The majority of DOM XSS vulnerabilities can be found quickly and reliably using Burp Suite's **web vulnerability scanner**. To test for DOM-based cross-site scripting manually, you generally need to use a browser with developer tools, such as Chrome. You need to work through each available source in turn, and test each one individually.

### Testing HTML sinks

1. Place a random alphanumeric string (ex: abcdfegh123456) into the source (ex: `location.search`)
2. Use developer tools to inspect the HTML (Press `F12`)
3. Find where your string appears (Press `Ctrl + F` → Enter the inserted string)
4. Identify the context → How is your inserted string processed?
    
    ```bash
    #### For example ####
    
    # Your placed string:
    'abcdefgh123456'
    
    # The string appears:
    'abcdefgh' # The numbers/digits were removed
    '654321hgfedcba' # The string was reversed
    ```
    

**********Note:**********

- The browser’s **************View source************** (Press `Ctrl + U`) won’t work for DOM XSS testing because it doesn’t take account of changes that have been performed in the HTML by JavaScript
- Some browsers might use the **URL-Encoding** with several **sources** (ex: Chrome, Firefox, Safari URL-encode `location.search` and `location.hash` while IE11, Microsoft Edge does not)
- If your data gets **********************URL-encoded********************** before being processed → The XSS attack does not work!

### Testing JavaScript execution sinks

1. Find cases within the page’s JavaScript code where the source is being referenced (Use `Ctrl + Shift + F`)
2. Use JavaScript debugger to add a break point → Follow how the source’s value is used
3. If the source gets assigned to other variables:
    
    3.1 Use search function to track these variables → Which are passed to a sink?
    
    3.2 Find a sink that being assigned data from the sources
    
    3.3 Use debugger to inspect the value (hover the variable) before it’s sent to the sink
    
    3.4 Refine the input → Verify whether the XSS attack is successful
    

### Testing DOM XSS using DOM Invader

Read more from this [document](https://portswigger.net/burp/documentation/desktop/tools/dom-invader)

# ****Exploiting DOM XSS with different sources and sinks****

A website is vulnerable to DOM-based XSS if there is an ******************executable path****************** via which data can propagate from **********source********** to ********sink********.

The `document.write` sink works with `script` elements → Use a simple payload:

```jsx
document.write('... <script>alert(document.domain)</script> ...');
```

Visit this [Lab: DOM XSS in `document.write` sink using source `location.search`](../../Labs_Walkthrough/Cross-site%20Scripting%20(XSS)/DOM%20XSS%20in%20documentWrite%20sink%20using%20source%20locationSearch.md)

However, the content is written to `document.write` might include some surrounding context. For example, you might need to close some existing elements before using your JavaScript payload.

Visit this Lab: DOM XSS in `document.write` sink using source `location.search` inside a select element

The `innerHTML` sink and the `svg onload` events do not accept `script` elements on any modern browser → Use alternative elements like `img` or `iframe` or `onload` or `onerror`:

```jsx
element.innerHTML='... <img src=1 onerror=alert(document.domain)> ...'
```

Visit this Lab: DOM XSS in `innerHTML` sink using source `location.search`