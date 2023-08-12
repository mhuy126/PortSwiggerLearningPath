# DOM XSS in jQuery selector sink using a hashchange event

> ************************Instructions************************
> 
> 
> This lab contains a [DOM-based cross-site scripting](<../../Cross-site%20Scripting%20(XSS)/Sub_Pages/DOM-based%20XSS.md>) vulnerability on the home page. It uses jQuery's `$()` selector function to auto-scroll to a given post, whose title is passed via the `location.hash` property.
> 
> To solve the lab, deliver an exploit to the victim that calls the `print()` function in their browser.
> 

Access the Lab Home → Press `Ctrl + U` to view the Page’s source → Scroll down to the end → You will find a block of script:

```tsx
$(window).on('hashchange', function(){
  // Decode the hash value and select the corresponding blog post
  var post = $('section.blog-list h2:contains(' + decodeURIComponent(window.location.hash.slice(1)) + ')');
  
  // Scroll the blog post into view if it exists
  if (post) {
    post.get(0).scrollIntoView();
  }
});
```

## Understand the script structure

- The `$` sign stands for the ************jQuery************ ****************selector****************
- `window.location.hash`: sets or returns the anchor part of a URL, including the hash sign (#). Example:
    
    ![Untitled](DOM%20XSS%20in%20jQuery%20selector%20sink%20using%20a%20hashchange%20event%20images/Untitled.png)
    
    ![Untitled](DOM%20XSS%20in%20jQuery%20selector%20sink%20using%20a%20hashchange%20event%20images/Untitled%201.png)
    
    ![Untitled](DOM%20XSS%20in%20jQuery%20selector%20sink%20using%20a%20hashchange%20event%20images/Untitled%202.png)
    
- `hashchange` event: fired when the fragment identifier of the URL has changed (the part of the URL beginning with and following the `#` symbol).
- `post.get(0)`: get the first element of the `post` object. Example:
    
    ![Untitled](DOM%20XSS%20in%20jQuery%20selector%20sink%20using%20a%20hashchange%20event%20images/Untitled%203.png)
    
- `scrollIntoView()`: scrolls an element into the visible area of the browser window. Example with the `hashchange` event and `window.location.hash`:
    
    ![Untitled](DOM%20XSS%20in%20jQuery%20selector%20sink%20using%20a%20hashchange%20event%20images/Untitled%204.png)
    

## Inject the jQuery selector `$` with the `hashchange` event

In the previous examples, the `post` variable assigned with the `$` jQuery selector looking for the element `<h2>` which contains the ************Volunteering************ string. When the element is found, the `post` variable becomes an **object**.

**What would happen if the element inside the `$()` is not available?**

![Untitled](DOM%20XSS%20in%20jQuery%20selector%20sink%20using%20a%20hashchange%20event%20images/Untitled%205.png)

Despite of the `post.get(0)` is now `undefined`, it is still an ************object************ with the length is `0` and it still exists!

![Untitled](DOM%20XSS%20in%20jQuery%20selector%20sink%20using%20a%20hashchange%20event%20images/Untitled%206.png)

********Could this object is exploitable?********

First of all, adding a `<h1>` tag instead of adding a ********node******** as a string in the `contains()` function:

![Untitled](DOM%20XSS%20in%20jQuery%20selector%20sink%20using%20a%20hashchange%20event%20images/Untitled%207.png)

Then the `post` object is defined with the `<h1>` element which has been signed:

![Untitled](DOM%20XSS%20in%20jQuery%20selector%20sink%20using%20a%20hashchange%20event%20images/Untitled%208.png)

After that, create a variable holding the element containing the id `academyLabHeader` which is the header of the page → Use the `appendChild()` function to append the previous `post` object value:

![Untitled](DOM%20XSS%20in%20jQuery%20selector%20sink%20using%20a%20hashchange%20event%20images/Untitled%209.png)

![Untitled](DOM%20XSS%20in%20jQuery%20selector%20sink%20using%20a%20hashchange%20event%20images/Untitled%2010.png)

**Behavior of the** `<img>` **element**

![Untitled](DOM%20XSS%20in%20jQuery%20selector%20sink%20using%20a%20hashchange%20event%20images/Untitled%2011.png)

![Untitled](DOM%20XSS%20in%20jQuery%20selector%20sink%20using%20a%20hashchange%20event%20images/Untitled%2012.png)

When the `src` attribute of the `<img>` element is created by assigning a value (**********vulnerable**********), the application immediately send a request to the assigned value → And because the `src` value does not exist → It returns a response with `404` status code (not found).

To handle the error of the element `<img>` when the `src` attribute is not successfully executed, the `onerror()` event is used → Assign the `onerror` with an `alert()` function:

![Untitled](DOM%20XSS%20in%20jQuery%20selector%20sink%20using%20a%20hashchange%20event%20images/Untitled%2013.png)

****************How to combine the `<img>`'s behavior with the `$()` jQuery selector?**

![Untitled](DOM%20XSS%20in%20jQuery%20selector%20sink%20using%20a%20hashchange%20event%20images/Untitled%2014.png)

We can also call the `alert()` function by injecting the URL and it will be executed by the `window.location.hash` above

![Untitled](DOM%20XSS%20in%20jQuery%20selector%20sink%20using%20a%20hashchange%20event%20images/Untitled%2015.png)

## Delivery the payload

The above injection is only the self-XSS on your on browser. Now, we need to delivery this vulnerability to another users when they access the application (the page).

To do this, click on the ******************Go to exploit server******************

![Untitled](DOM%20XSS%20in%20jQuery%20selector%20sink%20using%20a%20hashchange%20event%20images/Untitled%2016.png)

Type the below payload into the ********Body******** field:

```tsx
<iframe src="https://0a7900ab03447245801417cc0089002d.web-security-academy.net/#" onload="this.src+='<img src=0` onerror=print()>'"></iframe>
```

`this.src+=`: take the value of the previous `src` value and append it to the `<img` next to it → The `onload` event will be looked like this:

```tsx
onload="https://0a7900ab03447245801417cc0089002d.web-security-academy.net/#<img src=0 onerror=print()"
```

![Untitled](DOM%20XSS%20in%20jQuery%20selector%20sink%20using%20a%20hashchange%20event%20images/Untitled%2017.png)

To pre-view the exploit result before delivering it to the victim → Click ************************View exploit************************:

![Untitled](DOM%20XSS%20in%20jQuery%20selector%20sink%20using%20a%20hashchange%20event%20images/Untitled%2018.png)

Get back and click on ******************************************Deliver exploit to victim****************************************** and solve the lab