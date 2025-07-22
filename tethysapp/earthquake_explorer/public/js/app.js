
$("#query-form").on("submit", function(event) {
    event.preventDefault();
    var formData = new FormData(this);

    // Check if all required fields are filled in
    const requiredFields = ['start_date', 'end_date'];
    const missingFields = requiredFields.filter(field => !formData.get(field));
    if (missingFields.length > 0) {
        TETHYS_APP_BASE.alert("danger", "Make sure to fill in all required fields.");
        return;
    }
    // Add these lines to test the form submission handling
    console.log("Start Date: ", formData.get('start_date'));
    console.log("End Date: ", formData.get('end_date'));

     // Add this portion:
    fetch('/apps/earthquake-explorer/', {
        method: 'POST',
        body: formData
     }).then(response => response.json())
     .then(data => {
        console.log(data);
    });
})