export function SubscriberForm() {
  return <form onSubmit={event => {
      event.preventDefault();
      const formData = new FormData(event.target);
      const formObject = Object.fromEntries(formData.entries());
      console.log(formObject);
      // const serviceUrl = import.meta.url.replace("index.js", ""); // 더 이상 필요하지 않습니다.
      fetch(`/api/contact`, { // 수정된 부분: 절대 경로 사용
          method:"post",
          headers: {
            "Content-Type": "application/json",
            "Origin":location.origin
          },
          body:JSON.stringify(formObject)
      }).then((res)=>{
          res.json().then((oResponse) => {
              console.log(oResponse);
              alert(`response: ${JSON.stringify(oResponse)}`);
          });
      })
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