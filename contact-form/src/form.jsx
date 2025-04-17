export function SubscriberForm() {
  return <form onSubmit={event => {
      event.preventDefault();
      const formData = new FormData(event.target);
      const formObject = Object.fromEntries(formData.entries());
      console.log(formObject);
      fetch(`/api/contact`, {
          method: "post",
          headers: {
            "Content-Type": "application/json",
            "Origin": location.origin
          },
          body: JSON.stringify(formObject)
      }).then((res)=>{
          if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
          }
          return res.json();
      }).then((oResponse) => {
          console.log(oResponse);
          alert(`response: ${JSON.stringify(oResponse)}`);
      }).catch((error) => {
          console.error('Error:', error);
          alert('Error submitting form: ' + error.message);
      });
  }}>
    <label>
      name
      <input name="name" placeholder="your name" />
    </label>
    <label>
      email
      <input name="email" placeholder="your email address" />
    </label>
    <label>
      subject
      <select name="subject">
        <option value="consulting">consulting</option>
        <option value="support">support</option>
      </select>
    </label>
    <label>
      message
      <textarea placeholder="enter your query here" name="message"></textarea>
    </label>
    <button type="submit">Send</button>
  </form>
}