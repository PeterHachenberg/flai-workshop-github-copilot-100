document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        const participantsList = details.participants.length > 0
          ? `<ul class="participants-list">${details.participants.map(p => `<li><span>${p}</span><button class="delete-btn" data-activity="${name}" data-email="${p}" title="Abmelden">&times;</button></li>`).join("")}</ul>`
          : `<p class="no-participants">Noch keine Teilnehmer – sei der Erste!</p>`;

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Zeitplan:</strong> ${details.schedule}</p>
          <p><strong>Verfügbarkeit:</strong> <span class="spots-badge ${spotsLeft === 0 ? 'full' : spotsLeft <= 3 ? 'limited' : 'open'}">${spotsLeft === 0 ? 'Ausgebucht' : spotsLeft + ' Plätze frei'}</span></p>
          <div class="participants-section">
            <strong>Teilnehmer (${details.participants.length}/${details.max_participants}):</strong>
            ${participantsList}
          </div>
        `;

        activitiesList.appendChild(activityCard);

        // Attach delete handlers
        activityCard.querySelectorAll(".delete-btn").forEach(btn => {
          btn.addEventListener("click", async () => {
            const activity = btn.dataset.activity;
            const email = btn.dataset.email;
            try {
              const response = await fetch(
                `/activities/${encodeURIComponent(activity)}/unregister?email=${encodeURIComponent(email)}`,
                { method: "DELETE" }
              );
              if (response.ok) {
                fetchActivities();
              } else {
                const result = await response.json();
                console.error("Unregister failed:", result.detail);
              }
            } catch (error) {
              console.error("Error unregistering:", error);
            }
          });
        });

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Aktivitäten konnten nicht geladen werden. Bitte versuche es später erneut.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
        fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "Ein Fehler ist aufgetreten";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Anmeldung fehlgeschlagen. Bitte versuche es erneut.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
