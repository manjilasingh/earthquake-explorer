// ----- CSRF helper (official Django recipe) -----
function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (const c of cookies) {
    const [key, value] = c.trim().split('=');
    if (key === name) return decodeURIComponent(value);
  }
  return null;
}
const csrftoken = getCookie('csrftoken'); // same-origin only

$("#query-form").on("submit", function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    var data = new URLSearchParams();
    data.append('method', 'postTest');
    data.append(start_date, formData.get('start_date'));
    data.append(end_date, formData.get('end_date'));
    // Add CSRF token to the request headers
    // const requiredFields = ['start_date', 'end_date'];
    // const missingFields = requiredFields.filter(field => !formData.get(field));
    // if (missingFields.length > 0) {
    //     TETHYS_APP_BASE.alert("danger", "Make sure to fill in all required fields.");
    //     return;
    // }
    // Add these lines to test the form submission handling
    // console.log("Start Date: ", formData.get('start_date'));
    // console.log("End Date: ", formData.get('end_date'));

     // Add this portion:
    fetch('.', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken
        },
        body: data

        // body: formData
     }).then(response => response.json())
     .then(data => {
        console.log(data);
    });
})