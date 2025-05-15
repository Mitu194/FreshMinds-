document.addEventListener("DOMContentLoaded", function() {
  const likeButton = document.querySelector(".like-btn");

  likeButton.addEventListener("click", function() {
      alert("You liked this post!");
  });

  const commentButton = document.querySelector(".comment-btn");
  
  commentButton.addEventListener("click", function() {
      alert("Comment feature coming soon!");
  });
});

function showSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.classList.remove('active');
    });

    // Remove active class from all tabs
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });

    // Show the selected section
    const selectedSection = document.getElementById(sectionId);
    selectedSection.classList.add('active');

    // Add active class to the clicked tab
    const selectedTab = document.querySelector(`a[href="#${sectionId}"]`);
    selectedTab.classList.add('active');
}

// Redirect to the About section
function redirectToAbout() {
    showSection('about');
}

function redirectToPosts() {
    // Hide all sections
    document.querySelectorAll(".content-section").forEach(section => section.classList.remove("active"));

    // Show the "Posts" section
    document.getElementById("posts").classList.add("active");

    // Update active tab
    document.querySelectorAll(".tab").forEach(tab => tab.classList.remove("active"));
    document.querySelector("[href='#posts']").classList.add("active");
}

function redirectToJobs() {
    // Hide all sections
    document.querySelectorAll(".content-section").forEach(section => section.classList.remove("active"));

    // Show the "Jobs" section
    document.getElementById("jobs").classList.add("active");

    // Update active tab
    document.querySelectorAll(".tab").forEach(tab => tab.classList.remove("active"));
    document.querySelector("[href='#jobs']").classList.add("active");
}

 const tabs = document.querySelectorAll('.nav-tabs .tab');

 // Check for the current URL to set the active tab (useful for navigation)
 const currentPath = window.location.pathname;
 
 // Function to dynamically set active tab
 function setActiveTab() {
     tabs.forEach(tab => {
         const href = tab.getAttribute('href');
         if (currentPath.includes(href)) {
             tab.classList.add('active');
         } else {
             tab.classList.remove('active');
         }
     });
 }
 
 // Add click listener to update active class without relying on URL
 tabs.forEach(tab => {
     tab.addEventListener('click', function (e) {
         tabs.forEach(t => t.classList.remove('active')); // Remove active class from all tabs
         this.classList.add('active'); // Add active class to the clicked tab
     });
 });
 
 // Set active tab based on the current URL (important for page reloads)
 setActiveTab();

 //job page::
 // Example: Updating job count dynamically
const jobCountElement = document.getElementById('job-count');
const totalJobs = 9057;

document.addEventListener('DOMContentLoaded', () => {
    jobCountElement.textContent = totalJobs.toLocaleString();
});

function navigateToJob(jobTitle) {
    // Create a URL parameter to pass the job title (optional)
    const jobPageUrl = `linkjob.html?title=${encodeURIComponent(jobTitle)}`;
    window.location.href = jobPageUrl;
}

document.addEventListener('DOMContentLoaded', () => {
      const tabs = document.querySelectorAll('.nav-tabs .tab');

    tabs.forEach(tab => {
        tab.addEventListener('click', (event) => {
            event.preventDefault();
            const targetPage = tab.getAttribute('href');
            if (targetPage) {
                window.location.href = targetPage;
            }
        });
    });
});
 
 
// Example functionality for interactivity (optional)
document.addEventListener("DOMContentLoaded", () => {
  const links = document.querySelectorAll(".nav ul li a");

  links.forEach(link => {
      link.addEventListener("click", () => {
          // Highlight the active link
          links.forEach(item => item.classList.remove("active"));
          link.classList.add("active");
      });
  });

  console.log("About page script loaded successfully!");
});
