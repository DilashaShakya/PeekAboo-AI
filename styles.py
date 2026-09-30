CSS = """
#user_location { display: none !important; }
"""

# Runs when the "Share my location" button is clicked: the browser shows its
# permission popup, and whatever this returns ("lat,lon" or "") goes into the hidden box.
LOCATION_JS = """
() => new Promise((resolve) => {
  if (!navigator.geolocation) {
    alert("Your browser doesn't support location sharing.");
    return resolve("");
  }
  navigator.geolocation.getCurrentPosition(
    (pos) => resolve(`${pos.coords.latitude},${pos.coords.longitude}`),
    (err) => {
      alert("Couldn't get your location: " + err.message +
            "\\nIf you blocked it before, click the icon left of the address bar and allow Location.");
      resolve("");
    }
  );
})
"""
