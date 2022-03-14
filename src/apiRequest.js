export default async function apiRequest (method = 'GET', url = '', body = {}) {
  // Define the fetch() options.
  const options = {
    method: method,
    headers: {
      'Authorization': `Bearer ${localStorage.getItem("dungeonomicsAccessToken")}`,
      'Content-Type': 'application/json',
    },
  }
  // GET can't take a body, so check if we have a body to add to the fetch() options.
  if (Object.keys(body).length > 0) {
    options['body'] = JSON.stringify(body);
  }

  // Perform the API request.
  const response = await fetch(url, options);
  // Check for status codes and either redirect to login or return the data.
  if (response.status === 401) {
    return window.location.href = "/login";
  } else if (response.status >= 200 && response.status < 300) {
    if (method === 'DELETE') {
      return;
    } else {
      return response.json();
    };
  } else {
      return response.status;
  };
}
